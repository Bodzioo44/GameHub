from Assets.constants import Color


class Lobby:
    def __init__(self, type:str, size:int, id:int):
        self.type = type
        self.size = size
        self.live = False
        self.id = id
        self.colors = {}
        
        self.players = []
        self.player_count = 0
        #self.Assign_Color(player)
        self.host = None
        #player.Join_Lobby(self)
        
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
    
    #returns list with lobby values for create lobby method
    def _get_loby_info(self) -> list:
        return [self.id, self.type, self.size, self.live]
    
    #returns list with players as a key and their color as a value
    def _get_players_info(self) -> list:
        players_info_dict = []
        for player in self.players:
            players_info_dict.append(player.get_info())
        return players_info_dict
    
    def _Add_Player(self, player):
        if not self.host:
            self.host = player
        self.player_count += 1
        self.players.append(player)
        self.Assign_Color(player)
        player.Join_Lobby(self)
        print(f"{player.name} has joined lobby {self.id}")

    def _Remove_Player(self, player):
        self.player_count -= 1
        self.players.remove(player)
        del self.colors[player]
        player.Leave_Lobby()
        print(f"{player.name} has left lobby {self.id}")

    #Lobby should return finished dict with data assigned for each player
    #for example: {Player_to_send: dict with multiple entries}
    #this should return both _player_info and _lobby_info on join_lobby, and only _player_info on update_lobby
    def Join(self, player):
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
            self._Add_Player(player)

            for p in self.players:
                return_dict.update({p:{"Message":[f"{player.name} has joined the lobby"],
                                       "Update_Lobby":self._get_players_info()}})
            return_dict[player].update({"Join_Lobby":self._get_players_info()})
        print(f"Returning this: {return_dict}")
        return return_dict
    
    #TODO Maybe move the return_dict generation in case of empty lobby here?
    def Leave(self, player):
        return_dict = {}
        if self.live:
            return_dict.update({player:{"Message":["Cant leave live lobby."]}})
            return return_dict

        self._Remove_Player(player)

        if self.players:
            message_list = [f"{player.name} has left the lobby."]

            if player == self.host:
                self.host = self.players[0]
                message_list.append(f"{self.host.name} is now a host.")
            
            for p in self.Other_Players(player):
                return_dict.update({p:{"Message":message_list,
                                       "Update_Lobby":self._get_players_info()}})
            return return_dict
        else:
            return False


    def start(self, player) -> dict:
        return_dict = {}
        if player != self.host:
            return_dict.update({player:{"Message":"Only host can start the game"}})
        elif self.player_count == self.size:
            self.live = True
            for p in self.players:
                return_dict.update({p:{"Message":f"Starting the {self.type} with id: {self.id} game as {p.color} player.",
                                       "Start_Lobby":0}})
        else:
             return_dict.update({player:{"Message":"Lobby is not filled"}})
        return return_dict


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
            self._Remove_Player(player)
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