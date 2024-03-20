import pygame
from PyQt5.QtWidgets import QSizePolicy, QWidget, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter


#Pygame surface is running without initializing the window, and then converted to QImage
#PyQt5 Widget events are used to generate equivalent pygame events
#Can i even create this without game object? or will it try to update iself right on creation
class PygameWidget(QWidget):
    def __init__(self, game, parent=None):
        
        print("Initializing PygameWidget")
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Game = game
        self.Game.debugg = False
        self.screen = self.Game.window
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        self.catch_up_timer = QTimer(self)
        self.catch_up_timer.timeout.connect(self.game_catch_up)
        self.catch_up_data = []


    def game_catch_up(self):
        if self.catch_up_data:

            data = self.catch_up_data.pop(0)
            print(f"Processing: {data}")
            self.Game.receive_update(data, True)
        else:
            self.catch_up_timer.stop()

    def show_promotion_box(self) -> str:
        promotionBox = QMessageBox(self)
        promotionBox.setWindowTitle("Promotion")
        promotionBox.setText("Select a piece to promote to")

        queenButton = promotionBox.addButton("Queen", QMessageBox.ActionRole)
        rookButton = promotionBox.addButton("Rook", QMessageBox.ActionRole)
        bishopButton = promotionBox.addButton("Bishop", QMessageBox.ActionRole)
        knightButton = promotionBox.addButton("Knight", QMessageBox.ActionRole)

        promotionBox.exec()
        if promotionBox.clickedButton() == queenButton:
            return "Queen"
        elif promotionBox.clickedButton() == rookButton:
            return "Rook"
        elif promotionBox.clickedButton() == bishopButton:
            return "Bishop"
        elif promotionBox.clickedButton() == knightButton:
            return "Knight"
        else:
            return None



    def update_game(self):
        for event in pygame.event.get():
            if not self.catch_up_timer.isActive():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click_pos = event.pos.x(), event.pos.y()
                    mouse_click_pos = self.Game.get_mouse_pos(mouse_click_pos)
                    if self.Game.is_player_turn():
                        self.Game.select(mouse_click_pos)
                    else:
                        print("Not your turn")
            else:
                print("Wait for game to finish catching up!")

        self.update()

    #Converts pygame surface to QImage
    def get_pygame_surface(self) -> QImage:
        image = QImage(self.screen.get_buffer(), self.screen.get_width(), self.screen.get_height(),
                       QImage.Format_RGB32)
        return image
    
    #FIXME AttributeError: 'pygame.surface.Surface' object has no attribute 'transform'
    #somehow make it only rescale on both axis
    def resizeEvent(self, event):
        #print("Resizing event")
        new_width = event.size().width()
        new_height = event.size().height()
        self.Game.rescale_screen(new_width)
        #print(f"LALO {self.screen} with size {self.screen.get_size()}")
        #so self.Game.window is not being updated, because for some reason its copied by value not reference?
        self.screen = self.Game.window
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.get_pygame_surface())

    #Hijacking the mousePressEvent to generate pygame events
    def mousePressEvent(self, event):
        pygame_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': event.button(), 'pos': event.pos()})
        #width = self.frameGeometry().width()
        #height = self.frameGeometry().height()
        #print(f"W: {width} H: {height}")
        #print(f"X: {event.x()} Y: {event.y()}")
        pygame.event.post(pygame_event)

