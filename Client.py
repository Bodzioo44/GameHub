import threading
import socket
import select
import json
import sys

from Checkers.Game import Game as Checkers_Game
from Chess.Game import Game as Chess_Game
from Assets.constants import Player_Colors

class Client:
    def __init__(self, name: str, server: str, port:int, gui = None):
        self.server = server
        self.port = port
        if gui:
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
        
    #TODO find a way to close sockets properly
    def Disconnect(self):
        self.sock.close()
        self.sock = None

    #TODO modify with enum, add optional color selection
    def Pick_Game_Type(self, type):
        match type:
            case "Chess_4":
                return Chess_Game(4)
            case "Checkers_2":
                return Checkers_Game(800)
            case "Chess_2":
                return Chess_Game(2)

    def Receive(self) -> dict:
        message = self.sock.recv(self.buff_size).decode(self.format)
        if message:
            message = json.loads(message)
            print(f"Received: {message}")
            return message
        else:
            raise socket.error("Received empty message")

    #TODO this needs to edit gui elements
    def Message_Handler(self, message:dict):
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
                    print("we would have started the game.")
                    #lobby_type, player_color = data
                    #player_color = Color(tuple(player_color))
                    #self.game = self.Pick_Game_Type(lobby_type)
                    #self.game.Assign_Online_Players(player_color, self)
                    #self.game_thread = threading.Thread(target = lambda: self.game.Start()).start()

                case "Join_Lobby":
                    print(f"Received call to join lobby, changing current widget: {data}")
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_Page)
                    self.gui.Add_Player_Info_Items(data[0])
                    self.gui.Lobby_Info.setText(data[1])

                case "Leave_Lobby":
                    print(f"Received call to leave lobby, changing current widget: {data}")
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_List_Page)

                case "Update_Lobby":
                    self.gui.Add_Player_Info_Items(data)

                case "Request_Lobbies":
                    self.gui.Add_Lobby_Tree_Items(data)
                
                case "Ping":
                    print(f"Received Ping from the server, sending it back: {message}")
                    return_message = {"Ping":data}
                    self.Send(return_message)

                case "Message":
                    print(f"Message(s) Received from the Server: ", end="")
                    for message in data:
                        print(message)

                case "Global_Chat_Box":
                    self.gui.Update_Global_Chat(data)

                case "Lobby_Chat_Box":
                    self.gui.Update_Lobby_Chat(data)

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
                #print("is this working?")
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

if __name__ == '__main__':
    import threading
    #Client1 = Client('Bodzioo','192.168.1.14', 4444)
    Client1 = Client(sys.argv[1],sys.argv[2], 4444)
    Client1.Connect()
    #t1 = threading.Thread(target=Test, args=(Client1,), daemon=True)
    #t1.start()
    Client1.StartListening()
    #t1.join(0.1)
