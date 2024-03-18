from PyQt5.QtWidgets import QApplication
import socket
import json

from Checkers.Game import Game as Checkers_Game
from Chess.Game import Game as Chess_Game
from Assets.constants import Player_Colors, Game_Type, API, get_local_ip
from time import sleep

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
            self.gui.thread.stop()
            print("Listening thread finished, closing the socket...")
            self.sock.close()
        self.gui.Stacked_Widget.setCurrentWidget(self.gui.Connection_Page)

    def send(self, message: dict):
        #print(f"Sending this shiet: {message}")
        message = json.dumps(message)
        self.sock.send(message.encode(self.format))

    def start_game(self, type:Game_Type, color:Player_Colors):
        match type:
            case Game_Type.Chess_2:
                self.game = Chess_Game(400, self, color)
            case Game_Type.Checkers_2:
                self.game = Checkers_Game(400, self, color)
        self.gui.start_game_widget(self.game)

    def catch_up(self, history:dict):
        for value in history.values():
            #print(f"processing: {value}")
            self.game.receive_update(value, True)
            sleep(0.5)
            #FIXME VERY ugly solution imo
            #replace with QThread and block moves until its done
            QApplication.processEvents()

    #This edits assigned GUI based on the server response
    #receiveing raw json data from the server
    def message_handler(self, message:str):
        message = json.loads(message)
        for api_id, data in message.items():
            print(f"Proccesing {api_id} with data: {data}")
            match api_id:
                case "Request_Game_History":
                    self.catch_up(data)
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
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_Info_Page)
                    self.gui.add_lobby_info_item(data[0])
                    self.gui.set_lobby_info_label(data[1])

                case "Leave_Lobby":
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

                case "Socket_Error":
                    for message in data:
                        print(message)
                    self.disconnect()

                case "Empty_Message":
                    print("Empty message received.")
                    self.disconnect()

                case _:
                    print(f"Invalid API {message}")
