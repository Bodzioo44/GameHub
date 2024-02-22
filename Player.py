class Player:
    def __init__(self, name:str, sock):
        self.name = name
        self.sock = sock
        self.lobby = None

    def Disconnect(self):
        if self.lobby:
            self.lobby.Disconnect_Player(self)
        self.sock = None
        
    def Reconnect(self, sock):
        self.Connect(sock)
        
    def Connect(self, sock):
        self.sock = sock

    def Get_Lobby(self):
        return self.lobby
    
    
    #cant join multiple lobbies, etc...
    def Join_Lobby(self, lobby):
        self.lobby = lobby
    
    def Leave_Lobby(self):
        self.lobby = None
        
    