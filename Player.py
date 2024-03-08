class Player:
    def __init__(self, name:str, sock):
        self.name = name
        self.sock = sock
        self.color = None
        #Player keeps lobby even while disconnected
        self.lobby = None

    #returns dict with player name as a key and their color as a value, maybe more values in the future
    def get_info(self) -> list:
        return [self.name, self.color.name]

    def Join_Lobby(self, lobby):
        self.lobby = lobby
    
    def Leave_Lobby(self):
        self.lobby = None
        self.color = None
        
    def Get_Lobby(self):
        return self.lobby


    def Disconnect(self):
        if self.lobby:
            self.lobby.Disconnect_Player(self)
        if not self.lobby.live:
            self.lobby = None
        self.sock = None
        self.color = None
        
    def Reconnect(self, sock):
        self.sock = sock
        #another method just for rejoining lobby?
        #self.lobby.Reconnect_Player(sock)

    def Rejoin_Lobby(self):
        pass