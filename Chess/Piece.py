from Assets.constants import Color
from numpy import sign

class Piece:
    img_scale = 0.75
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        
        self.AssignColorValues()
        
    #used in queen, rook, and bishop
    def ValidMoves(self, board):
        valid_moves = []
        for pos in self.directions:
            i = 1
            while True:
                if board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color) == "0": #go agane (empty square)
                    if move := board.check_move_validity(self, (self.row+pos[0]*i, self.col+pos[1]*i)):
                        valid_moves.append(move)
                    i += 1
                elif board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color) == True: #enemy piece, add and break
                    if move := board.check_move_validity(self, (self.row+pos[0]*i, self.col+pos[1]*i)):
                        valid_moves.append(move)
                    break 
                
                else: #False (friendly piece, or out of bounds) break
                    break
        valid_moves.sort()
        return valid_moves

    def calc_img_position(self, square_size):
        img_size = int(square_size * self.img_scale)
        x = (square_size * self.col) + (square_size - img_size)/2
        y = (square_size * self.row) + (square_size - img_size)/2
        return x, y

    def move(self, row, col):
        self.row = row
        self.col = col
        
    def position(self):
        return self.row, self.col
    
    def name(self):
        return self.__class__.__name__
    
    def AssignColorValues(self):
        #assign img based on class name and color?
        pass

    #better __str__, returns this instead of memory address
    def __repr__(self):
        return f"<{self.color.name} {self.__class__.__name__} at: {self.row}, {self.col}>"
    

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)  
        self.first_move = True
    def move(self, row, col):
        if self.first_move:
            self.first_move = False
        self.row = row
        self.col = col
        
        
    def ValidMoves(self, board):
        valid_moves = []
        if board.CheckSquare(self.row+self.direction[0], self.col+self.direction[1], self.color) == "0":
            valid_moves.append((self.row+self.direction[0], self.col+self.direction[1]))
        if self.first_move and board.CheckSquare(self.row+self.direction[0], self.col+self.direction[1], self.color) == "0" and board.CheckSquare(self.row+self.direction[0]*2, self.col+self.direction[1]*2, self.color) == "0":
            valid_moves.append((self.row+self.direction[0]*2, self.col+self.direction[1]*2))

        #vertical
        if self.direction[0]:
            if board.CheckSquare(self.row+self.direction[0], self.col+1, self.color) == True:
                valid_moves.append((self.row+self.direction[0], self.col+1))
            if board.CheckSquare(self.row+self.direction[0], self.col-1, self.color) == True:
                valid_moves.append((self.row+self.direction[0], self.col-1))
        #horizontal
        else:
            if board.CheckSquare(self.row+1, self.col+self.direction[1], self.color) == True:
                valid_moves.append((self.row+1, self.col+self.direction[1]))
            if board.CheckSquare(self.row-1, self.col+self.direction[1], self.color) == True:
                valid_moves.append((self.row-1, self.col+self.direction[1]))
        valid_moves.sort()
        new_valid_moves = []
        for move in valid_moves:
            if board.check_move_validity(self, move):
                new_valid_moves.append(move)
        return new_valid_moves

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.direction = (-1, 0)
                self.img_path = 'Assets/img/white_pawn.png'
            case Color.BLACK:
                self.direction = (1, 0)
                self.img_path = 'Assets/img/black_pawn.png'
            case Color.BLUE:
                self.direction = (0, 1)
                self.img_path = 'Assets/img/blue_pawn.png'
            case Color.ORANGE:
                self.direction = (0, -1)
                self.img_path = 'Assets/img/orange_pawn.png'

class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        self.first_move = True
        
    def move(self, row, col):
        if self.first_move:
            self.first_move = False
        self.row = row
        self.col = col
        

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_rook.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_rook.png'
            case Color.BLUE:
                self.img_path = 'Assets/img/blue_rook.png'
            case Color.ORANGE:
                self.img_path = 'Assets/img/orange_rook.png'

