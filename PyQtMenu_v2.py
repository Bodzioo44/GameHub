from PyQt5.QtWidgets import *
from PyQtDesigner_Menu import Ui_Menu
import sys

class MainWindow(QWidget, Ui_Menu):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)


        self.Create_Lobby.clicked.connect(self.Create_Lobby_Button)
        self.Join_Lobby.clicked.connect(self.Join_Lobby_Button)
        self.Start_Lobby.clicked.connect(self.Start_Lobby_Button)
        self.Leave_Lobby.clicked.connect(self.Leave_Lobby_Button)
        self.Message_Input.returnPressed.connect(self.Message_Input_Enter)

        self.Message_History = ""
        self.Lobby_List = []


    def Join_Lobby_Button(self):
        print("we would have joined lobby (probably with passed client or something)")
    
    def Leave_Lobby_Button(self):
        print("leave lobby")
    
    def Create_Lobby_Button(self):
        lobby_dict = {'1': {'Players': ['Bodzioo'], 'Size': 2, 'Type': 'Checkers_2', 'Live': False, 'Host': 'Bodzioo'},
                      '2': {'Players': ['Bodzioo1'], 'Size': 2}
                      }
        for key, value in dict.items():
            lobby = 
            lobby_id = key

        print("Create lobby")

    def Start_Lobby_Button(self):
        print("start lobby")

    #what happens after we press enter in message input
    #this should be moved to client.recv etc
    #and this should just be sending client.send
    def Message_Input_Enter(self):
        message = self.Message_Input.text()
        if message:
            #print(f"we would have sent this: {message}")
            if self.Message_History:
                self.Message_History +=  f"\n{message}"
            else:
                self.Message_History += str(message)
            self.Message_Box.setText(self.Message_History)
            #just beautiful
            self.Message_Box.verticalScrollBar().setValue(self.Message_Box.verticalScrollBar().maximum())
            self.Message_Input.clear()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())