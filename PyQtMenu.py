from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMainWindow, QStackedWidget, QApplication, QLabel
from Checkers.Game import Game as Checkers_Game

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        network_widget = NetworkWidget(self)
        network_widget.Online_button.clicked.connect(self.OnlineButton)
        network_widget.Offline_button.clicked.connect(self.OfflineButton)
        
        self.central_widget.addWidget(network_widget)
        
    def OnlineButton(self):
        print("we would switch to next Online submenu")
        online_widget = OnlineWidget(self)
        self.central_widget.addWidget(online_widget)
        self.central_widget.setCurrentWidget(online_widget)
        
    def OfflineButton(self):
        print("we would switch to next Offline submenu")
        offline_widget = OfflineWidget(self)
        offline_widget.Checkers_button.clicked.connect(self.OfflineCheckersButton)
        offline_widget.Chess_button.clicked.connect(self.OfflineChessButton)
        
        self.central_widget.addWidget(offline_widget)
        self.central_widget.setCurrentWidget(offline_widget)
    
    def OfflineCheckersButton(self):
        print("we would switch to next Offline Checker submenu")
        offline_checkers_widget = Offline_CheckersWidget(self)
        offline_checkers_widget.EvE_button.clicked.connect(self.OfflineCheckersButtonEvE)
        offline_checkers_widget.PvE_button.clicked.connect(self.OfflineCheckersButtonPvE)
        offline_checkers_widget.PvP_button.clicked.connect(self.OfflineCheckersButtonPvP)

        self.central_widget.addWidget(offline_checkers_widget)
        self.central_widget.setCurrentWidget(offline_checkers_widget)
        
    def OfflineChessButton(self):
        print("we would switch to next Offline Checker submenu")
        
    def OfflineCheckersButtonEvE(self):
        print("launching EVE checkers")
        self.close()
        
        Game = Checkers_Game(800, 4, 4)
        Game.Start()
    def OfflineCheckersButtonPvE(self):
        print("launching PVE checkers")
        self.close()
        Game = Checkers_Game(800, 4)
        Game.Start()
    def OfflineCheckersButtonPvP(self):
        print("launching PVP checkers")
        self.close()
        Game = Checkers_Game(800)
        Game.Start()



class NetworkWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.Online_button = QPushButton("Online")
        self.Offline_button = QPushButton("Offline")
        layout.addWidget(self.Online_button)
        layout.addWidget(self.Offline_button)
        self.setLayout(layout)
        
class OfflineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.Chess_button = QPushButton("Chess")
        self.Checkers_button = QPushButton("Checkers")
        layout.addWidget(self.Chess_button)
        layout.addWidget(self.Checkers_button)
        self.setLayout(layout)

class Offline_CheckersWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.EvE_button = QPushButton("EvE")
        self.PvE_button = QPushButton("PvE")
        self.PvP_button = QPushButton("PvP")
        layout.addWidget(self.EvE_button)
        layout.addWidget(self.PvE_button)
        layout.addWidget(self.PvP_button)
        self.setLayout(layout)

class OnlineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.LocalHost_button = QPushButton("127.0.0.1")
        self.LocalAddress_button = QPushButton("192.168.X.X")
        self.PublicIPAddress_button = QPushButton("Connect to public server")
        layout.addWidget(self.LocalHost_button)
        layout.addWidget(self.LocalAddress_button)
        layout.addWidget(self.PublicIPAddress_button)
        self.setLayout(layout)





if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()