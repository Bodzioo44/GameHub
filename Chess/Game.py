import pygame
from Assets.constants import Color
from Chess.Board import Board

import threading
from time import sleep

class Chess_Game:
    def __init__(self, board_size, mode = 8):
        self.board_size = board_size
        self.mode = mode
        self.square_size = board_size/mode

        self.running = True
        self.debugg = False

        self.selected = False
        self.turn = Color.WHITE
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        self.Chess_Board = Board(self.screen, board_size)

        
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #TODO Highlight available moves/selected square
                        row, col = self.get_mouse_position(pygame.mouse.get_pos())
                        selected_square = self.Chess_Board.board[row][col]
                        if selected_square in ("0","x") and self.selected == False:
                            print("select correct square")
                        elif self.selected == False and selected_square not in ("0","x"):
                            self.selected = selected_square
                            print("selected: ", selected_square)
                            print("Valid Moves: ", self.selected.ValidMoves(self.Chess_Board))
                        elif self.selected == selected_square:
                            print("deselected: ", selected_square)
                            self.selected = False
                        elif (row, col) in self.selected.ValidMoves(self.Chess_Board):
                            self.Chess_Board.Move(self.selected.position(), (row, col))
                            self.selected = False
                        else:
                            print("select correct square")
        pygame.quit()

    def get_mouse_position(self, pos):
        x, y = pos
        return y//(self.board_size//self.mode), x//(self.board_size//self.mode)
    
    
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

