import sys

try:
    import pygame
except NameError as error:
    print(f"Pygame is not installed{error}")
    sys.exit()
    
from Assets.constants import Color
from Checkers.Board import Board
from Checkers.Bot import Bot

import threading
import json
from time import sleep
#import asyncio


#some better way of assigning players (online) is needed
class Game:
    def __init__(self, board_pixel_size: int):
        self.board_pixel_size = board_pixel_size
        self.square_size = self.board_pixel_size//8
        

        self.bot_ready = True
        
        self.running = True
        self.debugg = False
        self.timer = False
        print("Press 'D' to toggle debug mode")
        
        self.selected = None
        self.commited = None
        self.turn = Color.WHITE
        
        self.Board = Board(board_pixel_size)


    def Assign_Online_Players(self, color, client):
        self.client = client
        self.player_color = color
        self.player1 = None
        self.player2 = None
    
    def Assign_Offline_Players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

            
        
    def Receive_Update(self, data):
        #data = {(old_position, new_position):(pieces to nuke)}
        #data = 
        for key, value in data.items():
            old_position, new_position = json.loads(key)
            pieces_to_nuke = value
            for piece in pieces_to_nuke:
                self.Board.Remove(piece)
            row, col = old_position
            piece = self.Board.Grab_Tile(row, col)
            self.Board.Move(piece, new_position)
        self.Change_Turn()
        self.UpdateBoard()
            
    def Send_Update(self):
        old_position = self.Board.last_moved_piece_position_before
        new_position = self.Board.last_moved_piece_position_after
        removed_pieces = self.Board.Get_Removed_Pieces()
        message = {json.dumps((old_position, new_position)):removed_pieces}
        self.client.Send({"Game_Update":message})



    def Start(self):
        self.window = pygame.display.set_mode((self.board_pixel_size, self.board_pixel_size))
        pygame.init()
        pygame.font.init() 
        self.my_font = pygame.font.SysFont('Comic Sans MS', 20)
        pygame.display.set_caption("Checkers")
        
        self.UpdateBoard()
        self.main()


    def main(self):
        
        if self.player1 == "Bot":
            Bot1 = Bot(self.Board, Color.BLACK, 6)#, 0.8574026971964815)
        if self.player2 == "Bot":
            Bot2 = Bot(self.Board, Color.WHITE, 6)#, 0.8574026971964815)
        clock = pygame.time.Clock()
        
        while self.running:
            clock.tick(60)
            
            #winner check and displaying bot seeds
            winner = self.Board.CheckForWinner(True)
            if winner and self.turn:
                print(f"{winner.name} has won the game!")
                self.turn = None
                if self.player1 == "Bot":
                    print(f"{Color.BLACK.name} Bot random seed: {Bot1.seed}")
                if self.player2 == "Bot":
                    print(f"{Color.WHITE.name} Bot random seed: {Bot2.seed}")
            
            #Bot calculations are done in separate thread, otherwise main pygame window is laggy
            #Bot actions
            if self.turn == Color.BLACK and self.player1 == "Bot" and self.bot_ready:
                Bot_thread1 = threading.Thread(target = lambda: self.BotMove(Bot1))
                #Bot_thread1.setDaemon(True)
                Bot_thread1.start()
                self.bot_ready = False

            elif self.turn == Color.WHITE and self.player2 == "Bot" and self.bot_ready:
                Bot_thread2 = threading.Thread(target = lambda: self.BotMove(Bot2))
                #Bot_thread2.setDaemon(True)
                Bot_thread2.start()
                self.bot_ready = False

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.Board.Print_Board()
                        elif event.key == pygame.K_d:
                            if self.debugg:
                                self.debugg = False
                            else:
                                self.debugg = True
                            self.UpdateBoard()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            #if the game keeps going (self.turn != None)
                            if self.turn:
                                pos = self.get_mouse_position(pygame.mouse.get_pos())
                                #if both players are bots do nothing
                                if self.player1 == "Bot" and self.player2 == "Bot":
                                    print("Let the bots play!")
                                else:
                                    #
                                    if self.turn == self.player_color:
                                        self.Select(pos)
                                    else:
                                        print("Wait for your turn!")
                                        
                            #if the game is over (self.turn = None)
                            else:
                                print(f"Game has ended! {winner.name} has won!")
                                
        #joining bots threads
        if self.player1 == "Bot":
            print(f"Waiting for {Bot1} to finish...")
            Bot_thread1.join()
        if self.player2 == "Bot":
            print(f"Waiting for {Bot2} to finish...")
            Bot_thread2.join()
        pygame.quit()
        
        print("Game closed")

    def BotMove(self, Bot):
        #optional timer thread so bot moves always last same amount of time
        if self.timer:
            timer_thread = threading.Thread(target = sleep, args = (self.timer,))
            timer_thread.start()
        new_board = Bot.GetBotMove(self.Board)
        if new_board:
            self.Board = new_board
            self.Change_Turn()
            self.UpdateBoard()
        else:
            print(f"{Bot.main_color} can't move, {Bot.secondary_color} wins!")
            self.turn = None
        if self.timer:
            timer_thread.join()
        self.bot_ready = True

    def Change_Turn(self):
        if self.turn == self.player_color:
            self.Send_Update()
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE
        #To avoid spam in bot vs bot
        if not self.player1 == "Bot" and not self.player2 == "Bot":
            print("Turn change!")

    def Select(self, pos):
        if self.commited:
            self.Commit(pos)
        else:
            row, col = pos
            current_square = self.Board.Grab_Tile(row, col)
            if self.selected == None and current_square != "0":
                if current_square.color != self.turn:
                    print("Wrong color selected, pick again")
                else:
                    self.selected = current_square
                    print(f"Selected {self.selected}")
                    valid_moves = self.selected.ValidMoves(self.Board)
                    if valid_moves:
                        self.Highlight_Squares(valid_moves)
                        print(f"Valid moves: {valid_moves}")
                    else:
                        print(f"{self.selected} has no valid moves")
                        self.selected = None
                    
            elif self.selected == current_square:
                print(f"Deselected {self.selected}")
                self.Remove_Highlight()
                self.selected = None
            
            elif self.selected:
                valid_short_moves = self.selected.Short_ValidMoves(self.Board)
                valid_long_moves = self.selected.Long_ValidMoves(self.Board)
                if pos in valid_short_moves:
                    self.Board.Move(self.selected, pos)
                    self.UpdateBoard()
                    self.Change_Turn()
                    self.selected = None
                elif pos in valid_long_moves:
                    Nuke_row, Nuke_col = self.Board.Get_Middle(self.selected, pos)
                    Piece_To_Nuke = self.Board.Grab_Tile(Nuke_row, Nuke_col)
                    self.Board.Remove(Piece_To_Nuke)
                    
                    if self.Board.Move(self.selected, pos):
                        self.UpdateBoard()
                        self.selected = None
                        self.Change_Turn()
                    
                    else:
                        self.UpdateBoard()
                        self.commited = self.selected
                        self.selected = None
                        valid_long_moves = self.commited.Long_ValidMoves(self.Board)
                        if valid_long_moves:
                            self.Highlight_Squares(valid_long_moves)
                            print(f"Valid moves: {valid_long_moves}")
                        else:
                            self.commited = None
                            self.Change_Turn()
                else:
                    print("Select correct tile")
            else:
                print("Select correct tile")
    
    def Commit(self, pos):
        if pos in self.commited.Long_ValidMoves(self.Board):
            Nuke_row, Nuke_col = self.Board.Get_Middle(self.commited, pos)
            Piece_To_Nuke = self.Board.Grab_Tile(Nuke_row, Nuke_col)
            self.Board.Remove(Piece_To_Nuke)
            
            if self.Board.Move(self.commited, pos):
                self.UpdateBoard()
                self.commited = None
                self.Change_Turn()
            else:
                self.UpdateBoard()
                valid_long_moves = self.commited.Long_ValidMoves(self.Board)
                if valid_long_moves:
                    self.Highlight_Squares(valid_long_moves)
                    print(f"Valid moves: {valid_long_moves}")
                else:
                    self.commited = None
                    self.Change_Turn()
        else:
            print("Select correct tile")
            
    def get_mouse_position(self, pos):
        x, y = pos
        return y//(self.board_pixel_size//8), x//(self.board_pixel_size//8)
    
    def Kill(self):
        self.running = False
    


    """
    PYGAME DRAWING STUFF
    """
    #Removes all highlights
    def Remove_Highlight(self):
        for row in range(8):
            if row % 2 == 0:
                for col in range(0, 8, 2):
                    pygame.draw.rect(self.window, Color.WHITE.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size), width=3)
                for col in range(1, 8, 2):
                    pygame.draw.rect(self.window, Color.GREY.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size), width=3)
            else:
                for col in range(0, 8, 2):
                    pygame.draw.rect(self.window, Color.GREY.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size), width=3)
                for col in range(1, 8, 2):
                    pygame.draw.rect(self.window, Color.WHITE.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size), width=3)
        pygame.display.update()
        
    #Draws highligted tiles on the board
    def Highlight_Squares(self, positions):
        #print(f"Highlighting: {positions}")
        for row, col in positions:
            pygame.draw.rect(self.window, Color.RED.value, (col*self.square_size, row*self.square_size, self.square_size, self.square_size), width=3)
        pygame.display.update()
        
    #Redraws whole board
    def UpdateBoard(self):
        self.draw_squares()
        self.draw_board()
        if self.debugg:
            self.draw_numbers()
        
    #Draws empty board
    def draw_squares(self):
        self.window.fill(Color.GREY.value)
        for row in range(8):
            for col in range(row % 2, 8, 2):
                pygame.draw.rect(self.window, Color.WHITE.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size))
    
    #Draws coords for debugging
    def draw_numbers(self):
        for row in range(8):
            for col in range(8):
                text = self.my_font.render(f"{col}, {row}", False, Color.RED.value)
                self.window.blit(text, (row*self.square_size, col*self.square_size))
        pygame.display.update()

    #Draws pieces
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if self.Board.board[i][j] != "0":
                    piece = self.Board.board[i][j]
                    #deepcopy cant pickle pygame surfaces
                    img = pygame.transform.scale(pygame.image.load(piece.img_path), (piece.img_size, piece.img_size))
                    self.window.blit(img, piece.calc_img_position())
        pygame.display.update()

