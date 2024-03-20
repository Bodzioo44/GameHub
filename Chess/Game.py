import pygame
from Assets.constants import Color, Player_Colors
from Chess.Board import Board
from Chess.Piece import Piece

class Game:
    def __init__(self, size:int, Client, player_color:Player_Colors):
        self.size = size
        self.square_size = size/8

        self.Board = Board()
        self.Client = Client

        self.selected = None
        self.turn = Player_Colors.WHITE
        self.player_color = player_color
        #self.turn_counter = 0
        
        self.running = True
        self.debugg = True

        pygame.init()
        pygame.font.init()

        self.my_font = pygame.font.SysFont('Comic Sans MS', size//45)
        self.window = pygame.Surface((size, size))
        self._redraw_board()


    def select(self, pos:tuple):
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
        #TODO! Keep valid moves!!!! (optimization thingy, no need to recalculate every time)
        elif self.selected:
            valid_moves = self.selected.ValidMoves(self.Board)
            if pos in valid_moves:
                print("moving stuff")
                self.Board.Move(self.selected, pos)
                self._redraw_board()
                print("checking if piece can be promoted")
                if pos := self.Board.check_for_promotion():
                    print(f"piece can be promoted: {pos}")
                    if piece := self.Client.gui.Game_Widget.show_promotion_box():
                        print(f"received from popupbox {piece}")
                        row, col = pos
                        self.Board.select_promotion(row, col, piece)
                        self._redraw_board()
                print("changing turn, (sending update)")
                self.change_turn()
                self.selected = None
            else:
                print(f"{pos} is not a valid move for {self.selected}")


    def is_player_turn(self) -> bool:
        if self.player_color == self.turn:
            return True
        else:
            return False

    #changes turn and sends update after every local player move
    def change_turn(self, catching_up:bool = False):
        if not catching_up and self.is_player_turn():
            self.send_update()
        if self.turn == Player_Colors.WHITE:
            self.turn = Player_Colors.BLACK
        else:
            self.turn = Player_Colors.WHITE

    def receive_update(self, data:dict, catching_up:bool = False):
        for entry in data:
            for key, value in entry.items():
                match key:
                    case "Move":
                        row, col = value[0]
                        piece = self.Board.Grab_Tile(row, col)
                        self.Board.Move(piece, value[1], False)
                    case "Remove":
                        row, col = value
                        self.Board.remove(row, col)
                    case "Promote":
                        row, col = value[0]
                        self.Board.select_promotion(row, col, value[1], False)
                    case _:
                        raise f"Invalid key inside Game_Update, something went really bad!: {key}"
        self.change_turn(catching_up)
        self._redraw_board()

    def send_update(self):
        game_data = self.Board.get_moves()
        self.Client.send({"Game_Update": game_data})

    def get_mouse_pos(self, pos:tuple[int, int]) -> tuple[int, int]:
        row, col = pos[1]//self.square_size, pos[0]//self.square_size
        return row, col
    
    
    """
    PYGAME SURFACE DRAWING STUFF
    """

    def rescale_screen(self, new_size:int):
        self.size = new_size
        self.square_size = new_size//8
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
        if self.debugg:
            self._draw_numbers()

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
                    img = pygame.transform.scale(pygame.image.load(piece.img_path), (self.square_size*Piece.img_scale, self.square_size*Piece.img_scale))
                    self.window.blit(img, piece.calc_img_position(self.square_size))
