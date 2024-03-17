from PyQtMainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


from Chess.Game import Game
from Client import Client
from Assets.constants import Player_Colors

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    #window.Stacked_Widget.setCurrentWidget(window.Game_Page)
    #gaming = Game(800, None, Player_Colors.WHITE)
    #window.start_game_widget(gaming)
    
    app.exec_()
    