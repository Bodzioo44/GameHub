from Assets.constants import Player_Colors, Game_Type



class Lobby:
    def __init__(self, game_type:Game_Type, id:int):
        self.type = game_type.name
        self.size = game_type.value
        self.live = False
        self.id = id
        self.colors = {}
        
        self.players = []
        self.player_count = 0
        self.host = None
        
        self.game_history = {}
        self.disconnected_players = []


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
    
    #TODO send this to everyone who join along with _get_players_info
    #or maybe merge them into one method? _get_lobby_info returns static lobby data
    #returns list with lobby values for create lobby method
    #kinda inconsistent with _get_players_info but whatever
    def _get_lobby_info(self) -> str:
        return f"ID: {self.id} Type: {self.type} Size: {self.size} Live:{self.live}"
    
    #returns list with players info also as a list [[]]
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
        self._assign_color(player)
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
                
            return_dict[player].update({"Join_Lobby":(self._get_players_info(),self._get_lobby_info())})
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
            return_dict.update({player:{"Message":["Only host can start the game"]}})
        elif self.player_count == self.size:
            self.live = True
            for p in self.players:
                return_dict.update({p:{"Message":[f"Starting the {self.type} with id: {self.id} game as {p.color.name} player."],
                                       "Start_Lobby":0}})
        else:
             return_dict.update({player:{"Message":["Lobby is not filled"]}})
        return return_dict


    def Other_Players(self, current_player):
        players_to_send = []
        for player in self.players:
            if current_player != player:
                players_to_send.append(player)
        return players_to_send
    

    #TODO later on specify available colors based on game played
    def _assign_color(self, player):
        taken_colors = self.colors.values()
        for color in Player_Colors:
            if color not in taken_colors:
                self.colors.update({player:color})
                player.color = color
                break

    def Update_Game_History(self, game_update:dict):
        turn = len(self.game_history)
        self.game_history.update({turn:game_update})
        
    def Request_Game_History(self, turn:int) -> dict:
        #returns turns from input, to the end
        part_dict = {k: self.game_history[k] for k in list(range(turn, len(self.game_history)))}
        return part_dict

    #does lobby needs to do anything with disconnected player? should sending info about disconnecting be here?
    #exit lobby whenever its not started? keep the player after the game started?
    #called by player, what to do whenever player disconnects
    def Disconnect_Player(self, player):
        return_dict = {}
        if self.live:
            #TODO LOBBBY IS LIVE AND PLAYER DISCONNECTED
            #add DC'd player to a list
            self.disconnected_players.append(player)
            #add some reconnect method that will match with disconnected players
            #add some bool anyone_can_connect to relist lobby, and maybe change self.live for lobby relisting??
            #changing self.live is not a good idea imo.
            pass
        else:
            return_dict = self.Leave(player)
        return return_dict
    
    def Reconnect_Player(self, player):
        return_dict = {}
        #no idea whats supposed to be here
        if self.live:
            #whole check if player CAN reconnect
            pass
        else:
            return_dict = self.Join(player)
        return return_dict