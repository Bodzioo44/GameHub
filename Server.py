
import socket
import select
import json
import sys
import platform

from Player import Player
from Lobby import Lobby
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
        self.game_types = {"Chess_4" : 4, "Chess_2" : 2, "Checkers" : 2}
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
            Input_Thread = threading.Thread(target = self.Terminal_Input_Thread, args = (), daemon=True)
            Input_Thread.start()

    def Start_Server(self):
        print(f"Starting server at {self.ip}:{self.port}")
        self.sock.bind(self.addr) 
        self.Listen_For_Connections()
        
    def Disconnect(self, sock):
        player = self.player_list[sock]
        player.Disconnect()
        self.disconnected_player_list.update({player.name:player})
        del self.player_list[sock]
        sock.close()
        print(f"disconnecting {player.name} because of socket error")

    #assuming that player is inside disconnected list, reconnect it with passed sock
    def Reconnect(self, name: str, sock: socket.socket):
        
        player = self.disconnected_player_list[name] #player that we are reconnecting
        player.Reconnect(sock)
        current_time = strftime("%H:%M:%S", localtime())
        message = {"Message":f"Sucesfully reconnected to the server as {player.name} at {current_time}"}
        self.Send(sock, message)
        del self.disconnected_player_list[name]
        self.player_list.update({sock:player})
        print(f"Reconnected {player.name}")

    #whole API thingymajiggy
    def Message_Handler(self, message, sock):
        player_name = self.player_list[sock].name #name of the client we are handling
        player = self.player_list[sock] #Player object we are handling
        
        for api_id, data in message.items():
            match api_id:
                #data = (game_update_data)
                case "Game_Update":
                    lobby = player.lobby
                    if lobby and lobby.live:
                        players_to_send = lobby.Other_Players(player)
                        for player in players_to_send:
                            self.Send(player.sock, data)
                    else:
                        return_message = {"Message":"Join or start a lobby first"}
                        self.Send(sock, return_message)
                
                case "Message":
                    print(f"Message Received from {player_name}: {data}")
                    
                case "Request_Lobbies":
                    new_list = {}
                    for key, value in self.lobby_list.items():
                        new_list.update({key:value.Get_Dict()})
                    return_message = {"Request_Lobbies":new_list}
                    self.Send(sock, return_message)

                #data = (lobby_type, lobby_size)
                case "Create_Lobby":
                    if player.Get_Lobby():
                        return_message = {"Message":"Cant create a lobby while in another lobby."}
                    else:
                        lobby_id = self.Get_Lobby_ID()
                        lobby_type, lobby_size = data
                        new_lobby = Lobby(lobby_type, lobby_size, lobby_id, player)
                        self.lobby_list.update({lobby_id:new_lobby})
                        return_message = {"Message":f"Joined lobby {lobby_id}"}
                    self.Send(sock, return_message)

                #data = lobby_id
                case "Join_Lobby":
                    if data in list(self.lobby_list.keys()):
                        lobby = self.lobby_list[data]
                        return_message = {"Message":lobby.Add_Player(player)}
                    else:
                        return_message = {"Message":"Invalid lobby id"}
                    self.Send(sock, return_message)

                case "Leave_Lobby":
                    if player.lobby:
                        lobby = player.lobby
                        return_message = {"Message":lobby.Remove_Player(player)}
                        
                        if lobby.player_count == 0:
                            del self.lobby_list[lobby.id]
                    else:
                        return_message = {"Message":"Player not in a lobby"}
                        
                    self.Send(sock, return_message)
                        
                case "Start_Lobby":
                    lobby = player.lobby
                    if lobby:
                        return_message = {"Message":lobby.Start(player)}
                        if lobby.live:
                            for player in lobby.players:
                                self.Send(player.sock, return_message)
                        else:
                            self.Send(sock, return_message)
                    else:
                        return_message = {"Message":"Not inside a lobby"}
                        self.Send(sock, return_message)
                        

                    
                        
                        
                case "Ping":
                    self.pinged_conns.remove(sock)
                    print(f"{player_name} has responded to the ping.")

                case _:
                    print("api doesnt match, whoops")


    def Listen_For_Connections(self):
        self.sock.listen()
        print(f"Listening for new connections at {self.ip}:{self.port}")
        try:
            while self.Running:
                all_inputs = self.inputs + list(self.player_list.keys())
                read_sockets, write_sockets, error_sockets = select.select(all_inputs, [], all_inputs, 2) #2 sec timeout, for keyboard interrupt (temp)
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
                                message = {"Message":f"Connected to the Server as {new_player.name} at: {current_time}"}
                                self.Send(conn, message)

                        #optional for sys.stdin in linux to avoid threading
                        elif self.linux and sock == sys.stdin:
                            terminal_input = sys.stdin.readline()
                            try:
                                self.Send_All(terminal_input)
                            except json.decoder.JSONDecodeError:
                                print("Wrong input format, cant decode to json")
                                
                        #Handling existing connections
                        else:
                            try:
                                message = self.Receive(sock) #this should raise socket.error if message is empty (disconnect message)
                                #print(f"Received a message from {self.player_list[sock].name}: {message}")
                                self.Message_Handler(message, sock)
                                
                            except socket.error as error:
                                print(f"Socket error detected: {error}")
                                self.Disconnect(sock)
                                
                #anything interesting in here?
                if error_sockets:
                    for e in error_sockets:
                        print("BIG ERRORRORORORORORORROROROROROROR")
                        print(e)
                        
            #closing actions
            #TODO message all clients that server is dead before closing?
            self.sock.close()    
                                
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.Running = False

    #just because Windows is retarded
    def Terminal_Input_Thread(self):
        while self.Running:
            #TODO somehow move this line to the bottom of the terminal feed (different for windows/linux? idk yet)
            #TODO add eval() method to write code directly into feed? 100% secure
            #just leave it for the end
            try:
                message = input("Send to all clients (in form of api): ")
                if self.Running:
                    self.Send_All(message)
                else:
                    print("Server is down, restart it first")
            except EOFError:
                print("Shutting down Terminal Input Thread...")
            except json.decoder.JSONDecodeError:
                print("Wrong input format, cant decode to json")

    #Sends message to a specific client
    def Send(self, conn: socket.socket, message: dict):
        if self.debugg:
            print(f"Sent: {message}")
        message = json.dumps(message)
        conn.send(message.encode(self.format))

    #Sends message to all clients
    def Send_All(self, message:str):
        message = json.loads(message)
        for key in self.player_list.keys():
            self.Send(key, message)

    #Pings the client
    def Ping(self, conn: socket.socket):
        message = {"Ping":0}
        self.Send(conn, message)
    
    #Receives message from socket and checks if its empty
    def Receive(self, conn: socket.socket):
        message = conn.recv(self.buff_size).decode(self.format)
        if message:
            message = json.loads(message)
            if self.debugg:
                print(f"Received: {message}")
            return message
        else:
            raise socket.error("Received empty message")

    #Check if player name is already taken (by active player)
    def Check_Player_Tag_Availability(self, tag):
        for key, value in self.player_list.items():
            if value.name == tag:
                return key
        return False
    
    #Generate unique lobby id
    def Get_Lobby_ID(self):
        i = 1
        acitve_lobbies = list(self.lobby_list.keys())
        while True:
            if i not in acitve_lobbies:
                return i
            i += 1




