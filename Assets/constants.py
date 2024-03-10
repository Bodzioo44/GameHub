from enum import Enum


class Color(tuple, Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 106, 0)
    BLUE = (1, 255, 12)
    GREY = (128, 128, 128)
    RED = (255, 0 , 0)

class Player_Colors(tuple, Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 106, 0)
    BLUE = (1, 255, 12)


#Whats wrong with python enum? You cant even assign same value to different key.
class Game_Type(tuple, Enum):
    Chess_4 = ("Chess_4", 4)
    Checkers_2 = ("Checkers_2", 2)
    Chess_2 = ("Chess_2", 2)


#Replace API?
#maybe use flask or django? idk later on
#from flask import Flask, jsonify

#import sqlite3
#in a future far far away....



class API(Enum):
    Create_Lobby = "Create_Lobby"
    Join_Lobby = "Join_Lobby"
    Leave_Lobby = "Leave_Lobby"
    Start_Lobby = "Start_Lobby"
    
    Game_Update = "Game_Update"
    
    Request_Lobbies = "Request_Lobbies"
    Request_Game_History = "Request_Game_History"

    Message = "Message"
    Global_Chat_Box = "Global_Chat_Box"
    Lobby_Chat_Box = "Lobby_Chat_Box"

    Ping = "Ping"
    Disconnect = "Disconnect"
    Connect = "Connect"
    

    
    
