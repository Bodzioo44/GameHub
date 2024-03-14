import threading
import socket
import select
import json

from Checkers.Game import Game as Checkers_Game
from Assets.constants import Player_Colors, Game_Type, API, get_local_ip

#Only send one message per action, otherwise they mix up and json.loads fails
class Client:
    def __init__(self, gui):
        self.format = "utf-8"
        self.buff_size = 4096

        self.game = None
        self.gui = gui
        
        self.running = False

    def connect(self, name:str = "Bodzioo", ip:str = get_local_ip(), port:int = 4444):
        self.ip = ip
        self.port = port
        self.name = name
        self.addr = (self.ip, self.port)
        
        print(f"Connecting to: {self.ip}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.connect(self.addr)
        self.send({"Connect":self.name})
        print("Starting listening thread...")
        self.running = True
        #self.listening_thread = threading.Thread(target = self._start_listening)
        #self.listening_thread.start()

    def disconnect(self):
        if self.running:
            print("Disconnecting from the server...")
            print("Waiting for listening thread to finish...")
            self.gui.thread.terminate()
            self.running = False
            print("Listening thread finished, closing the socket...")
            self.sock.close()
        self.gui.Stacked_Widget.setCurrentWidget(self.gui.Connection_Page)
        

    #TODO move this to the pyqt5 loop?
    #yep, prolly the good idea to avoid QObject::setParent: Cannot set parent, new parent is in a different thread
    #totally yep, try pyqtSingal and WorkerThread
    def _start_listening(self):
        while self.running:
            #print("Listening for messages...")
            read_sockets, write_sockets, error_sockets = select.select([self.sock], [], [], 2)
            if read_sockets:
                try:
                    message = self._receive()
                    self._message_handler(message)
                except socket.error as error:
                    print(f"BIG SOCKET ERROR DETECTED: {error}")
                    self.disconnect()

    def send(self, message: dict):
        #print(f"Sending this shiet: {message}")
        message = json.dumps(message)
        self.sock.send(message.encode(self.format))
        
    def _receive(self) -> dict:
        #print(self.sock)
        message = self.sock.recv(self.buff_size).decode(self.format)
        #print(f"Received this shiet: {message}")
        if message:
            message = json.loads(message)
            return message
        else:
            print("Received empty message, disconnecting...")
            self.disconnect()


    def start_game(self, type:Game_Type, color:Player_Colors):
        match type:
            case Game_Type.Checkers_2:
                self.game = Checkers_Game(400, self, color)
        
        self.gui.start_game_widget(self.game)



    #This edits assigned GUI based on the server response
    def _message_handler(self, message:dict):
        for api_id, data in message.items():
            match api_id:
                case "Request_Game_History":
                    print(f"Received game history from the server: {data}")

                case "Game_Update":
                    print("Received game update")
                    self.game.receive_update(data)
                    
                case "Start_Lobby":
                    print(data)
                    game_type = Game_Type[data[0]]
                    print(game_type)
                    player_color = Player_Colors[data[1]]
                    print(player_color)
                    self.start_game(game_type, player_color)

                case "Join_Lobby":
                    #print(f"Received call to join lobby, changing current widget: {data}")
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_Info_Page)
                    self.gui.add_lobby_info_item(data[0])
                    self.gui.set_lobby_info_label(data[1])

                case "Leave_Lobby":
                    #print(f"Received call to leave lobby, changing current widget: {data}")
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_List_Page)

                case "Update_Lobby":
                    self.gui.add_lobby_info_item(data)

                case "Request_Lobbies":
                    self.gui.add_lobby_tree_item(data)
                
                case "Ping":
                    print(f"Received Ping from the server, sending it back: {message}")
                    return_message = {"Ping":data}
                    self.send(return_message)

                case "Message":
                    #print(f"Message(s) Received from the Server: ", end="")
                    for message in data:
                        print(message)

                case "Global_Chat_Text_Edit":
                    self.gui.update_global_chat(data)

                case "Lobby_Chat_Text_Edit":
                    self.gui.update_lobby_chat(data)

                case "Disconnect":
                    for message in data:
                        print(message)
                    self.disconnect()

                case _:
                    print(f"Invalid API {message}")
