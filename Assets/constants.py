from enum import Enum


class Color(tuple, Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 106, 0)
    BLUE = (1, 255, 12)
    GREY = (128, 128, 128)
    RED = (255, 0 , 0)

class Game_Type(Enum):
    Chess_4 = 4
    Checkers_2 = 2
    Chess_2 = 2
    #maybe?

#def Dict_Merger(dict_list):
#    dict3 = {}
#    for dict in dict_list:
#        for key, value in dict.items():
#            if key in dict3.keys():
#                old_value = dict3[key]
#                dict3.update({key:[old_value, value]})
#            else:
#                dict3.update({key:value})
#    return dict3


#maybe use flask or django? idk later on
#from flask import Flask, jsonify

class API(Enum):
    Create_Lobby = "Create_Lobby"
    Request_Lobby = "Request_Lobby"
    
#import sqlite3
#in a future far far away....


#print(API.Create_Lobby)
    
#class CustomError(Exception): 
#    def __init__(self, message): 
#        super().__init__(message)      

"""
WIDTH, HEIGHT = 560//2, 560//2
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

x, y = 54//2, 48//2

class BlackImg(Enum):
    Rook = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_rook.png'), (x, y))
    Pawn = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_pawn.png'), (x, y))
    Bishop = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_bishop.png'), (x, y))
    Queen = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_queen.png'), (x, y))
    King = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_king.png'), (x, y))
    Knight = pygame.transform.scale(pygame.image.load('Chess/assets/img/black_knight.png'), (x, y))
    
class WhiteImg(Enum):
    Pawn = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_pawn.png'), (x, y))
    Rook = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_rook.png'), (x, y))
    Bishop = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_bishop.png'), (x, y))
    Queen = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_queen.png'), (x, y))
    King = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_king.png'), (x, y))
    Knight = pygame.transform.scale(pygame.image.load('Chess/assets/img/white_knight.png'), (x, y))

class BlueImg(Enum):
    Pawn = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_pawn.png'), (x, y))
    Rook = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_rook.png'), (x, y))
    Bishop = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_bishop.png'), (x, y))
    Queen = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_queen.png'), (x, y))
    King = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_king.png'), (x, y))
    Knight = pygame.transform.scale(pygame.image.load('Chess/assets/img/blue_knight.png'), (x, y))

class OrangeImg(Enum):
    Pawn = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_pawn.png'), (x, y))
    Rook = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_rook.png'), (x, y))
    Bishop = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_bishop.png'), (x, y))
    Queen = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_queen.png'), (x, y))
    King = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_king.png'), (x, y))
    Knight = pygame.transform.scale(pygame.image.load('Chess/assets/img/orange_knight.png'), (x, y))

"""