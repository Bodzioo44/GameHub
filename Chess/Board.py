import pygame
from Assets.constants import Player_Colors
from Chess.Piece import Pawn, Rook, Knight, Bishop, King, Queen
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = self.create_board()
        self.last_removed_pieces_positions = []
        
    def SelectPromotion(self, piece):
        #this should pause the game and ask the player what piece they want to promote to,
        #and later on return said piece
        pass

    #piece that we are moving, and the pos we are moving it to
    def Move(self, piece, pos):
        row, col = pos 
        Prow, Pcol = piece.position()
        tile_to_move = self.Grab_Tile(row, col)
        #castling, move rook to the king, and place the king right after the rook
        if piece.name() == "King" and tile_to_move not in  ("0", False) and tile_to_move.name() == "Rook" and tile_to_move.first_move:
            if piece.col > tile_to_move.col: #long
                self.board[row][col] = "0"
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol-1] = tile_to_move
                self.board[Prow][Pcol-2] = piece
                piece.move(Prow, Pcol-2)
                tile_to_move.move(Prow, Pcol-1)
            else: #short
                print(f"King before: {piece}, {row, col}")
                print(f"Rook before: {tile_to_move}, {Prow, Pcol}")
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol+1] = tile_to_move
                self.board[Prow][Pcol+2] = piece
                piece.move(Prow, Pcol+2)
                tile_to_move.move(Prow, Pcol+1)
        else:
            self.board[Prow][Pcol] = "0"
            piece.move(row, col)
            if piece.name() == "Pawn":
                match piece.color:
                    case Player_Colors.WHITE:
                        if row == 0:
                            piece = self.SelectPromotion(piece)
                    case Player_Colors.BLACK:
                        if row == 7:
                            piece = self.SelectPromotion(piece)
            #FIXME use this only for en passant
            #if self.board[row][col] != "0":
            #    self.last_removed_pieces_positions.append((row, col))
            self.board[row][col] = piece
        

    #for online moves
    def Get_Removed_Pieces(self):
        result = self.last_removed_pieces_positions
        self.last_removed_pieces_positions = []
        return result

    def Grab_Tile(self, row , col):
        return self.board[row][col]
    
    def create_board(self):
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append('0')
        #Black Pieces
        board[0][0] = Rook(0, 0, Player_Colors.BLACK)
        board[0][1] = Knight(0, 1, Player_Colors.BLACK)
        board[0][2] = Bishop(0, 2, Player_Colors.BLACK)
        board[0][3] = Queen(0, 3, Player_Colors.BLACK)
        board[0][4] = King(0, 4, Player_Colors.BLACK)
        self.black_king = board[0][4]
        board[0][5] = Bishop(0, 5, Player_Colors.BLACK)
        board[0][6] = Knight(0, 6, Player_Colors.BLACK)
        board[0][7] = Rook(0, 7, Player_Colors.BLACK)
        for i in range(8):
           board[1][i] = Pawn(1, i, Player_Colors.BLACK)
           
        #White Pieces
        board[7][0] = Rook(7, 0, Player_Colors.WHITE)
        board[7][1] = Knight(7, 1, Player_Colors.WHITE)
        board[7][2] = Bishop(7, 2, Player_Colors.WHITE)
        board[7][3] = Queen(7, 3, Player_Colors.WHITE)
        board[7][4] = King(7, 4, Player_Colors.WHITE)
        self.white_king = board[7][4]
        board[7][5] = Bishop(7, 5, Player_Colors.WHITE)
        board[7][6] = Knight(7, 6, Player_Colors.WHITE)
        board[7][7] = Rook(7, 7, Player_Colors.WHITE)
        for i in range(8):
           board[6][i] = Pawn(6, i, Player_Colors.WHITE)
        return board


    def check_move_validity(self, piece, pos):
        #print(f"Creating new board to check if {pos} is a valid move for {piece}")
        new_board = deepcopy(self)
        new_piece = new_board.Grab_Tile(piece.row, piece.col)
        new_board.Move(new_piece, pos)
        
        #print(f"{new_piece} moved to {pos} on new board")
        if new_piece.color == Player_Colors.WHITE:
            king = new_board.white_king
            if new_board.is_square_in_check(king.row, king.col, king.color):
                #print(f"Moving {piece} to {pos} would put white king in check")
                return False
        else:
            king = new_board.black_king
            if new_board.is_square_in_check(king.row, king.col, king.color):
                #print(f"Moving {piece} to {pos} would put black king in check")
                return False
        #print(f"Moving {piece} to {pos} is a valid move")
        return pos
    
    #TODO add another method that will check the square for checkmate, in case of castling
    
    def check_for_checkmate(self, color):
        if color == Player_Colors.WHITE:
            king = self.white_king
        else:
            king = self.black_king
        if self.is_square_in_check(king.row, king.col, king.color):
            return True
        return False
    
    def is_square_in_check(self, row, col, color):
        #Rook and Queen check
        for pos in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            i = 1
            while True:
                match self.CheckSquare(row+pos[0]*i, col+pos[1]*i, color):
                    case True:
                        if self.Grab_Tile(row+pos[0]*i, col+pos[1]*i).name() in ("Rook", "Queen"):
                            return True
                        else:
                            break
                    case False:
                        break
                    case "0":
                        i += 1
                        
        #Bishop and Queen check
        for pos in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            i = 1
            while True:
                match self.CheckSquare(row+pos[0]*i, col+pos[1]*i, color):
                    
                    case True:
                        if self.Grab_Tile(row+pos[0]*i, col+pos[1]*i).name() in ("Bishop", "Queen"):
                            return True
                        else:
                            break
                    case False:
                        break
                    case "0":
                        i += 1
        #Knight check
        for pos in [(2, 1), (1, 2), (-1, 2), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1)]:
            if self.CheckSquare(row+pos[0], col+pos[1], color) == True:
                if self.Grab_Tile(row+pos[0], col+pos[1]).name() == "Knight":
                    return True
        #King check
        for pos in [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]:
            if self.CheckSquare(row+pos[0], col+pos[1], color) == True:
                if self.Grab_Tile(row+pos[0], col+pos[1]).name() == "King":
                    return True
        #Pawn check
        for pos in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if self.CheckSquare(row+pos[0], col+pos[1], color) == True:
                if self.Grab_Tile(row+pos[0], col+pos[1]).name() == "Pawn":
                    direction = self.Grab_Tile(row+pos[0], col+pos[1]).direction
                    if direction[0]:
                        if self.CheckSquare(row+direction[0]*-1, col+1, color) == True:
                            return True
                        if self.CheckSquare(row+direction[0]*-1, col-1, color) == True:
                            return True
                    #horizontal
                    else:
                        if self.CheckSquare(row+1, col+direction[1]*-1, color) == True:
                            return True
                        if self.CheckSquare(row-1, col+direction[1]*-1, color) == True:
                            return True

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
        
    def Print_Board(self):
        for row in self.board:
            print(row)
            
            
