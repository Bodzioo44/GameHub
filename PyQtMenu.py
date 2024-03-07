from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
from PyQtDesigner_Menu import Ui_Menu
import threading
import sys
from Client import Client

#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
class MainWindow(QWidget, Ui_Menu):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)


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

        #Not needed since QTreeWidget is being redone every time
        #self.lobby_list = {} # lobby_id:QTreeWidgetItem
        #self.player_list = {} # player_name:QTreeWidgetItem



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
        #SENDS {"Join_Lobby":lobby_id} to the server if lobby is selected

        if selected := self.Lobby_Tree.selectedItems():
            print("Sending Join_Lobby request.")
            self.client.Send({"Join_Lobby":int(selected[0].text(0))})
        else:
            print("select a lobby first")
    
    def Create_Lobby_Button(self):
        #MOVES TO THE CREATE LOBBY PAGE
        self.Stacked_Widget.setCurrentWidget(self.Create_Lobby_Page)

    def Update_Lobby_List_Button(self):
        self.client.Send({"Request_Lobbies":0})

    #CREATE LOBBY PAGE

    def Exit_From_Lobby_Creation_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)

    def Chess_2_Button(self):
        self.client.Send({"Create_Lobby":("Chess_2", 2)})
        #self.Stacked_Widget.setCurrentWidget(self.Lobby_Page)

    def Checkers_2_Button(self):
        self.client.Send({"Create_Lobby":("Checkers_2", 2)})
        #self.Stacked_Widget.setCurrentWidget(self.Lobby_Page)


    def Leave_Lobby_Button(self):
        #self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)
        self.client.Send({"Leave_Lobby":0})
        print("Sent request to leave lobby")
    

    def Start_Lobby_Button(self):
        print("start lobby")

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

    def Add_Lobby_Tree_Items(self, data):
        self.Lobby_Tree.clear()
        print(f"Updating QTreeWidget (Lobby_Tree_) with this: {data}")
        item = QTreeWidgetItem()
        for i, value in enumerate(data):
            item.setText(i, str(value))
        self.Lobby_Tree.addTopLevelItem(item)
        #self.lobby_list.update({data[0]:item})


    def Add_Player_Info_Items(self, data):
        self.Player_Info_Tree.clear()
        print(f"Updating QTreeWidget (Player_Info_Tree) with this: {data}")
        for player_info in data:
            item = QTreeWidgetItem()
            for i, value in enumerate(player_info):
                item.setText(i, str(value))
            self.Player_Info_Tree.addTopLevelItem(item)


    #TODO add flashing tabs on new message (in the far future)
    def Update_Global_Chat(self, data):
        for message in data:
            self.Global_Chat_Box.append(message)
        self.Global_Chat_Box.verticalScrollBar().setValue(self.Global_Chat_Box.verticalScrollBar().maximum())
        self.Message_Input.clear()
    
    def Update_Lobby_Chat(self, data):
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
        listening_thread = threading.Thread(target = lambda: self.client.StartListening())
        listening_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.Assign_Client()
    window.show()
    #print("after gui closed")
    sys.exit(app.exec_())







    """
    #After data needs to be dict, and based on keys edit values
    #IDk about above, but maybe merge these 2?
    def Update_Lobby_Tree_Item(self, data):
        item = self.lobby_list[data[0]]
        for i, value in enumerate(data):
            item.setText(i, str(value))
    

    #TODO fix this finally
    def Remove_Lobby_Tree_Item(self, data):
        #self.Lobby_Tree.takeTopLevelItem(self.lobby_index_list.index(data))
        index = QModelIndex(self.Lobby_Tree).row(self.lobby_list[data])
        print(f"We would remove some shit: {index}")
        self.Lobby_Tree.takeTopLevelItem(index)
        del self.lobby_list[data]
    #TODO fuck removing items, just redo whole table on every request? YAP
    """