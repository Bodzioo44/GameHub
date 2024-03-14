import pygame
from Assets.constants import Color, Player_Colors
#from Client import Client
from Checkers.Board import Board

class Game:
    def __init__(self, size:int, Client, player_color:Player_Colors):
        self.size = size
        self.square_size = size//8

        self.Board = Board(size)
        self.Client = Client

        self.selected = None
        self.commited = None
        self.turn = Color.WHITE
        self.player_color = player_color
        self.turn_counter = 0

        self.running = True
        self.debugg = True

        pygame.init()
        pygame.font.init()

        self.my_font = pygame.font.SysFont('Comic Sans MS', size//30)
        self.window = pygame.Surface((size, size))
        self._redraw_board()

    #all the prints should be replaced with gui messages
    def select(self, pos:tuple):
        if self.commited:
            self.commit(pos)
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
                        self._highlight_squares(valid_moves)
                        print(f"Valid moves: {valid_moves}")
                    else:
                        print(f"{self.selected} has no valid moves")
                        self.selected = None
                    
            elif self.selected == current_square:
                print(f"Deselected {self.selected}")
                self._remove_highlight()
                self.selected = None
            
            elif self.selected:
                self.last_starting_position = self.selected.position()
                
                valid_short_moves = self.selected.Short_ValidMoves(self.Board)
                valid_long_moves = self.selected.Long_ValidMoves(self.Board)
                if pos in valid_short_moves:
                    self.Board.Move(self.selected, pos)
                    self._redraw_board()
                    self.change_turn()
                    self.selected = None
                elif pos in valid_long_moves:
                    Nuke_row, Nuke_col = self.Board.Get_Middle(self.selected, pos)
                    Piece_To_Nuke = self.Board.Grab_Tile(Nuke_row, Nuke_col)
                    self.Board.Remove(Piece_To_Nuke)
                    
                    if self.Board.Move(self.selected, pos):
                        self._redraw_board()
                        self.change_turn()
                        self.selected = None
                    
                    else:
                        self._redraw_board()
                        self.commited = self.selected
                        self.selected = None
                        valid_long_moves = self.commited.Long_ValidMoves(self.Board)
                        if valid_long_moves:
                            self._highlight_squares(valid_long_moves)
                            print(f"Valid moves: {valid_long_moves}")
                        else:
                            self.change_turn()
                            self.commited = None
                else:
                    print("Select correct tile")
            else:
                print("Select correct tile")
    
    def commit(self, pos:tuple):
        if pos in self.commited.Long_ValidMoves(self.Board):
            Nuke_row, Nuke_col = self.Board.Get_Middle(self.commited, pos)
            Piece_To_Nuke = self.Board.Grab_Tile(Nuke_row, Nuke_col)
            self.Board.Remove(Piece_To_Nuke)
            
            if self.Board.Move(self.commited, pos):
                self._redraw_board()
                self.change_turn()
                self.commited = None
            else:
                self._redraw_board()
                valid_long_moves = self.commited.Long_ValidMoves(self.Board)
                if valid_long_moves:
                    self._highlight_squares(valid_long_moves)
                    print(f"Valid moves: {valid_long_moves}")
                else:
                    self.change_turn()
                    self.commited = None
        else:
            print("Select correct tile")

    def is_player_turn(self) -> bool:
        if self.player_color == self.turn:
            return True
        else:
            return False

    def change_turn(self):
        self.turn_counter += 1
        if self.turn == self.player_color:
            if self.selected:
                self.last_ending_position = self.selected.position()
            elif self.commited:
                self.last_ending_position = self.commited.position()
            else:
                raise "Something went really bad, no selected or commited piece after player move"

            self.send_update()

        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    #FIXME pop items instead of matching them
    def receive_update(self, data:dict):
        for key, value in data.items():
            match key:
                case "Position":
                    row, col = value[0]
                    piece = self.Board.Grab_Tile(row, col)
                    print(piece)
                    self.Board.Move(piece, value[1])
                case "Removed":
                    for pos in value:
                        row, col = pos
                        self.Board.Remove_by_position(row, col)
                case _:
                    raise f"Invalid key inside Game_Update, somethinh went really bad!: {key}"
        self.change_turn()
        self._redraw_board()

    def send_update(self):
        removed_pieces = self.Board.Get_Removed_Pieces()
        data_dict = {"Position": (self.last_starting_position, self.last_ending_position), "Removed": removed_pieces}
        self.Client.send({"Game_Update":data_dict})

    def get_mouse_pos(self, pos:tuple) -> tuple:
        row, col = pos[1]//self.square_size, pos[0]//self.square_size
        return row, col


    """
    PYGAME SURFACE DRAWING STUFF
    """

    def rescale_screen(self, new_size:int):
        self.size = new_size
        self.square_size = new_size//8
        #self.window = pygame.Surface((new_size, new_size))
        self.window = pygame.transform.scale(self.window, (new_size, new_size))
        self._redraw_board()

    def _remove_highlight(self):
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

    def _highlight_squares(self, positions:list):
        for row, col in positions:
            pygame.draw.rect(self.window, Color.RED.value, (col*self.square_size, row*self.square_size, self.square_size, self.square_size), width=3)

    def _redraw_board(self):
        self._draw_squares()
        self._draw_pieces()
        if self.debugg:
            self._draw_numbers()

    def _draw_numbers(self):
        for row in range(8):
            for col in range(8):
                text = self.my_font.render(f"{col}, {row}", False, Color.RED.value)
                self.window.blit(text, (row*self.square_size, col*self.square_size))

    def _draw_squares(self):
        self.window.fill(Color.GREY.value)
        for row in range(8):
            for col in range(row % 2, 8, 2):
                pygame.draw.rect(self.window, Color.WHITE.value, (row*self.square_size, col *self.square_size, self.square_size, self.square_size))

    def _draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.Board.board[i][j] != "0":
                    piece = self.Board.board[i][j]
                    #deepcopy cant pickle pygame surfaces
                    img = pygame.transform.scale(pygame.image.load(piece.img_path), (piece.img_size, piece.img_size))
                    self.window.blit(img, piece.calc_img_position())