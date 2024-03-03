from Assets.constants import Color


class Lobby:
    def __init__(self, type:str, size:int, id:int, player):
        self.type = type
        self.size = size
        self.live = False
        self.id = id
        self.colors = {}
        
        self.players = [player]
        self.player_count = 1
        self.Assign_Color(player)
        self.host = player
        player.Join_Lobby(self)
        
        self.game_history = {}


    #__dict__?
    #Add everything that needs to be displayed in GUI into single dict with multiple entries
    #so the lobby description would look like this: Lobby id - 2; Player Count - (2/4);Game type - Chess; Live - True
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
    
    def Get_List(self):
        pp = []
        for player in self.players:
            pp.append(player.name)
        Info = [self.id, pp, self.type, self.live]
        return Info


    #Lobby should return finished dict with data assigned for each player
    #for example: {Player: dict_tos_send_}
    def Add_Player(self, player):
        return_dict = {}
        if self.live:
            return_dict.update({player:{"Message": ["Lobby already started"]}})
        elif player.Get_Lobby() == self:
            return_dict.update({player:{"Message": ["Player already in this lobby"]}})
        elif player.Get_Lobby():
            return_dict.update({player:{"Message": ["Cant join multiple lobbies"]}})
        elif self.player_count == self.size:
            return_dict.update({player:{"Message": ["Lobby is full"]}})
        else:
            
            self.player_count += 1
            self.players.append(player)
            self.Assign_Color(player)
            player.Join_Lobby(self)
            print(f"{player} has joned a lobby {self.id}")

            for p in self.players:
                return_dict.update({p:{"Message":[f"{player.name} has joined the lobby"]}})
                return_dict[p].update({"Update_Lobby":self.Get_List()})
            return_dict[player].update({"Join_Lobby":self.id})
        print(f"Returning this: {return_dict}")
        return return_dict

    def Start(self, player):
        if player != self.host:
            return "Only host can start the game"
        elif self.player_count == self.size:
            self.live = True
            return "Starting the lobby"
        else:
            return "Lobby is not filled"
        
    #cant leave while game is on? idk 
    # 1- Cant leave while game is live.
    # 2- if host changed send additional message
    # 3- if lobby is empty, remove it (outside check)
    # 4- if player left, send to everyone and update lobby

    def Remove_Player(self, player):
        return_dict = {}
        if self.live:
            return_dict.update({player:{"Message":["Cant leave live lobby."]}})
            return return_dict
        
        self.players.remove(player)
        self.player_count -= 1
        del self.colors[player]
        player.Leave_Lobby()

        if self.players:
            message_list = [f"{player.name} has left the lobby."]

            if player == self.host:
                self.host = self.players[0]
                message_list.append(f"{self.host.name} is now a host.")
            
            for p in self.players:
                return_dict.update({p:{"Message":message_list,
                                       "Update_Lobby":self.Get_List()}})
            return return_dict
        else:
            return False





    def Other_Players(self, current_player):
        players_to_send = []
        for player in self.players:
            if current_player != player:
                players_to_send.append(player)
        return players_to_send
    
    def Assign_Color(self, player):
        taken_colors = self.colors.values()
        for color in Color:
            if color not in taken_colors:
                self.colors.update({player:color})
                break

    def Update_Game_History(self, game_update:dict):
        turn = len(self.game_history)
        self.game_history.update({turn:game_update})
        
    def Request_Game_History(self, turn):
        #returns turns from input, to the end
        part_dict = {k: self.game_history[k] for k in list(range(turn, len(self.game_history)))}
        return part_dict

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