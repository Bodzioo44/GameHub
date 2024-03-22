from Assets.constants import Player_Colors, Game_Type, API
from time import strftime, localtime

#Lobby actions should return finished dict with data assigned for each player
#for example: {Player to send: dict with multiple entries}
class Lobby:
    def __init__(self, game_type:Game_Type, id:int):
        self.type = game_type
        self.size = game_type.value[1]
        self.live = False
        self.id = id
        self.colors = {}
        
        self.players = []
        self.player_count = 0
        self.host = None
        
        self.game_history = {}
        self.turn = 0
        self.disconnected_players = []
    
    #TODO add disconnected players to the list 
    def Get_List(self) -> list:
        pp = []
        for player in self.players:
            pp.append(player.name)
        Info = [self.id, pp, self.type.name, self.live]
        return Info

    def _get_lobby_info(self) -> list:
        return [str(self.id), self.type.name, str(self.size)]
        #return f"ID: {self.id} Type: {self.type.name} Size: {self.size} Live:{self.live}"
    
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
        
    def Game_Update(self, data:dict, player):
        return_dict = {}
        for p in self.Other_Players(player):
            return_dict.update({p:{API.Game_Update:data}})
        return return_dict


    #this should return both _player_info and _lobby_info on join_lobby, and only _player_info on update_lobby
    def Join(self, player):
        return_dict = {}
        if self.live:
            return_dict.update({player:{API.Message: ["Lobby already started"]}})
        elif player.Get_Lobby() == self:
            return_dict.update({player:{API.Message: ["Player already in this lobby"]}})
        elif player.Get_Lobby():
            return_dict.update({player:{API.Message: ["Cant join multiple lobbies"]}})
        elif self.player_count == self.size:
            return_dict.update({player:{API.Message: ["Lobby is full"]}})
        else:
            self._Add_Player(player)

            for p in self.players:
                return_dict.update({p:{API.Message:[f"{player.name} has joined the lobby"],
                                       API.Update_Lobby:self._get_players_info()}})
                
            return_dict[player].update({API.Join_Lobby:(self._get_players_info(),self._get_lobby_info())})
        #print(f"Returning this: {return_dict}")
        return return_dict

    #TODO Maybe move the return_dict generation in case of empty lobby here?
    def Leave(self, player):
        return_dict = {
            "Remove_Lobby":False}
        if self.live:
            return_dict.update({player:{API.Message:["Cant leave live lobby."]}})
            return return_dict

        self._Remove_Player(player)

        if self.players:
            message_list = [f"{player.name} has left the lobby."]

            if player == self.host:
                self.host = self.players[0]
                message_list.append(f"{self.host.name} is now a host.")
            
            for p in self.Other_Players(player):
                return_dict.update({p:{API.Message:message_list,
                                       API.Update_Lobby:self._get_players_info()}})
        else:
            return_dict.update({"Remove_Lobby":True})
        return return_dict

    #this handles ALL disconnects.
    #1. Removes player in all cases.
    #2. if there are no players left, removes lobby.
    #3. checks if lobby was live, if so, adds player to disconnected list and assigns lobby to player
    #4 
    #2. Checks if lobby was live.
    #3 if live, adds player to disconnected list and assigns lobby to player
    def Disconnect_Player(self, player):
        return_dict = {
            "Disconnect_Player":False,
            "Remove_Lobby":False}
        self._Remove_Player(player)

        if self.players:
            if self.live: #only if there are players left and lobby was live
                return_dict.update({"Disconnect_Player":True})
                self.disconnected_players.append(player)
                player.lobby = self
                
            for p in self.players:
                return_dict.update({p:{API.Message:[f"{player.name} has disconnected."],#}})
                                       API.Update_Lobby:self._get_players_info()}})

        #if the player was last player inside lobby, remove the lobby, and disconnect any other players.
        else:
            return_dict.update({"Remove_Lobby":True})
            
        return return_dict
    
    #reconnect only occurs with live games, so that else is kinda uselses
    def Reconnect_Player(self, player):
        
        return_dict = {}
        for p in self.Other_Players(player):
            return_dict.update({p:{API.Message:[f"{player.name} has reconnected."]}})
        self._Add_Player(player)
        self.disconnected_players.remove(player)
        current_time = strftime("%H:%M:%S", localtime())
        return_dict.update({player:{API.Message:[f"Reconnected to the lobby {self.id}.", f"Sucesfully reconnected to the server as {player.name} at {current_time}"],
                                    API.Start_Lobby:(self.type.name, player.color.name),
                                    API.Request_Game_History:self.Request_Game_History(1)}})
        return return_dict
    
    def start(self, player) -> dict:
        return_dict = {}
        if player != self.host:
            return_dict.update({player:{API.Message:["Only host can start the game"]}})
        elif self.player_count == self.size:
            self.live = True
            for p in self.players:
                return_dict.update({p:{API.Message:[f"Starting the {self.type} with id: {self.id} game as {p.color.name} player."],
                                       API.Start_Lobby:(self.type.name, p.color.name)}})
        else:
             return_dict.update({player:{API.Message:["Lobby is not filled"]}})
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
        self.turn += 1
        self.game_history.update({self.turn:game_update})
        print(f"Adding entry to game history: {game_update}")
        
    #TODO this might be better to send in parts, message might get too big for sockets, or pickle it and send it as a whole
    def Request_Game_History(self, turn:int) -> dict:
        #returns turns from input, to the end
        #print(f"Whole game history: {self.game_history}")
        part_dict = {k: self.game_history[k] for k in list(range(turn, len(self.game_history)+1))}
        return part_dict
    
    def Kick_Disconnected_Players(self):
        for p in self.disconnected_players:
            pass
