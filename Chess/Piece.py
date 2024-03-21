from Assets.constants import Player_Colors

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

    #better __str__, returns this instead of memory address
    def __repr__(self):
        return f"<{self.color.name} {self.__class__.__name__} at: {self.row}, {self.col}>"
    

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)  
        self.first_move = True
        self.en_passant_eligible = False
        
    def move(self, row, col):
        if self.en_passant_eligible:
            self.en_passant_eligible = False
        if self.first_move:
            self.first_move = False
            if abs(self.row - row) == 2:
                self.en_passant_eligible = True
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
        #horizontal for future 4_man chess
        else:
            if board.CheckSquare(self.row+1, self.col+self.direction[1], self.color) == True:
                valid_moves.append((self.row+1, self.col+self.direction[1]))
            if board.CheckSquare(self.row-1, self.col+self.direction[1], self.color) == True:
                valid_moves.append((self.row-1, self.col+self.direction[1]))

        #en passant
        if self.direction[0]: #vertical
            if board.CheckSquare(self.row, self.col-1, self.color):
                left_tile = board.Grab_Tile(self.row, self.col-1)
                if left_tile != "0" and left_tile.name() == "Pawn" and left_tile.color != self.color and left_tile.en_passant_eligible:
                    valid_moves.append((self.row+self.direction[0], self.col-1))
            if board.CheckSquare(self.row, self.col+1, self.color):
                right_tile = board.Grab_Tile(self.row, self.col+1)
                if right_tile != "0" and right_tile.name() == "Pawn" and right_tile.color != self.color and right_tile.en_passant_eligible:
                    valid_moves.append((self.row+self.direction[0], self.col+1))
        else: #horizontal #FIXME this is broken, try CheckSquare instead?
            up_tile = board.Grab_Tile(self.row-1, self.col)
            down_tile = board.Grab_Tile(self.row+1, self.col)
            if up_tile != "0" and up_tile.name() == "Pawn" and up_tile.color != self.color and up_tile.en_passant_eligible:
                valid_moves.append((self.row-1, self.col+self.direction[1]))
            if down_tile != "0" and down_tile.name() == "Pawn" and down_tile.color != self.color and down_tile.en_passant_eligible:
                valid_moves.append((self.row+1, self.col+self.direction[1]))

        valid_moves.sort()
        new_valid_moves = []
        for move in valid_moves:
            if board.check_move_validity(self, move):
                new_valid_moves.append(move)
        return new_valid_moves

    def AssignColorValues(self):
        match self.color:
            case Player_Colors.WHITE:
                self.direction = (-1, 0)
                self.img_path = 'Assets/img/white_pawn.png'
            case Player_Colors.BLACK:
                self.direction = (1, 0)
                self.img_path = 'Assets/img/black_pawn.png'
            case Player_Colors.BLUE:
                self.direction = (0, 1)
                self.img_path = 'Assets/img/blue_pawn.png'
            case Player_Colors.ORANGE:
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
            case Player_Colors.WHITE:
                self.img_path = 'Assets/img/white_rook.png'
            case Player_Colors.BLACK:
                self.img_path = 'Assets/img/black_rook.png'
            case Player_Colors.BLUE:
                self.img_path = 'Assets/img/blue_rook.png'
            case Player_Colors.ORANGE:
                self.img_path = 'Assets/img/orange_rook.png'

class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def AssignColorValues(self):
        match self.color:
            case Player_Colors.WHITE:
                self.img_path = 'Assets/img/white_bishop.png'
            case Player_Colors.BLACK:
                self.img_path = 'Assets/img/black_bishop.png'
            case Player_Colors.BLUE:
                self.img_path = 'Assets/img/blue_bishop.png'
            case Player_Colors.ORANGE:
                self.img_path = 'Assets/img/orange_bishop.png'
        
class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        
    def AssignColorValues(self):
        match self.color:
            case Player_Colors.WHITE:
                self.img_path = 'Assets/img/white_queen.png'
            case Player_Colors.BLACK:
                self.img_path = 'Assets/img/black_queen.png'
            case Player_Colors.BLUE:
                self.img_path = 'Assets/img/blue_queen.png'
            case Player_Colors.ORANGE:
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
        return new_valid_moves
    
    def AssignColorValues(self):
        match self.color:
            case Player_Colors.WHITE:
                self.img_path = 'Assets/img/white_knight.png'
            case Player_Colors.BLACK:
                self.img_path = 'Assets/img/black_knight.png'
            case Player_Colors.BLUE:
                self.img_path = 'Assets/img/blue_knight.png'
            case Player_Colors.ORANGE:
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

        #castling
        if self.first_move:
            #checks if the squares between the king and right rook are empty
            if board.CheckSquare(self.row, self.col+1, self.color) == "0" and board.CheckSquare(self.row, self.col+2, self.color) == "0":
                #checks if right rook exists and has not moved
                tile = board.Grab_Tile(self.row, 7)
                if tile != "0" and tile.name() == "Rook" and tile.first_move:
                    #checks if any of the squares between the king and right rook are in check
                    for i in range(4):
                        if board.is_square_in_check(self.row, self.col+i, self.color):
                            break
                    else:
                        valid_moves.append((self.row, self.col+3))
            #checks if the squares between the king and left rook are empty
            if board.CheckSquare(self.row, self.col-1, self.color) == "0" and board.CheckSquare(self.row, self.col-2, self.color) == "0" and board.CheckSquare(self.row, self.col-3, self.color) == "0":
                tile = board.Grab_Tile(self.row, 0)
                if tile != "0" and tile.name() == "Rook" and tile.first_move:
                    for i in range(5):
                        if board.is_square_in_check(self.row, self.col-i, self.color):
                            break
                    else:
                        valid_moves.append((self.row, self.col-4))

        valid_moves.sort()
        return valid_moves

    def AssignColorValues(self):
        match self.color:
            case Player_Colors.WHITE:
                self.img_path = 'Assets/img/white_king.png'
            case Player_Colors.BLACK:
                self.img_path = 'Assets/img/black_king.png'
            case Player_Colors.BLUE:
                self.img_path = 'Assets/img/blue_king.png'
            case Player_Colors.ORANGE:
                self.img_path = 'Assets/img/orange_king.png'
