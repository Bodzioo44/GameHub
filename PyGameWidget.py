import pygame
from PyQt5.QtWidgets import QSizePolicy, QWidget
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
        self.game = game
        
        self.screen = self.game.window
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        #catch_up_timer = QTimer(self)
        #catch_up_timer.timeout.connect(self.game_catch_up)
    #Pygame events are uselsess, we are just generating our own events based on PyQt5 events
    #this runs after the widget init, maybe disable it after the widget is no longer usefull.
    #def game_catch_up(self):
    #    while data :=



    def update_game(self):
        #print("Updating game")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_pos = event.pos.x(), event.pos.y()
                mouse_click_pos = self.game.get_mouse_pos(mouse_click_pos)
                #print(mouse_click_pos)
                if self.game.is_player_turn():
                    self.game.select(mouse_click_pos)
                else:
                    print("Not your turn")

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
        self.game.rescale_screen(new_width)
        #print(f"LALO {self.screen} with size {self.screen.get_size()}")
        #so self.game.window is not being updated, because for some reason its copied by value not reference?
        self.screen = self.game.window
        
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