if __name__ == "__main__":
    Server1 = Server("127.0.0.1", 4444)
    Server1.Start_Server()
    #print("we done")
    
    
    
    """    
    
        def Listen_For_Connections(self):
        self.sock.listen()
        print(f"Listening for new connections at {self.ip}:{self.port}")
        if platform.system() == "Linux":
            inputs = [self.sock, sys.stdin]
            linux = True
            print("Linux detected, adding sys.stdin to inputs...")
        else:
            inputs = [self.sock]
            linux = False
            print("sys.stdin is not supported on this OS, starting separate thread for terminal inputs...")
            Input_Thread = threading.Thread(target = self.Terminal_Input_Thread, args = (), daemon=True)
            Input_Thread.start()

        try:
            while self.Running:
                all_inputs = inputs + list(self.player_list.keys())
                read_sockets, write_sockets, error_sockets = select.select(all_inputs, [], all_inputs, 2)
                if read_sockets:
                    for sock in read_sockets:
                        #handling new connections requests
                        if sock == self.sock:
                            conn, addr = sock.accept()
                            player_tag = self.Receive(conn)["Connect"]

                            taken_sock = self.Check_Player_Tag_Availability(player_tag) #returns None or socket that is assigned to that name
                            
                            
                            if taken_sock:
                                if sock not in self.pinged_conns:
                                    self.pinged_conns.append(taken_sock)
                                    self.Send(taken_sock, {"Ping":"Connection_Check"})
                                    
                                    message = {"Disconnect":"Name already taken, disconnecting from the server... if you are sure name is avaiable try again."}
                                    print(f"{addr[0]}:{addr[1]} tried to connect under already taken name, disconnecting")
                                    self.Send(conn, message)
                                    continue
                                else:
                                    
                                    self.pinged_conns.remove(taken_sock)

                            new_player = Player(player_tag, conn)
                            
                            self.player_list.update({conn:new_player})
                            current_time = strftime("%H:%M:%S", localtime())
                            print(f"{addr[0]}:{addr[1]} Connected to the Server as {new_player.name} at: {current_time}")
                            message = {"Message":f"Connected to the Server as {new_player.name} at: {current_time}"}
                            self.Send(conn, message)

                        #optional for sys.stdin in linux to avoid threading
                        elif linux and sock == sys.stdin:
                            input = sys.stdin.readline()
                            try:
                                self.Send_All(input)
                            except json.decoder.JSONDecodeError:
                                print("Wrong input format, cant decode to json")
                                
                        #Handling existing connections
                        else:
                            try:
                                message = self.Receive(sock)
                                if message:
                                    print(f"Received a message from {self.player_list[sock].name}: {message}")
                                    self.Message_Handler(message, sock)
                                else:
                                    print("Empty message, disconnecting...")
                                    self.Disconnect(sock)
                                    
                            except socket.error as error:
                                print(f"socket error detected, disconnecting: {error}")
                                self.Disconnect(sock)
                #anything interesting in here?
                if error_sockets:
                    for e in error_sockets:
                        print("BIG ERRORRORORORORORORROROROROROROR")
                        print(e)
            #closing actions
            #TODO message all clients that server is dead?
            self.sock.close()    
                                
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.Running = False
    
    
    def Test(Server:Server):
    while True:
        message = input()
        Server.Send_All_Test(message)
        
        
    def Listen_For_Connections_WORKING(self):
        self.sock.listen()
        x = True
        self.inputs = []
        try:
            while x:
                print("its alive!")
                print([self.sock] + self.inputs)
                read_sockets, write_sockets, error_sockets = select.select([self.sock] + self.inputs, [], [], 2)
                
                if read_sockets:
                    print("We got something!")
                    for socket in read_sockets:
                        
                        if socket == self.sock:
                            print(f"its a new connection!")
                            
                            print(f"TO SERVER:    {socket}")
                            conn, addr = socket.accept()
                            print(f" FROM CLIENT  {conn}")
                            conn.setblocking(0)
                            self.Send(conn, {"Message":f"FUCK"})
                            self.inputs.append(conn)
                        else:
                            print("its a message!")
                            data = socket.recv(4096)
                            if data:
                                print(data)
                            else:
                                print("PROGRESS")
                        
        except KeyboardInterrupt:
            x = False
    """
    