class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_bishop.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_bishop.png'
            case Color.BLUE:
                self.img_path = 'Assets/img/blue_bishop.png'
            case Color.ORANGE:
                self.img_path = 'Assets/img/orange_bishop.png'
        
class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_queen.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_queen.png'
            case Color.BLUE:
                self.img_path = 'Assets/img/blue_queen.png'
            case Color.ORANGE:
                self.img_path = 'Assets/img/orange_queen.png'
        
class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        
    def ValidMoves(self, board):
        valid_moves = []
        self.directions = [(2, 1), (1, 2), (-1, 2), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1)]
        for pos in self.directions:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) in ("0", True):
                valid_moves.append((self.row+pos[0], self.col+pos[1]))
        valid_moves.sort()
        
        #Checking if move would put king in check
        new_valid_moves = []
        for move in valid_moves:
            if board.check_move_validity(self, move):
                
                new_valid_moves.append(move)
            else:
                print(f"Removing {move} from valid moves for said piee")
        return new_valid_moves
    
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_knight.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_knight.png'
            case Color.BLUE:
                self.img_path = 'Assets/img/blue_knight.png'
            case Color.ORANGE:
                self.img_path = 'Assets/img/orange_knight.png'
                
class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first_move = True
        
    def move(self, row, col):
        if self.first_move:
            self.first_move = False
        self.row = row
        self.col = col
        
    def ValidMoves(self, board):
        valid_moves = []
        self.directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        for pos in self.directions:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) in ("0", True):
                if move := board.check_move_validity(self, (self.row+pos[0], self.col+pos[1])):
                    valid_moves.append(move)
                    
        valid_moves.sort()
        return valid_moves
    
    def is_in_check(self, board):
        #Rook and Queen check
        for pos in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            i = 1
            while True:
                match board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color):
                    case True:
                        if board.Grab_Tile(self.row+pos[0]*i, self.col+pos[1]*i).name() in ("Rook", "Queen"):
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
                match board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color):
                    
                    case True:
                        if board.Grab_Tile(self.row+pos[0]*i, self.col+pos[1]*i).name() in ("Bishop", "Queen"):
                            return True
                        else:
                            break
                    case False:
                        break
                    case "0":
                        i += 1
        #Knight check
        for pos in [(2, 1), (1, 2), (-1, 2), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1)]:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) == True:
                if board.Grab_Tile(self.row+pos[0], self.col+pos[1]).name() == "Knight":
                    return True
        #King check
        for pos in [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) == True:
                if board.Grab_Tile(self.row+pos[0], self.col+pos[1]).name() == "King":
                    return True
        #Pawn check
        for pos in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) == True:
                if board.Grab_Tile(self.row+pos[0], self.col+pos[1]).name() == "Pawn":
                    direction = board.Grab_Tile(self.row+pos[0], self.col+pos[1]).direction
                    #vertical
                    if direction[0]:
                        #print("Vertical")
                        if board.CheckSquare(self.row+direction[0]*-1, self.col+1, self.color) == True:
                            #print(f"Adding {(self.row+self.direction[0]*-1, self.col+1)} to valid moves")
                            return True
                        if board.CheckSquare(self.row+direction[0]*-1, self.col-1, self.color) == True:
                            #print(f"Adding {(self.row+self.direction[0]*-1, self.col-1)} to valid moves")
                            return True
                    #horizontal
                    else:
                        #print("Horizontal")
                        if board.CheckSquare(self.row+1, self.col+direction[1]*-1, self.color) == True:
                            return True
                        if board.CheckSquare(self.row-1, self.col+direction[1]*-1, self.color) == True:
                            return True

                
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_king.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_king.png'
            case Color.BLUE:
                self.img_path = 'Assets/img/blue_king.png'
            case Color.ORANGE:
                self.img_path = 'Assets/img/orange_king.png'
