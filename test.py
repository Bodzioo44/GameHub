from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QApplication, QTextEdit, QMainWindow
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QImage, QPainter
from QMainWindow_Try import Ui_MainWindow
import sys
import argparse
import pygame
import socket
from Client import Client
from Assets.constants import Game_Type, get_local_ip
from PyGameWidget import PygameWidget

from Checkers.Game import Game as Checkers_Game
from Checkers.Game import Game as TestGame


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.Global_Chat_Tab.setLayout(self.Global_Chat_Tab_Layout)
        self.Lobby_Chat_Tab.setLayout(self.Lobby_Chat_Tab_Layout)
        self.Connection_Page.setLayout(self.Connection_Page_Layout)
        self.Lobby_List_Page.setLayout(self.Lobby_List_Page_Layout)
        self.Lobby_Info_Page.setLayout(self.Lobby_Info_Page_Layout)
        #self.Stacked_Widget.setCurrentWidget(self.Connection_Page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())