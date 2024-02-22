import pygame
from Assets.constants import Color
from Chess.Piece import Pawn, Rook, Knight, Bishop, King, Queen, Peon, Checkers_Queen

class Board:
    def __init__(self, window, board_pixel_size):
        self.board_pixel_size = board_pixel_size
        self.square_size = self.board_pixel_size//8
        self.window = window
        self.turn = Color.WHITE
        self.board = self.create_board()
        self.UpdateBoard()
        
    def Turn_Change(self):
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE
        
    def UpdateBoard(self):
        #TODO better updateboard to avoid flickering
        #pass squares that need to be updated
        self.draw_squares()
        self.draw_board()


    #Add highlighter remover
        

    def Highlight_Square(self, positions):
        for pos in positions:
            pygame.draw.rect(self.window, Color.RED.value, (pos[1]*self.square_size, pos[0]*self.square_size, self.square_size, self.square_size), width=3)
        pygame.display.update()

    def SelectPromotion(self, pos1, pos2):
        #TODO Promotion GUI
        color = self.board[pos1[0]][pos1[1]].color
        match int(input("select from [Queen,Knight,Bishop,Rook] 1-4")):
            case 1:
                self.board[pos2[0]][pos2[1]] = Queen(pos2[0], pos2[1], color, self.square_size)
            case 2:
                self.board[pos2[0]][pos2[1]] = Knight(pos2[0], pos2[1], color, self.square_size)
            case 3:
                self.board[pos2[0]][pos2[1]] = Bishop(pos2[0], pos2[1], color, self.square_size)
            case 4:
                self.board[pos2[0]][pos2[1]] = Rook(pos2[0], pos2[1], color, self.square_size)
        self.board[pos1[0]][pos1[1]] = "0"
        self.UpdateBoard()

    def Move(self, pos1, pos2):
        piece = self.board[pos1[0]][pos1[1]]
        if str(piece.__class__.__name__) == "Pawn":
            match piece.color:
                case Color.WHITE:
                    if pos2[0] == 0:
                        self.SelectPromotion(pos1, pos2)
                        return
                case Color.BLACK:
                    if pos2[0] == 7:
                        self.SelectPromotion(pos1, pos2)
                        return
        piece.move(pos2[0], pos2[1])
        self.board[pos2[0]][pos2[1]] = piece
        self.board[pos1[0]][pos1[1]] = "0"
        self.UpdateBoard()        
        
    def CheckSquare(self, row, col, color):
        #TODO Check for promotion, check for checkmate
        if row >= 0 and row <= 7 and col >=0 and col <= 7:
            if self.board[row][col] == "0":
                return "0"
            elif self.board[row][col] == "x":
                return False
            else:
                if self.board[row][col].color == color:
                    return False
                else:
                    return True
        else:
            return False
        
    def draw_squares(self):
        self.window.fill(Color.GREY.value)
        for row in range(8):
            for col in range(row % 2, 8, 2):
                pygame.draw.rect(self.window, Color.WHITE.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size))
                pygame.display.update()

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] not in ('x','0'):
                    piece = self.board[i][j]
                    self.window.blit(piece.img, piece.calc_img_position())
        pygame.display.update()
        
    def create_board(self):
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append('0')
        #Black Pieces
        board[0][0] = Rook(0, 0, Color.BLACK, self.square_size)
        board[0][1] = Knight(0, 1, Color.BLACK, self.square_size)
        board[0][2] = Bishop(0, 2, Color.BLACK, self.square_size)
        board[0][3] = Queen(0, 3, Color.BLACK, self.square_size)
        board[0][4] = King(0, 4, Color.BLACK, self.square_size)
        board[0][5] = Bishop(0, 5, Color.BLACK, self.square_size)
        board[0][6] = Knight(0, 6, Color.BLACK, self.square_size)
        board[0][7] = Rook(0, 7, Color.BLACK, self.square_size)
        for i in range(8):
           board[1][i] = Pawn(1, i, Color.BLACK, self.square_size)
           
        #White Pieces
        board[7][0] = Rook(7, 0, Color.WHITE, self.square_size)
        board[7][1] = Knight(7, 1, Color.WHITE, self.square_size)
        board[7][2] = Bishop(7, 2, Color.WHITE, self.square_size)
        board[7][3] = Queen(7, 3, Color.WHITE, self.square_size)
        board[7][4] = King(7, 4, Color.WHITE, self.square_size)
        board[7][5] = Bishop(7, 5, Color.WHITE, self.square_size)
        board[7][6] = Knight(7, 6, Color.WHITE, self.square_size)
        board[7][7] = Rook(7, 7, Color.WHITE, self.square_size)
        for i in range(8):
           board[6][i] = Pawn(6, i, Color.WHITE, self.square_size)
        return board
