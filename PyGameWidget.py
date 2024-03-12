import sys
import pygame
from PyQt5.QtWidgets import QSizePolicy, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPainter

from Assets.constants import Color


#Pygame surface is running without initializing the window, and then converted to QImage
#PyQt5 Widget events are used to generate equivalent pygame events
class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Very nice, dont delete
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setFocusPolicy(Qt.StrongFocus)

        self.init_pygame()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)


    def init_pygame(self):
        pygame.init()
        self.screen = pygame.Surface((400, 400))


    #Pygame events are uselsess, we are just generating our own events based on PyQt5 events
    def update_game(self):

        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, Color.RED.value, (50, 50), 20)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_click_pos = event.pos
                print(self.mouse_click_pos)
                #print(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                
                print("ayoyoyo")

    #is this needed? afaik this dinamically updates the widget on timer, but we can do it manually
    def paintEvent(self, event):
        print("speeeed")
        painter = QPainter(self)
        painter.drawImage(0, 0, self.get_pygame_surface())

    #Converts pygame surface to QImage
    def get_pygame_surface(self):
        image = QImage(self.screen.get_buffer(), self.screen.get_width(), self.screen.get_height(),
                       QImage.Format_RGB32)
        return image

    #Hijacking the mousePressEvent to generate pygame events
    def mousePressEvent(self, event):
        pygame_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': event.button(), 'pos': event.pos()})
        pygame.event.post(pygame_event)

