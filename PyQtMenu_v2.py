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
        self.Dict_Lobby_List = []


    def Join_Lobby_Button(self):
        print("we would have joined lobby (probably with passed client or something)")
    
    def Leave_Lobby_Button(self):
        #itemtoremove = self.Lobby_Tree.selectedItems()[0]
        #print(itemtoremove)
        #self.Lobby_List.takeItem(self.lobby_entry)
        #removes and returns index some way of getting index is needed
        self.Lobby_Tree.takeTopLevelItem(1)
        #self.Lobby_Tree.removeItemWidget(itemtoremove,1)
        print("leave lobby")
    

    #so the lobby description would look like this: Lobby id - 2; Player Count - (2/4);Game type - Chess; Live - True
    def Create_Lobby_Button(self):
        """
        lobby_dict = {'1': {'Players': ['Bodzioo'], 'Size': 2, 'Type': 'Checkers_2', 'Live': False, 'Host': 'Bodzioo'},
                      '2': {'Players': ['Bodzioo1'], 'Size': 2},
                      '3': 'lalo'
                      }
        for key, value in lobby_dict.items():
            lobby = QListWidgetItem(self.Lobby_List, str(key))
            self.Dict_Lobby_List.append(lobby)
        """
        dict_list = [{"Lobby_Id":1,
                      "Players": ["Bodzioo"],
                      "Type":"Chess",
                      "Live":False},
                      {"Lobby_Id":2,
                      "Players": ["Bodzioov2"],
                      "Type":"Checkers",
                      "Live":False}]


        for lobby_info in dict_list:
            item = QTreeWidgetItem()
            for i, (key, value) in enumerate(lobby_info.items()):
                #key is kinda useless, maybe send data in order in a simple list?
                item.setText(i, str(value))
            self.Lobby_Tree.addTopLevelItem(item)
        


        #self.lobby_entry = QListWidgetItem("test")
        #self.Lobby_List.addItem(self.lobby_entry)
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