import socket
import select
import json
import sys
import platform

from Player import Player
from Lobby import Lobby
from Assets.constants import Game_Type
from time import strftime, localtime

class Server:
    def __init__(self, ip: str, port:int = 4444):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.format = "utf-8"
        self.buff_size = 4096
        self.Running = True
        self.lobby_list = {} #{lobby_id : Lobby}
        self.player_list = {} #{sock : Player}
        self.disconnected_player_list = {} #{name:Player}
        self.pinged_conns = []
        self.debugg = True
        
        #Maybe this needs to be called again in case of server restart?
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #nonblocking socket will throw error whenever it has to wait for data
        #self.sock.setblocking(0)
        
        if platform.system() == "Linux":
            self.inputs = [self.sock, sys.stdin]
            self.linux = True
            print("Linux detected, adding sys.stdin to inputs...")
        else:
            import threading
            self.inputs = [self.sock]
            self.linux = False
            print("sys.stdin is not supported on this OS, starting separate thread for terminal inputs...")
            Input_Thread = threading.Thread(target = lambda:self.Terminal_Input_Thread(), daemon=True)
            Input_Thread.start()

    def Start_Server(self):
        print(f"Starting server at {self.ip}:{self.port}")
        self.sock.bind(self.addr) 
        self.Listen_For_Connections()
    
        
    #TODO add check if player was the last player inside the lobby, and if so, delete the lobby
    def Disconnect(self, sock: socket.socket):
        player = self.player_list[sock]
        lobby = player.lobby
        self.disconnected_player_list.update({player.name:player})
        del self.player_list[sock]

        if return_dict := lobby.Disconnect_Player(player):
            for key, value in return_dict.items():
                self.Send(key.sock, value)
        else:
            del self.lobby_list[lobby.id]

    #assuming that player is inside disconnected list, reconnect it with passed sock
    def Reconnect(self, name: str, sock: socket.socket):
        player = self.disconnected_player_list[name] #player that we are reconnecting
        player.Reconnect(sock)
        current_time = strftime("%H:%M:%S", localtime())
        message = {"Message":[f"Sucesfully reconnected to the server as {player.name} at {current_time}"]}
        self.Send(sock, message)
        del self.disconnected_player_list[name]
        self.player_list.update({sock:player})
        print(f"Reconnected {player.name}")
        #TODO Above only reconnects player, add lobby reconnect below



    #whole API thingymajiggy
    #If possible lobby methods should return dict with api calls assigned to each player
    def Message_Handler(self, message, current_sock):
        current_player = self.player_list[current_sock] #Player object we are handling
        current_lobby = current_player.lobby #Lobby object we are handling (None is possible)
        for api_id, data in message.items():
            match api_id:
                case "Request_Lobbies":
                    return_dict = {"Request_Lobbies":self._Generate_Lobby_Data_List()}
                    self.Send(current_sock, return_dict)

                #TODO if lobby creation is successful, update all other players about it
                case "Create_Lobby":
                    if current_lobby:
                        return_dict = {"Message":["Cant create a lobby while in another lobby."]}
                    else:
                        lobby_id = self.Get_Lobby_ID()
                        try:
                            game_type = getattr(Game_Type, data)
                            new_lobby = Lobby(game_type, lobby_id)
                            self.lobby_list.update({lobby_id:new_lobby})
                            return_dict = new_lobby.Join(current_player)[current_player]
                        except AttributeError:
                            return_dict = {"Message":["Invalid lobby type"]}

                    self.Send(current_sock, return_dict)

                #data = lobby_id
                case "Join_Lobby":
                    if data in self.lobby_list.keys(): #checks if lobby exists
                        lobby = self.lobby_list[data] 
                        for key, value in lobby.Join(current_player).items(): #Lobby actions should return whole dict with message and data
                            self.Send(key.sock, value)
                    else:
                        return_dict = {"Message":["Invalid lobby id"]}
                        self.Send(current_sock, return_dict)

                #messages other players that someone left
                #sends current lobby list to the current_player.
                case "Leave_Lobby":
                    if current_lobby:
                        
                        if return_dict := current_lobby.Leave(current_player):
                            for key, value in return_dict.items(): #this messages other players that someone left
                                self.Send(key.sock, value)
                                
                            self.Send(current_sock, {"Leave_Lobby":self._Generate_Lobby_Data_List()}) 
                        else:
                            del self.lobby_list[current_lobby.id]

                    else:
                        return_dict = {"Message":["Player not in a lobby"]}
                        self.Send(current_sock, return_dict)
                        
                #everything below might have outdated variable names
                case "Start_Lobby":
                    if current_lobby:
                        for key, value in current_lobby.start(current_player).items():
                            self.Send(key.sock, value)
                            
                    else:
                        return_dict = {"Message":["Not inside a lobby"]}
                        self.Send(current_sock, return_dict)

                case "Game_Update":
                    lobby = player.lobby
                    if lobby and lobby.live:
                        players_to_send = lobby.Other_Players(player)
                        for player in players_to_send:
                            self.Send(player.sock, {"Game_Update":data})
                    else:
                        return_dict = {"Message":["Join or start a lobby first"]}
                        self.Send(current_sock, return_dict)
                        
                case "Request_Game_History":
                    lobby = player.lobby
                    return_dict = {"Request_Game_History":lobby.Request_Game_History(data)}
                    self.Send(current_sock, return_dict)

                case "Lobby_Chat_Box":
                    if current_lobby := current_player.Get_Lobby():
                        self.Send_Lobby(current_lobby, {api_id:data})
                    else:
                        self.Send(current_sock, {api_id:["Join a Lobby First!"]})

                case "Global_Chat_Box":
                    self.Send_All({api_id:data})

                case "Message":
                    print(f"Message(s) Received from {current_player.name}: ", end="")
                    for message in data:
                        print(message)

                case "Ping":
                    self.pinged_conns.remove(current_sock)
                    print(f"{current_player.name} has responded to the ping.")

                case _:
                    print(f"Invalid API id!: {api_id}")


    def Listen_For_Connections(self):
        self.sock.listen()
        print(f"Listening for new connections at {self.ip}:{self.port}")
        try:
            while self.Running:
                all_inputs = self.inputs + list(self.player_list.keys())
                read_sockets, write_sockets, error_sockets = select.select(all_inputs, [], [], 2) #2 sec timeout, for keyboard interrupt (temp)
                if read_sockets:
                    for sock in read_sockets:
                        #handling new connections requests
                        if sock == self.sock:
                            conn, addr = sock.accept() #accepts conneciton
                            player_tag = self.Receive(conn)["Connect"] #receives name from the client
                            taken_sock = self.Check_Player_Tag_Availability(player_tag) #returns None or socket assigned to that name

                            if taken_sock: #actions if name is already taken
                                #TODO this might force reconnect if client requests for connections are too fast. but idk
                                #for example if 2nd connection attempt comes before ping response from the client (or even in the same loop iteration, maybe sort the list?)
                                #timeout thread is a solution, or just ignore it since its not password protected anyway
                                if sock in self.pinged_conns: #checks if socket was already pinged. if its still there it means client didnt respond.
                                    self.Disconnect(taken_sock)
                                    self.Reconnect(player_tag, conn)
                                    
                                else: #if socket was not pinged, ping it and tell client to try again. (in case client doesnt respond to the pign)
                                    self.pinged_conns.append(taken_sock) #adds pinged socket to the list
                                    self.Send(taken_sock, {"Ping":"Connection_Check"}) #sends ping to the client
                                    message = {"Disconnect":"Name already taken, disconnecting from the server... If you are sure name is available, try again"}
                                    print(f"{addr[0]}:{addr[1]} tried to connect under already taken name, sending disconnect message...")
                                    self.Send(conn, message)

                            elif player_tag in list(self.disconnected_player_list.keys()):
                                self.Reconnect(player_tag, conn)
                                    
                            else: #if the name is unique create new player
                                new_player = Player(player_tag, conn)
                                self.player_list.update({conn:new_player})
                                current_time = strftime("%H:%M:%S", localtime())
                                print(f"{addr[0]}:{addr[1]} Connected to the Server as {new_player.name} at: {current_time}")
                                message = {"Message":[f"Connected to the Server as {new_player.name} at: {current_time}"]}
                                self.Send(conn, message)

                        #optional for sys.stdin in linux to avoid threading
                        elif self.linux and sock == sys.stdin:
                            terminal_input = sys.stdin.readline()
                            try:
                                eval(terminal_input)
                            except json.decoder.JSONDecodeError:
                                print("Wrong input format, cant decode to json")
                            except Exception as error:
                                    print(f"this is error {error}")
                                
                        #Handling existing connections
                        else:
                            try:
                                message = self.Receive(sock) #this should raise socket.error if message is empty (disconnect message)
                                #print(f"Received a message from {self.player_list[sock].name}: {message}")
                                self.Message_Handler(message, sock)
                                
                            except socket.error as error:
                                print(f"Socket error detected: {error}")
                                self.Disconnect(sock)
                                
            #closing actions
            #TODO message all clients that server is dead before closing?
            self.sock.close()    

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.Running = False

    #just because Windows is retarded, wont matter in the final usecase
    def Terminal_Input_Thread(self):
        while self.Running:
            #TODO somehow move this line to the bottom of the terminal feed (different for windows/linux? idk yet)
            try:
                message = input("Send to all clients (in form of api): ")
                if self.Running:
                    eval(message)
                else:
                    print("Server is down, restart it first")
            except NameError:
                print("Invalid call, try again")
            except EOFError:
                print("Shutting down Terminal Input Thread...")
            except json.decoder.JSONDecodeError:
                print("Wrong input format, cant decode to json")

    #TODO Add check if the player is still connected here?
    def Send(self, conn: socket.socket, message: dict):
        if self.debugg:
            print(f"Sent: {message}")
        message = json.dumps(message)
        conn.send(message.encode(self.format))

    def Send_Lobby(self, lobby:Lobby, message:dict):
        for player in lobby.players:
            self.Send(player.sock, message)

    #Sends message to all clients
    def Send_All(self, message:dict):
        for key in self.player_list.keys():
            self.Send(key, message)


    #TODO change it, so it only returns NOT live lobbies
    def _Generate_Lobby_Data_List(self) -> dict:
            lobby_list_values = []
            for lobby in self.lobby_list.values():
                lobby_list_values.append(lobby.Get_List())
            return lobby_list_values

    #Pings the client
    def Ping(self, conn: socket.socket):
        message = {"Ping":0}
        self.Send(conn, message)
    
    #Receives message from socket and checks if its empty
    def Receive(self, conn: socket.socket) -> dict:
        message = conn.recv(self.buff_size).decode(self.format)
        if message:
            message = json.loads(message)
            if self.debugg:
                print(f"Received: {message}")
            return message
        else:
            raise socket.error("Received empty message")

    #Check if player name is already taken (by active player)
    def Check_Player_Tag_Availability(self, tag:str):
        for key, value in self.player_list.items():
            if value.name == tag:
                return key
        return False
    
    #Generate unique lobby id, there probably is more efficient way to do this
    def Get_Lobby_ID(self) -> int:
        i = 1
        acitve_lobbies = list(self.lobby_list.keys())
        while True:
            if i not in acitve_lobbies:
                return i
            i += 1
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = '192.168.1.14'
    Server1 = Server(ip, 4444)
    Server1.Start_Server()