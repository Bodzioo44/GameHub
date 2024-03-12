from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QApplication, QTextEdit
from PyQtDesigner_Menu import Ui_Menu
from Game_Widget import Game_Widget
import threading
import sys
from Client import Client
from Assets.constants import Game_Type


class MainWindow(QWidget, Ui_Menu):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.openGLWidget = Game_Widget()

        self.Create_Lobby.clicked.connect(self.Create_Lobby_Button)
        self.Join_Lobby.clicked.connect(self.Join_Lobby_Button)
        self.Start_Lobby.clicked.connect(self.Start_Lobby_Button)
        self.Leave_Lobby.clicked.connect(self.Leave_Lobby_Button)
        self.Message_Input.returnPressed.connect(self.Message_Input_Enter_Button)
        self.Exit_From_Lobby_Creation.clicked.connect(self.Exit_From_Lobby_Creation_Button)
        self.Chess_2.clicked.connect(self.Chess_2_Button)
        self.Checkers_2.clicked.connect(self.Checkers_2_Button)
        self.Update_Lobby_List.clicked.connect(self.Update_Lobby_List_Button)
        self.Online.clicked.connect(self.Online_Mode_Button)
        self.Offline.clicked.connect(self.Offline_Mode_Button)
        self.Stacked_Widget.setCurrentWidget(self.Game_Page)

    """
    SENDS INFO DIRECTLY TO THE SERVER BASED ON ACTION INSIDE GUI
    USING CLIENT.SEND
    """

    #CONNECTION PAGE

    def Offline_Mode_Button(self):
        pass
    
    #TODO add whole connection check and message box output before switching to lobby list page widget
    def Online_Mode_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)

    #LOBBY LIST PAGE

    def Join_Lobby_Button(self):
        if selected := self.Lobby_Tree.selectedItems():
            print("Sending Join_Lobby request.")
            self.client.Send({"Join_Lobby":int(selected[0].text(0))})
        else:
            print("select a lobby first")
    
    def Create_Lobby_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Create_Lobby_Page)

    def Update_Lobby_List_Button(self):
        self.client.Send({"Request_Lobbies":0})

    #CREATE LOBBY PAGE

    def Exit_From_Lobby_Creation_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)

    def Chess_2_Button(self):
        self.client.Send({"Create_Lobby":Game_Type.Chess_2.name})

    def Checkers_2_Button(self):
        self.client.Send({"Create_Lobby":Game_Type.Checkers_2.name})


    def Leave_Lobby_Button(self):
        self.client.Send({"Leave_Lobby":0})
    

    def Start_Lobby_Button(self):
        self.client.Send({"Start_Lobby":0})
        #print("start lobby")

    #TODO add self.client check so it doesnt work in offline mode
    def Message_Input_Enter_Button(self):
        message = self.Message_Input.text()
        if message:
            current_message_box = self.Chat_Tab.currentWidget().findChildren(QTextEdit)[0]
            self.client.Send({current_message_box.objectName():[f"{self.client.name}: "+message]})

    """
    CALLED DIRECTLY FROM CLIENT.MESSAGE_HANDLER()
    EDITS GUI BASED ON SERVER RESPONSE
    """

    def Add_Lobby_Tree_Items(self, data:list):
        self.Lobby_Tree.clear()
        item = QTreeWidgetItem()
        for lobby_info in data:
            for i, value in enumerate(lobby_info):
                item.setText(i, str(value))
            self.Lobby_Tree.addTopLevelItem(item)


    def Add_Player_Info_Items(self, data:list):
        self.Player_Info_Tree.clear()
        for player_info in data:
            item = QTreeWidgetItem()
            for i, value in enumerate(player_info):
                item.setText(i, str(value))
            self.Player_Info_Tree.addTopLevelItem(item)


    #TODO this is ugly af, replace it with some kind of label (visual quality improvement)
    def Add_Lobby_Info_Label(self, data:str):
        self.Lobby_Info_Label.setText(data)


    #TODO add flashing tabs on new message (visual quality improvement)
    def Update_Global_Chat(self, data:list):
        for message in data:
            self.Global_Chat_Box.append(message)
        self.Global_Chat_Box.verticalScrollBar().setValue(self.Global_Chat_Box.verticalScrollBar().maximum())
        self.Message_Input.clear()
    
    def Update_Lobby_Chat(self, data:list):
        for message in data:
            self.Lobby_Chat_Box.append(message)
        self.Lobby_Chat_Box.verticalScrollBar().setValue(self.Lobby_Chat_Box.verticalScrollBar().maximum())
        self.Message_Input.clear()       


    def Assign_Client(self):
        #self.client = Client("Bodzioo", "83.22.224.227", 4444, self)
        if len(sys.argv) == 3:
            self.client = Client(sys.argv[1], sys.argv[2], 4444, self)
        else:
            self.client = Client("Bodzioo", '127.0.0.1', 4444, self)
        self.client.Connect()

    def closeEvent(self, event):
        print("GUI was closed, disconnecting from the server...")
        self.client.Disconnect()
        print("Disconnected. Goodbye!")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.Assign_Client()
    window.show()
    sys.exit(app.exec_())




