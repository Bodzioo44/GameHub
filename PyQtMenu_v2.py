from PyQt5.QtWidgets import *
from PyQtDesigner_Menu import Ui_Menu
import threading
import sys
from Client import Client

#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
#TODO ONLY ADD STUFF BASED ON SERVER RETURN MESSAGES
#TODO Add another stackedwidget window for connecting/reconnecting?
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

        self.lobby_index_list = []



    """
    SENDS INFO DIRECTLY TO THE SERVER BASED ON ACTION INSIDE GUI
    USING CLIENT.SEND
    """


    def Exit_From_Lobby_Creation_Button(self):
        self.Select_Game_Type_List.setCurrentItem(None)
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)

    def Chess_2_Button(self):
        self.client.Send({"Create_Lobby":("Chess_2", 2)})
        self.Stacked_Widget.setCurrentWidget(self.Lobby_Page)

    def Checkers_2_Button(self):
        self.client.Send({"Create_Lobby":("Checkers_2", 2)})
        self.Stacked_Widget.setCurrentWidget(self.Lobby_Page)
        

    def Join_Lobby_Button(self):
        print("we would have joined lobby (probably with passed client or something)")
    
    def Leave_Lobby_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)
        self.client.Send({"Leave_Lobby":0})
        #self.Lobby_Tree.takeTopLevelItem(1)
        print("leave lobby")
    

    #so the lobby description would look like this: Lobby id - 2; Player Count - (2/4);Game type - Chess; Live - True
    #idk
    def Create_Lobby_Button(self):
        self.Stacked_Widget.setCurrentWidget(self.Create_Lobby_Page)

    def Start_Lobby_Button(self):
        print("start lobby")


    def Message_Input_Enter_Button(self):
        message = self.Message_Input.text()
        if message:
            current_message_box = self.Chat_Tab.currentWidget().findChildren(QTextEdit)[0]
            if current_message_box.objectName() == "Lobby_Chat_Box":
                if not self.Stacked_Widget.currentWidget() in (self.Lobby_Page, self.Game_Page):
                    message = "Join a lobby first!"
            current_message_box.append(message)
            current_message_box.verticalScrollBar().setValue(current_message_box.verticalScrollBar().maximum())
            self.Message_Input.clear()
    




    """
    CALLED DIRECTLY FROM CLIENT.MESSAGE_HANDLER()
    EDITS GUI BASED ON SERVER RESPONSE
    """

    def Add_Lobby_Tree_Item(self, data):
        item = QTreeWidgetItem()
        for i, value in enumerate(data):
            item.setText(i, str(value))
        self.lobby_index_list.append(int(data[0]))
        self.Lobby_Tree.addTopLevelItem(item)
    
    def Remove_Lobby_Tree_Item(self, data):
        print("We would remove some shit")
        self.Lobby_Tree.takeTopLevelItem(self.lobby_index_list.index(data))




    #Add another stacked widget for assigning client (connecting/disconnecting)
    #Always pass gui while creating client
    def Assign_Client(self):
        #self.client = Client("Bodzioo", "83.22.225.247", 4444, self)
        self.client = Client("Bodzioo", '127.0.0.1', 4444, self)
        self.client.Connect()
        listening_thread = threading.Thread(target = lambda: self.client.StartListening())
        listening_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.Assign_Client()
    window.show()
    sys.exit(app.exec_())
