from Assets.constants import Color
from Checkers.Piece import Peon, Queen
from numpy import sign


#TODO maybe add piece count for easier winner check?
#TODO move Get_All_Moves from Bot to here for easier winner check?

class Board:
    def __init__(self, extra_row = True):
        self.board = self.create_board(extra_row)
        
        #for online moves, imo there is no better way to do it
        #maybe add online mode check?
        self.last_removed_pieces_positions = []

    def __repr__(self):
        return f"Board with eval of {self.Evaluate(Color.BLACK)} in favor of {Color.BLACK.name}"
    
    def __hash__(self) -> int:
        final_hash = 0
        for row in self.board:
            for col in row:
                final_hash += hash(col)
        return final_hash

    def Evaluate(self, color):
        eval = 0
        for row in self.board:
            for piece in row:
                if piece != "0":
                    if piece.color == color:
                        eval += piece.weight
                    else:
                        eval -= piece.weight
        return eval

    def Get_Middle(self, piece, pos):
        Piece_row, Piece_col = piece.position()
        Jump_row, Jump_col = pos

        Del_row = Jump_row - sign(Jump_row - Piece_row)
        Del_col = Jump_col - sign(Jump_col - Piece_col)
        return (Del_row, Del_col)

    def Move(self, piece, pos):
        row, col = pos
        Prow, Pcol = piece.position()
        
        self.board[Prow][Pcol] = "0"
        if row == 0 and piece.color == Color.WHITE and piece.name() == "Peon":
            self.board[row][col] = Queen(row, col, Color.WHITE)
            return True
        elif row == 7 and piece.color == Color.BLACK and piece.name() == "Peon":
            self.board[row][col] = Queen(row, col, Color.BLACK)
            return True
        else:
            piece.move(row, col)
            self.board[row][col] = piece
            return False

    def Grab_All_Pieces(self, color):
        results = []
        for row in self.board:
            for col in row:
                if col != "0" and col.color == color:
                    results.append(col)
        return results

    #Valid moves for minimax
    def Valid_moves(self, piece):
        moves = {}
        for short_move in piece.Short_ValidMoves(self):
            moves.update({short_move:[]})
        skipped = []
        match piece.name():
            case "Peon":
                moves.update(self.Jump(piece.color, piece.position(), skipped))
            case "Queen":
                moves.update(self.Queen_Jump(piece.color, piece.position(), skipped))
        return moves
    
    #Recursive Queen moves for minimax
    def Queen_Jump(self, color, current_pos, skipped):
        Current_row, Current_col = current_pos
        moves = {}
        for Mod_row, Mod_col in [(1 , 1), (-1, 1), (1, -1), (-1, -1)]:
            i = 1
            while True:
                #Middle square
                Mrow = Current_row + (Mod_row*i)
                Mcol = Current_col + (Mod_col*i)
                #Jump Square
                Jrow = Current_row + (Mod_row*(i+1))
                Jcol = Current_col + (Mod_col*(i+1))
                if self.CheckSquare(Mrow, Mcol, color) == "0":
                    i+=1
                    continue
                elif (self.CheckSquare(Mrow, Mcol, color) == True) and (self.Grab_Tile(Mrow, Mcol) not in skipped) and (self.CheckSquare(Jrow, Jcol, color) == "0"):
                    skipped_copy = skipped.copy()
                    skipped_copy.append(self.Grab_Tile(Mrow, Mcol))
                    x = self.Queen_Jump(color, (Jrow, Jcol), skipped_copy)
                    if x == {}:
                        moves.update({(Jrow, Jcol):skipped_copy})
                    else:
                        moves.update(x)
                    break
                else:

                    break
        return moves

    #Recursive Peon moves for minimax
    def Jump(self, color, current_pos, skipped):
        Current_row, Current_col = current_pos
        moves = {}
        for pos in [(1 , 1), (-1, 1), (1, -1), (-1, -1)]:
            row, col = pos
            Drow, Dcol = Current_row + (row*2), Current_col + (col*2)
            row, col = Current_row + row, Current_col + col 
            
            if (self.CheckSquare(row, col, color) == True) and (self.Grab_Tile(row, col) not in skipped) and (self.CheckSquare(Drow, Dcol, color) == "0"):
                match color:
                    case Color.WHITE:
                        if Current_row == 0:
                            return {}
                    case Color.BLACK:
                        if Current_row == 7:
                            return {}
                skipped_copy = skipped.copy()
                skipped_copy.append(self.Grab_Tile(row, col))
                x = self.Jump(color, (Drow, Dcol), skipped_copy)
                if x == {}:
                    moves.update({(Drow, Dcol):skipped_copy})
                else:
                    moves.update(x)
        return moves

    def Grab_Tile(self, row , col):
        return self.board[row][col]

    def Remove(self, piece):
        row, col = piece.position()
        self.board[row][col] = "0"
        
        #for online moves
        self.last_removed_pieces_positions.append((row, col))
     
     
    #ONLY for removing pieces from online update
    def Remove_by_position(self, row, col):
        self.board[row][col] = "0"
    
    #for online moves
    def Get_Removed_Pieces(self):
        result = self.last_removed_pieces_positions
        self.last_removed_pieces_positions = []
        return result

    #TODO this is kinda ugly, especially since this is happening on every iteration of bot minimax
    def CheckForWinner(self, check: bool = False):
        #piece count check
        white_pieces = self.Grab_All_Pieces(Color.WHITE)
        black_pieces = self.Grab_All_Pieces(Color.BLACK)
        if white_pieces == []:
            self.winner = Color.BLACK
            return Color.BLACK
        elif black_pieces == []:
            self.winner = Color.WHITE
            return Color.WHITE
        #stalemate check
        #this should work right?
        if check:
            for piece in white_pieces:
                if piece.ValidMoves(self):
                    break
            else:
                return Color.BLACK
            
            for piece in black_pieces:
                if piece.ValidMoves(self):
                    break
            else:
                return Color.WHITE
            
            #white_moves = []
            #black_moves = []
            #for piece in white_pieces:
            #    white_moves += piece.ValidMoves(self)
            #if white_moves == []:
            #    return Color.BLACK
            #for piece in black_pieces:
            #    black_moves += piece.ValidMoves(self)
            #if black_moves == []:
            #    return Color.WHITE
        

    def create_board(self, extra_row):
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append('0')
        for i in range(4):
            board[0][i*2+1] = Peon(0, i*2+1, Color.BLACK)
            board[1][i*2] = Peon(1, i*2, Color.BLACK)
            board[7][i*2] = Peon(7, i*2, Color.WHITE)
            board[6][i*2+1] = Peon(6, i*2+1, Color.WHITE)
            if extra_row:
                board[2][i*2+1] = Peon(2, i*2+1, Color.BLACK)
                board[5][i*2] = Peon(5, i*2, Color.WHITE)
        return board

    #Checks the status of the square, "0" for free space, False for same color/invalid space, True for enemy color
    def CheckSquare(self, row, col, color):
        if row >= 0 and row <= 7 and col >=0 and col <= 7:
            if self.board[row][col] == "0":
                return "0"
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
            
            


