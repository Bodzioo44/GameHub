from Checkers.Game import Game as Checkers_Game
from Chess.Game import Game as Chess_Game
from Client import Client
from Assets.constants import Color




def main():
    Game = Checkers_Game(Color.WHITE, 800, 4, 4)
    Game_Client = Client("Bodzioo", "127.0.0.1", 4444)
    Game.Assign_Online_Players(Color.WHITE, Game_Client)
    Game_Client.Assign_Game(Game)
    #we are starting the actuall game assuming that all players are ready and connected
    Game.Start()
    





if __name__ == "__main__":
    main()










"""
from Client import Client
import threading
import ctypes
import sys

#from Chess.Game import Game 
#from Chess.Game import Chess_Game
#Game1 = Chess_Game(800)
#Game1.Start()

def main():
    Client1 = Client('127.0.0.1', 4444)
    Game1 = Checkers_Game(800, 3, 3)
    try:
        Client1.Connect("Bodzioo")
    except ConnectionRefusedError:
        try:
            ctypes.windll.user32.MessageBoxW(0, "You need to start server first", "Checkers", 0)
        except:
            print("Server is offline")
        sys.exit()
    threading.Thread(target = Game1.Start, args = ()).start()

#main()
"""


#Checkers_Game(board_pixel_size, black_bot, white_bot)
#board_pixel_size - size of a pygame window
#black_bot - False by default, passing positive int will replace black player with bot with that complexity
#white_bot - False by default, passing positive int will replace white player with bot with that complexity

#for alphabeta algorithm complexity of 6 is optimal, later on moves take too long
#for minimax algorithm complexity of 4 is optimal, later on moves take too long
#default algorithm is alphabeta (can be changed inside Bot.GetBotMove)

#default row number is 3, can be changed to 2 by passing optional "False" argument while creating Board in Game.init
#coords on the board can be toggled with "d" key
#Pieces can be resized by changing Piece.img_scale inside Piece init



#Game with 2 bots with complexity of 6 (Bot vs Bot)
#Game = Checkers_Game(800, 4, 4)

#Game with black bot with complexity of 5 (Player vs Bot)
#Game = Checkers_Game(800, 5)

#Game with white bot with complexity of 4 (Player vs Bot)
#Game = Checkers_Game(800, False, 4)

#Game with 2 players (Player vs Player)
#Game = Checkers_Game(800)
