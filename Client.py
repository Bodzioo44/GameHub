import threading
import multiprocessing
import os
import socket
import select
import json

from Checkers.Game import Game as Checkers_Game
from Chess.Game import Game as Chess_Game
from Assets.constants import Player_Colors, Game_Type, API

#Only send one message per action, otherwise they mix up and json.loads fails
class Client:
    def __init__(self, name: str, server: str, port:int, gui):
        self.server = server
        self.port = port
        self.addr = (server, port)
        self.sock = None
        
        self.format = "utf-8"
        self.buff_size = 4096
        
        self.name = name
        self.game = None
        self.gui = gui
        
        self.listening_thread = threading.Thread(target = self._start_listening)
        self.running = True
        self.threading_error = False

    def Connect(self):
        print(f"Connecting to: {self.server}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        self.Send({"Connect":self.name})
        print("Starting listening thread...")
        self.listening_thread.start()
        
    def Disconnect(self):
        self.running = False
        print("Waiting for listening thread to finish...")
        self.listening_thread.join()
        if self.game:
            self.game.running = False
            print("Waiting for game thread to finish...")
            self.game_thread.join()
        print("Listening thread finished, closing the socket...")
        self.sock.close()
        self.gui.Stacked_Widget.setCurrentWidget(self.gui.Connection_Page)


    def Reconnect(self):
        self.running = True
        self.Connect()
        self.Send({"Request_Game_History":self.game.turn_count})


    def _start_listening(self):
        while self.running:
            read_sockets, write_sockets, error_sockets = select.select([self.sock], [], [], 2)
            if read_sockets:
                try:
                    message = self._receive()
                    self.Message_Handler(message)
                except socket.error as error:
                    print(f"BIG SOCKET ERROR DETECTED: {error}")
                    self.Disconnect()

    def Send(self, message: dict):
        message = json.dumps(message)
        self.sock.send(message.encode(self.format))
        
    def _receive(self) -> dict:
        message = self.sock.recv(self.buff_size).decode(self.format)
        #print(f"Received this shiet: {message}")
        if message:
            message = json.loads(message)
            return message
        else:
            print("Received empty message, disconnecting...")
            self.Disconnect()

    #FIXME dont fuck around with OpenGL since it doesnt really like multi-threading,
    #maybe add exception, and try multiprocessing?
    def start_game(self, type:Game_Type, color:Player_Colors):
        match type:
            case Game_Type.Chess_4:
                self.game = Chess_Game(4)
            case Game_Type.Chess_2:
                self.game = Chess_Game(2)
            case Game_Type.Checkers_2:
                self.game = Checkers_Game(800)
        self.game.Assign_Online_Players(color, self)
        #try:
        #    self.game_thread = threading.Thread(target = self.game.Start, args=(), daemon=True)
        #except pygame.error:
        #    self.Disconnect()
        print("Starting game process")
        manager = multiprocessing.Manager()
        #manager.start()
        self.game = manager.Lock()
        self.game_thread = multiprocessing.Process(target=self.game.Start)
        self.game_thread.start()
        print(f"PID of process: {self.game_thread.pid, self.game_thread.is_alive()}")

    #This edits assigned GUI based on the server response
    def Message_Handler(self, message:dict):
        for api_id, data in message.items():
            match api_id:
                case "Request_Game_History":
                    print(f"Received game history from the server: {data}")
                    self.game.Catchup(data)
                    self.game_thread.start()

                case "Game_Update":
                    if self.game:
                        self.game.Receive_Update(data)
                    else:
                        print("Received game update, but no game is assigned.")
                        
                case "Start_Lobby":
                    print(data)
                    game_type = Game_Type[data[0]]
                    print(game_type)
                    player_color = Player_Colors[data[1]]
                    print(player_color)
                    self.start_game(game_type, player_color)

                case "Join_Lobby":
                    #print(f"Received call to join lobby, changing current widget: {data}")
                    self.gui.Stacked_Widget.setCurrentWidget(self.gui.Lobby_Page)
                    self.gui.Add_Player_Info_Items(data[0])
                    self.gui.Lobby_Info_Label.setText(data[1])

                case "Leave_Lobby":
                    #print(f"Received call to leave lobby, changing current widget: {data}")
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
                    #print(f"Message(s) Received from the Server: ", end="")
                    for message in data:
                        print(message)

                case "Global_Chat_Box":
                    self.gui.Update_Global_Chat(data)

                case "Lobby_Chat_Box":
                    self.gui.Update_Lobby_Chat(data)

                case "Disconnect":
                    self.Disconnect()

                case _:
                    print(f"Invalid API {message}")


