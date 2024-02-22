import socket
import select
import json
import sys
#from time import sleep
#from Assets.constants import API

#TODO pass game object into client, and calling its update method every time we receive data...
class Client:
    def __init__(self, name: str, server: str, port:int = 4444):
        self.server = server
        self.port = port
        self.addr = (server, port)
        self.sock = None
        self.format = "utf-8"
        self.buff_size = 4096
        self.name = name
        #self.disconnect_message = {"Disconnect":self.name}

    def Connect(self):
        print(f"Connecting to: {self.server}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        print(f"Connected to {self.sock}")
        #sending player_id for verification
        self.Send({"Connect":self.name})

    def Send(self, message: dict):
        message = json.dumps(message)
        #print(f"Sending: {message}")
        self.sock.send(message.encode(self.format))
        
    def Disconnect(self):
        self.sock.close()
        self.sock = None

    def Receive(self):
        message = self.sock.recv(self.buff_size).decode(self.format)
        if message:
            message = json.loads(message)
            return message
        else:
            raise socket.error("Received empty message")

    def Message_Handler(self, message):
        for api_id, data in message.items():
            match api_id:
                case "Game_Update":
                    pass
                
                case "Start_Lobby":
                    pass
                
                case "Request_Lobbies":
                    for key, value in data.items():
                        print(f"Lobby id: {key}, Lobby info: {value}")
                
                case "Ping":
                    print(f"Received Ping from the server, sending it back: {message}")
                    return_message = {"Ping":data}
                    self.Send(return_message)

                case "Message":
                    print(data)
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
            case "f":
                Client.Send({"Game_Update": {"Hello":"This would be game data to update OwO"}})
                



if __name__ == '__main__':
    import threading
    #Client1 = Client('Bodzioo','192.168.1.14', 4444)
    Client1 = Client(sys.argv[1],'127.0.0.1', 4444)
    Client1.Connect()
    t1 = threading.Thread(target=Test, args=(Client1,), daemon=True)
    t1.start()
    Client1.StartListening()
    t1.join(0.1)
    
    
    
    
    """
        #checking server response
        message = self.Receive()
        #replace this with self.Message handler, or just delete this whole thing (along with above line)
        for key, value in message.items():
            if key == "Disconnect":
                print(value)
                self.sock = None
            elif key == "Message":
                print(value)
            else:
                print("Received invalid api from the server, disconnecting...")
                self.sock = None

    def Send(self, conn: socket.socket, message: dict):
        message = json.dumps(message)
        conn.send(message.encode(self.format))
    """