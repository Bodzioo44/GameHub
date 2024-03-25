from Assets.constants import Player_Colors
from Chess.Piece import Pawn, Rook, Knight, Bishop, King, Queen
from copy import deepcopy

class Board:
    def __init__(self):
        self.moves = []
        self.white_pieces = []
        self.black_pieces = []
        self.board = self.create_board()
        
    def add_piece(self, piece):
        print(f"Adding {piece} to the board")
        match piece.color:
            case Player_Colors.WHITE:
                self.white_pieces.append(piece)
            case Player_Colors.BLACK:
                self.black_pieces.append(piece)
        
    def nuke_tile(self, row, col):
        if self.board[row][col] != "0":
            piece = self.board[row][col]
            print(piece)
            print(self.white_pieces)
            match piece.color:
                case Player_Colors.WHITE:
                    self.black_pieces.remove(piece)
                case Player_Colors.BLACK:
                    self.white_pieces.remove(piece)
            print(f"Removing {piece} from the board")
        self.board[row][col] = "0"
        
    def game_end_check(self, color:Player_Colors):
        match color:
            case Player_Colors.WHITE:
                for piece in self.white_pieces:
                    if piece.ValidMoves(self):
                        return False
                if self.check_for_checkmate(color):
                    return "Checkmate"
                return "Draw"
            case Player_Colors.BLACK:
                for piece in self.black_pieces:
                    if piece.ValidMoves(self):
                        return False
                if self.check_for_checkmate(color):
                    return "Checkmate"
                return "Draw"

    def select_promotion(self, row, col, piece, save_moves = True):
        match piece:
            case "Queen":
                new_piece = Queen(row, col, self.Grab_Tile(row, col).color)
            case "Rook":
                new_piece = Rook(row, col, self.Grab_Tile(row, col).color)
            case "Bishop":
                new_piece = Bishop(row, col, self.Grab_Tile(row, col).color)
            case "Knight":
                new_piece = Knight(row, col, self.Grab_Tile(row, col).color)
        self.nuke_tile(row, col)
        self.add_piece(new_piece)
        self.board[row][col] = new_piece
        if save_moves:
            self.moves.append({"Promote": ((row, col), piece)})

    def check_for_promotion(self):
        for i in range(8):
            black_tile = self.Grab_Tile(0,i)
            if black_tile != "0" and black_tile.name() == "Pawn" and black_tile.color == Player_Colors.WHITE:
                return (0, i)
            white_tile = self.Grab_Tile(7,i)
            if white_tile != "0" and white_tile.name() == "Pawn" and white_tile.color == Player_Colors.BLACK:
                return (7, i)
        return False

    def Move(self, piece, pos:tuple[int, int], save_moves = True):
        row, col = pos 
        Prow, Pcol = piece.position()
        tile_to_move = self.Grab_Tile(row, col)

        #castling
        if piece.name() == "King" and tile_to_move not in ("0", False) and tile_to_move.name() == "Rook" and tile_to_move.first_move:
            if piece.col > tile_to_move.col: #long
                self.board[row][col] = "0"
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol-1] = tile_to_move
                self.board[Prow][Pcol-2] = piece
                piece.move(Prow, Pcol-2)
                tile_to_move.move(Prow, Pcol-1)
                if save_moves:
                    self.moves.append({"Move":((Prow, Pcol), (Prow, Pcol-2))})
                    self.moves.append({"Move":((row, col), (Prow, Pcol-1))})
            else: #short
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol] = "0"
                self.board[Prow][Pcol+1] = tile_to_move
                self.board[Prow][Pcol+2] = piece
                piece.move(Prow, Pcol+2)
                tile_to_move.move(Prow, Pcol+1)
                if save_moves:
                    self.moves.append({"Move":((Prow, Pcol), (Prow, Pcol+2))})
                    self.moves.append({"Move":((row, col), (Prow, Pcol+1))})
        #en passant
        elif piece.name() == "Pawn" and tile_to_move == "0" and Pcol != col:
            self.board[Prow][Pcol] = "0"
            self.board[row][col] = piece
            self.nuke_tile(Prow, col)
            #self.board[Prow][col] = "0"
            piece.move(row, col)
            if save_moves:
                self.moves.append({"Move":((Prow, Pcol), (row, col))})
                self.moves.append({"Remove":((Prow, col))})
        #normal move
        else:
            self.board[Prow][Pcol] = "0"
            piece.move(row, col)
            self.nuke_tile(row, col)
            self.board[row][col] = piece
            if save_moves:
                self.moves.append({"Move":((Prow, Pcol), (row, col))})

    #returns all the moves that have been made by the player since the last time this function was called
    def get_moves(self):
        temp = self.moves
        self.moves = []
        return temp
 
    #checks if move would put the king in check
    def check_move_validity(self, piece, pos):
        new_board = deepcopy(self)
        new_piece = new_board.Grab_Tile(piece.row, piece.col)
        new_board.Move(new_piece, pos)
        if new_piece.color == Player_Colors.WHITE:
            king = new_board.white_king
            if new_board.is_square_in_check(king.row, king.col, king.color):
                return False
        else:
            king = new_board.black_king
            if new_board.is_square_in_check(king.row, king.col, king.color):
                return False
        return pos
    
    #checks if the king is in checkmate
    def check_for_checkmate(self, color):
        if color == Player_Colors.WHITE:
            king = self.white_king
        else:
            king = self.black_king
        if self.is_square_in_check(king.row, king.col, king.color):
            return True
        return False
    
    
    #checks if square is in check
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

    #returns True if the square is occupied by an enemy, False if it is occupied by an ally or out of bound, and "0" if it is empty
    def CheckSquare(self, row, col, color):
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

    def Grab_Tile(self, row , col):
        return self.board[row][col]
    
    def create_board(self):
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append('0')

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
           
        for i in range(8):
            self.white_pieces.append(board[1][i])
            self.white_pieces.append(board[0][i])

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
           
        for i in range(8):
            self.black_pieces.append(board[6][i])
            self.black_pieces.append(board[7][i])
            
        return board
   
    def Print_Board(self):
        for row in self.board:
            print(row)
            
            
