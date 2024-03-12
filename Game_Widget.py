from PyQt5.QtWidgets import *


class Game_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 400   #Variables used for the setting of the size of everything
        self.height = 400
        self.setGeometry(0, 0, self.width, self.height)    #Set the window size

    def setupUI(self):
        self.openGLWidget = QOpenGLWidget(self)    #Create the GLWidget
        self.openGLWidget.setGeometry(0, 0, self.width, self.height)    #Size it the same as the window.
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.width, self.height)    #Resize GL's knowledge of the window to match the physical size?
        self.openGLWidget.paintGL = self.paintGL 
