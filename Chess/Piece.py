from Assets.constants import Color
from numpy import sign


    
class Piece:
    #TODO fix square_size/img_size (WHY IS IT WORKING?), okay, thats why
    def __init__(self, row, col, color, square_size):
        self.row = row
        self.col = col
        self.color = color
        self.img_scale = 0.75
        self.square_size = square_size
        self.img_size = self.square_size * self.img_scale
        self.AssignColorValues()
        
    def ValidMoves(self, board):
        valid_moves = []
        for pos in self.directions:
            i = 1
            while True:
                if board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color) in ("0", True):
                    valid_moves.append((self.row+pos[0]*i, self.col+pos[1]*i))
                    i += 1
                else:
                    break
        valid_moves.sort()
        return valid_moves
        
    def calc_img_position(self):
        x = (self.square_size * self.col) + (self.square_size - self.img_size)//2
        y = (self.square_size * self.row) + (self.square_size - self.img_size)//2
        return x, y

    def move(self, row, col):
        self.row = row
        self.col = col
        
    def position(self):
        return self.row, self.col

    #better __str__, returns this instead of memory address
    def __repr__(self):
        return f"<{self.color.name} {self.__class__.__name__} at: {self.row}, {self.col}>"
    

class Pawn(Piece):
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)  
        self.first_move = True
    def move(self, row, col):
        if self.first_move:
            self.first_move = False
        self.row = row
        self.col = col
        
    def ValidMoves(self, board):
        #TODO add en passant
        valid_moves = []
        match self.direction:
            case "down":
                if board.CheckSquare(self.row+1, self.col, self.color) == "0":
                    valid_moves.append((self.row+1, self.col))
                if self.first_move and board.CheckSquare(self.row+1, self.col, self.color) == "0" and board.CheckSquare(self.row+2, self.col, self.color) == "0":
                    valid_moves.append((self.row+2, self.col))
                if board.CheckSquare(self.row+1, self.col+1, self.color) == True:
                    valid_moves.append((self.row+1, self.col+1))
                if board.CheckSquare(self.row+1, self.col-1, self.color) == True:
                    valid_moves.append((self.row+1, self.col-1))
            case "up":
                if board.CheckSquare(self.row-1, self.col, self.color) == "0":
                    valid_moves.append((self.row-1, self.col))
                if self.first_move and board.CheckSquare(self.row-1, self.col, self.color) == "0" and board.CheckSquare(self.row-2, self.col, self.color) == "0":
                    valid_moves.append((self.row-2, self.col))
                if board.CheckSquare(self.row-1, self.col+1, self.color) == True:
                    valid_moves.append((self.row-1, self.col+1))
                if board.CheckSquare(self.row-1, self.col-1, self.color) == True:
                    valid_moves.append((self.row-1, self.col-1))  
        valid_moves.sort()
        return valid_moves

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.direction = "up"
                self.img_path = 'Assets/img/white_pawn.png'
            case Color.BLACK:
                self.direction = "down"
                self.img_path = 'Assets/img/black_pawn.png'
            case Color.BLUE:
                self.direction = "left"
                self.img_path = 'Assets/img/blue_pawn.png'
            case Color.ORANGE:
                self.direction = "right"
                self.img_path = 'Assets/img/orange_pawn.png'

class Rook(Piece):
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)
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
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)
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
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)
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
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)
        
    def ValidMoves(self, board):
        #TODO Check for castling
        valid_moves = []
        self.directions = [(2, 1), (1, 2), (-1, 2), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1)]
        for pos in self.directions:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) in ("0", True):
                valid_moves.append((self.row+pos[0], self.col+pos[1]))
        valid_moves.sort()
        return valid_moves
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = self.img_path = 'Assets/img/white_knight.png'
            case Color.BLACK:
                self.img_path = self.img_path = 'Assets/img/black_knight.png'
            case Color.BLUE:
                self.img_path = self.img_path = 'Assets/img/blue_knight.png'
            case Color.ORANGE:
                self.img_path = self.img_path = 'Assets/img/orange_knight.png'
                
class King(Piece):
    def __init__(self, row, col, color, img_size):
        super().__init__(row, col, color, img_size)
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
                valid_moves.append((self.row+pos[0], self.col+pos[1]))
        valid_moves.sort()
        return valid_moves
    
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = self.img_path = 'Assets/img/white_king.png'
            case Color.BLACK:
                self.img_path = self.img_path = 'Assets/img/black_king.png'
            case Color.BLUE:
                self.img_path = self.img_path = 'Assets/img/blue_king.png'
            case Color.ORANGE:
                self.img_path = self.img_path = 'Assets/img/orange_king.png'

class Peon(Piece):
    def __init__(self, row, col, color, image_size):
        super().__init__(row, col, color, image_size)
        self.first_move_this_turn = True

    #TODO replace with math.copysign
    #math.copysign(1, x) returns 1 with x's sign
    #or numpy.sign(x) returns signum
    def MiddleCheck(self, x):
        if x == 2:
            return 1
        else:
            return -1
                
    def ValidMoves(self, board):
        directions = [(2 , 2), (-2, 2), (2, -2), (-2, -2)]
        valid_short_moves = []
        valid_long_moves = []
        match self.direction:
            case "down":
                if board.CheckSquare(self.row+1, self.col+1, self.color) == "0":
                    valid_short_moves.append((self.row+1, self.col+1))
                if board.CheckSquare(self.row+1, self.col-1, self.color) == "0":
                    valid_short_moves.append((self.row+1, self.col-1))
            case "up":
                if board.CheckSquare(self.row-1, self.col+1, self.color) == "0":
                    valid_short_moves.append((self.row-1, self.col+1))
                if board.CheckSquare(self.row-1, self.col-1, self.color) == "0":
                    valid_short_moves.append((self.row-1, self.col-1))  
        #print(f"before: {valid_moves}")
        for pos in directions:
            if board.CheckSquare(self.row+pos[0], self.col+pos[1], self.color) == "0" and board.CheckSquare(self.row+self.MiddleCheck(pos[0]), self.col+self.MiddleCheck(pos[1]), self.color) == True:
                valid_long_moves.append((self.row+pos[0], self.col+pos[1]))
        #valid_moves.sort()
        #print(f"after: {valid_moves}")
        return (valid_short_moves, valid_long_moves)
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.first_move_this_turn = False

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.direction = "up"
                self.img_path = 'Assets/img/white_pawn.png'
            case Color.BLACK:
                self.direction = "down"
                self.img_path = 'Assets/img/black_pawn.png'

class Checkers_Queen(Piece):
    def __init__(self, row , col, color, image_size):
        super().__init__(row, col, color, image_size)

    def ValidMoves(self, board):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        valid_short_moves = []
        valid_long_moves = []
        for pos in directions:
            i = 1
            while True:
                #print((self.row+pos[0]*i+self.MiddleCheck(pos[0]), self.col+pos[1]*i+self.MiddleCheck(pos[1])))
                if board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color) == "0":
                    valid_short_moves.append((self.row+pos[0]*i, self.col+pos[1]*i))
                    i += 1
                elif board.CheckSquare(self.row+pos[0]*i, self.col+pos[1]*i, self.color) == True and board.CheckSquare(self.row+(pos[0]*(i+1)), self.col+(pos[1]*(i+1)), self.color) == "0":
                    #print("Did we get here?")
                    valid_long_moves.append((self.row+(pos[0]*(i+1)), self.col+(pos[1]*(i+1))))
                    i += 1
                    break
                else:
                    #print(i)
                    break
        #valid_moves.sort()
        return (valid_short_moves, valid_long_moves)
    
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_queen.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_queen.png'

