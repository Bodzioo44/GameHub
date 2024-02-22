
class Lobby:
    def __init__(self, type:str, size:int, id:int, player):
        self.type = type
        self.size = size
        self.live = False
        self.id = id
        
        self.players = [player]
        self.player_count = 1
        self.host = player
        player.Join_Lobby(self)


    #__dict__?
    def Get_Dict(self):
        pp = []
        for player in self.players:
            pp.append(player.name)

        Info = {
            "Players":pp,
            "Size":self.size,
            "Type":self.type,
            "Live":self.live,
            "Host":self.host.name
        }
        return Info

    def Add_Player(self, player):
        if self.live:
            return "Lobby already started"
        elif player.Get_Lobby() == self:
            return "Player already in this lobby"
        elif player.Get_Lobby():
            return "Cant join multiple lobbies"
        elif self.player_count == self.size:
            return "Lobby is full"
        else:
            self.player_count += 1
            self.players.append(player)
            player.Join_Lobby(self)
            return "Joined the lobby"

    def Start(self, player):
        if player != self.host:
            return "Only host can start the game"
        elif self.player_count == self.size:
            self.live = True
            return "Starting the lobby"
        else:
            return "Lobby is not filled"
        

    def Remove_Player(self, player):
        #print(f"{player.name} has left the lobby")
        self.players.remove(player)
        if player == self.host and self.players:
            self.host = self.players[0]
        player.Leave_Lobby()
        self.player_count -= 1
        return "Left the lobby"

    def Other_Players(self, current_player):
        players_to_send = []
        for player in self.players:
            if current_player != player:
                players_to_send.append(player)
        return players_to_send
    
    def Game_Update(self, current_player):
        #idk
        pass
    

    #does lobby needs to do anything with disconnected player? should sending info about disconnecting be here?
    #exit lobby whenever its not started? keep the player after the game started?
    def Disconnect_Player(self, player):
        if not self.live:
            self.Remove_Player(player)
        else:
            #do the disconnect thingy
            pass


if __name__ == "__main__":
    from Player import Player
    p1 = Player("Bodzioo", 2)
    p2 = Player("House", 4)
    l1 = Lobby("Chess_4", 4)
    l1.Add_Player(p1)
    l1.Add_Player(p2)
    l1.Add_Player(p1)
    #l1.Remove_Player(p1)
    print(l1.Get_Dict())