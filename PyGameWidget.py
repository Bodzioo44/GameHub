import sys
import pygame
from PyQt5.QtWidgets import QSizePolicy, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPainter

from Assets.constants import Color


#Pygame surface is running without initializing the window, and then converted to QImage
#PyQt5 Widget events are used to generate equivalent pygame events
#Can i even create this without game object? or will it try to update iself right on creation
class PygameWidget(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.screen = self.game.window
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

    def start_timer(self):
        self.timer.start(16)

    def stop_timer(self):
        self.timer.stop()

    #Pygame events are uselsess, we are just generating our own events based on PyQt5 events
    #this runs after the widget init, maybe disable it after the widget is no longer usefull.

    def update_game(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_pos = event.pos.x(), event.pos.y()
                mouse_click_pos = self.game.get_mouse_pos(mouse_click_pos)
                if self.game.is_player_turn():
                    self.game.select(mouse_click_pos)
                    self.update()
                else:
                    print("Not your turn")

    #Converts pygame surface to QImage
    def get_pygame_surface(self) -> QImage:
        image = QImage(self.screen.get_buffer(), self.screen.get_width(), self.screen.get_height(),
                       QImage.Format_RGB32)
        return image
    
    #FIXME AttributeError: 'pygame.surface.Surface' object has no attribute 'transform'
    #somehow make it only rescale on both axis
    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()
        self.game.rescale_screen(new_width)
        #self.screen.transform.scale(self.screen, (new_width, new_height))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.get_pygame_surface())

    #Hijacking the mousePressEvent to generate pygame events
    def mousePressEvent(self, event):
        pygame_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': event.button(), 'pos': event.pos()})
        pygame.event.post(pygame_event)

