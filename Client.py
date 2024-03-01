import threading
import socket
import select
import json
import sys

from Checkers.Game import Game as Checkers_Game
from Chess.Game import Game as Chess_Game
from Assets.constants import Color
#from PyQtMenu_v2 import MainWindow



class Client:
    def __init__(self, name: str, server: str, port:int, gui):
        self.server = server
        self.port = port
        self.gui = gui
        self.name = name
        self.addr = (server, port)
        self.sock = None
        self.format = "utf-8"
        self.buff_size = 4096
        self.game = None

    def Connect(self):
        print(f"Connecting to: {self.server}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        print(f"Connected to {self.sock}")
        #sending player_id for verification
        self.Send({"Connect":self.name})

    def Send(self, message: dict):
        print(f"Sent: {message}")
        message = json.dumps(message)
        #print(f"Sending: {message}")
        self.sock.send(message.encode(self.format))
        
    def Disconnect(self):
        self.sock.close()
        self.sock = None
        
    def Pick_Game_Type(self, type):
        match type:
            case "Chess_4":
                return Chess_Game(4)
            case "Checkers_2":
                return Checkers_Game(800)
            case "Chess_2":
                return Chess_Game(2)

    def Receive(self):
        message = self.sock.recv(self.buff_size).decode(self.format)
        if message:
            message = json.loads(message)
            print(f"Received: {message}")
            return message
        else:
            raise socket.error("Received empty message")

    #TODO this needs to edit gui elements
    def Message_Handler(self, message):
        for api_id, data in message.items():
            #print(f"Received: {api_id}:{data}")
            match api_id:
                case "Game_Update":
                    if self.game:
                        self.game.Receive_Update(data)
                    else:
                        print("we shouldnt be here, but idk")
                
                #data = lobby_type, player_color
                case "Start_Lobby":
                    print("we got here?")
                    lobby_type, player_color = data
                    player_color = Color(tuple(player_color))
                    self.game = self.Pick_Game_Type(lobby_type)
                    self.game.Assign_Online_Players(player_color, self)
                    self.game_thread = threading.Thread(target = lambda: self.game.Start()).start()
                
                #Data = lobby [id, players, type, live]
                case "Create_Lobby":
                    print(data)
                    self.gui.Add_Lobby_Tree_Item(data)

                #Data = lobby_id
                case "Leave_Lobby":
                    self.gui.Remove_Lobby_Tree_Item(data)

                case "Request_Lobbies":
                    for key, value in data.items():
                        print(f"Lobby id: {key}, Lobby info: {value}")
                
                case "Ping":
                    print(f"Received Ping from the server, sending it back: {message}")
                    return_message = {"Ping":data}
                    self.Send(return_message)

                case "Message":
                    print(f"Message(s) Received from the Server: ", end="")
                    for message in data:
                        print(message)

                case "Disconnect":
                    print(data)
                    self.Disconnect()

                case _:
                    print(f"Invalid API {message}")

    def StartListening(self):
        if self.sock:
            print("Starting listening...")
        try:
            while self.sock:
                print("is this working?")
                read_sockets, write_sockets, error_sockets = select.select([self.sock], [], [], 2)
                if read_sockets: #just one socket, so no need to iterate anything
                    try:
                        message = self.Receive()
                        self.Message_Handler(message)
                    except socket.error as error:
                        print(f"socket error, disconnecting: {error}")
                        self.Disconnect()
                        
            print("Disconnected from the server.")
        except KeyboardInterrupt:
            self.Disconnect()
            self.game.Kill()
            self.game_thread.join()
            print("Keyboard Interrupt")

def Test(Client:Client):
    while True:
        message = input()
        match message:
            case "a":
                Client.Send({"Create_Lobby":("Checkers_2", 2)})
            case "b":
                Client.Send({"Request_Lobbies":0})
            case "c":
                Client.Send({"Leave_Lobby":0})
            case "d":
                Client.Send({"Join_Lobby":1})
            case "e":
                Client.Send({"Start_Lobby":0})


if __name__ == '__main__':
    import threading
    #Client1 = Client('Bodzioo','192.168.1.14', 4444)
    Client1 = Client(sys.argv[1],sys.argv[2], 4444)
    Client1.Connect()
    t1 = threading.Thread(target=Test, args=(Client1,), daemon=True)
    t1.start()
    Client1.StartListening()
    t1.join(0.1)