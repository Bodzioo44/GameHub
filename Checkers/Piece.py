from Assets.constants import Color

#TODO Remove square_size from piece class
class Piece:
    def __init__(self, row, col, color, square_size):
        self.row = row
        self.col = col
        self.color = color
        self.img_scale = 0.75
        #self.square_size = square_size
        #self.img_size = self.square_size * self.img_scale
        self.AssignColorValues()

    def calc_img_position(self, square_size, img_size):
        x = (square_size * self.col) + (square_size - img_size)/2
        y = (square_size * self.row) + (square_size - img_size)/2
        return x, y

    def move(self, row, col):
        self.row = row
        self.col = col
    def ValidMoves(self, board):
        return self.Short_ValidMoves(board) + self.Long_ValidMoves(board)

    def position(self):
        return self.row, self.col

    def name(self):
        return self.__class__.__name__

    #better __str__, returns this instead of memory address whenever function is called
    def __repr__(self):
        return f"<{self.color.name} {self.__class__.__name__} at: {self.row}, {self.col}>"
    
    def __hash__(self) -> int:
        return hash((self.row, self.col, self.color, self.__class__.__name__))
    

class Peon(Piece):
    def __init__(self, row, col, color, image_size):
        super().__init__(row, col, color, image_size)
        self.weight = 1

    def Short_ValidMoves(self, board):
        valid_short_moves = []
        match self.color:
            case Color.BLACK:
                if board.CheckSquare(self.row+1, self.col+1, self.color) == "0":
                    valid_short_moves.append((self.row+1, self.col+1))
                if board.CheckSquare(self.row+1, self.col-1, self.color) == "0":
                    valid_short_moves.append((self.row+1, self.col-1))
            case Color.WHITE:
                if board.CheckSquare(self.row-1, self.col+1, self.color) == "0":
                    valid_short_moves.append((self.row-1, self.col+1))
                if board.CheckSquare(self.row-1, self.col-1, self.color) == "0":
                    valid_short_moves.append((self.row-1, self.col-1))  
        return valid_short_moves
    
    def Long_ValidMoves(self, board):
        valid_long_moves = []
        for Mod_row, Mod_col in [(1 , 1), (-1, 1), (1, -1), (-1, -1)]:
            if board.CheckSquare(self.row + Mod_row, self.col + Mod_col, self.color) == True and board.CheckSquare(self.row + (Mod_row*2), self.col + (Mod_col*2), self.color) == "0":
                valid_long_moves.append((self.row + (Mod_row*2), self.col + (Mod_col*2)))
        return valid_long_moves
    
    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_pawn.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_pawn.png'

class Queen(Piece):
    def __init__(self, row, col, color, image_size):
        super().__init__(row, col, color, image_size)
        self.weight = 1.5
        
    def Short_ValidMoves(self, board):
        valid_short_moves = []
        for Mod_row, Mod_col in [(1 , 1), (-1, 1), (1, -1), (-1, -1)]:
            i = 1
            while True:
                if board.CheckSquare(self.row + Mod_row*i, self.col + Mod_col*i, self.color) == "0":
                    valid_short_moves.append((self.row + Mod_row*i, self.col + Mod_col*i))
                    i += 1
                else:
                    break
        return valid_short_moves
    
    def Long_ValidMoves(self, board):
        valid_long_moves = []
        for Mod_row, Mod_col in [(1 , 1), (-1, 1), (1, -1), (-1, -1)]:
            i = 1
            while True:
                if board.CheckSquare(self.row + Mod_row*i, self.col + Mod_col*i, self.color) == "0":
                    i += 1
                    continue
                elif board.CheckSquare(self.row + Mod_row*i, self.col + Mod_col*i, self.color) == True and board.CheckSquare(self.row + (Mod_row*(i+1)), self.col + (Mod_col*(i+1)), self.color) == "0":
                    valid_long_moves.append((self.row + (Mod_row*(i+1)), self.col + (Mod_col*(i+1))))
                    break
                else:
                    break
        return valid_long_moves

    def AssignColorValues(self):
        match self.color:
            case Color.WHITE:
                self.img_path = 'Assets/img/white_queen.png'
            case Color.BLACK:
                self.img_path = 'Assets/img/black_queen.png'
