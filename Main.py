from PyQt.PyQtMainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    