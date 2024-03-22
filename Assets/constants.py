from enum import Enum, auto
import socket
import sys
import os

#import sqlite3
#con = sqlite3.connect("tutorial.db")

"""
def get_local_data():
    if os.path.isfile("local_data.txt"):
        with open("local_data.txt", "r") as f:
            data = f.read().splitlines()
            print(data)
    else:
        open("local_data.txt", "w").close()

def write_local_data(data):
    file = open("local_data.txt", "a")

    data = file.read().splitlines()
    print(data)

    if len(file.read().splitlines()) > 5:
        pass
"""

def read_local_data():
    file = open("local_data.txt", "r")
    data = file.read().splitlines()
    file.close()
    return data
def write_local_data(data):
    with open("local_data.txt", "w") as file:
        file.writelines(data)
    file.close()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#print(get_local_ip())

#Colors are used for pygame visuals.
class Color(tuple, Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 106, 0)
    BLUE = (1, 255, 12)
    GREY = (128, 128, 128)
    RED = (255, 0 , 0)

#Player colors are used for logic, they dont even need values.
#TODO Maybe remove values?
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


class API(int, Enum):
    Create_Lobby = auto() #Server receives
    Join_Lobby = auto() #Client receives, Server receives
    Leave_Lobby = auto() #Client receives, Server receives
    Start_Lobby = auto() #Server receives
    Update_Lobby = auto() #Client receives
    
    Game_Update = auto() #Client receives, Server receives
    
    Request_Lobbies = auto() #Client receives
    Request_Game_History = auto() #Client receives, Server receives

    Message = auto() #Client receives, Server receives??????
    Global_Chat_Text_Edit = auto() #Client receives, Server receives
    Lobby_Chat_Text_Edit = auto() #Client receives, Server receives

    Ping = auto() #Client receives, Server receives
    Disconnect = auto() #Client receives, Server receives
    Connect = auto() #Move to message handler?

    Socket_Error = auto() #Client receives
    Empty_Message = auto() #Client receives

    

    
    
