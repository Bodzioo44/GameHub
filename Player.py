class Player:
    def __init__(self, name:str, sock):
        self.name = name
        self.sock = sock
        self.color = None
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

        

    #handling connection and disconnection during active game, not used for now
    def Disconnect(self):
        if self.lobby:
            self.lobby.Disconnect_Player(self)
        self.sock = None
        
    def Reconnect(self, sock):
        self.Connect(sock)
        
    def Connect(self, sock):
        self.sock = sock