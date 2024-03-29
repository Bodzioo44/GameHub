from PyQt5.QtWidgets import QTreeWidgetItem, QApplication, QTextEdit, QMainWindow
from PyQt.PyQtDesigner import Ui_MainWindow
from PyQt.PyGameWidget import PygameWidget
from PyQt.PyQtListeningThread import ListeningThread

import sys
import socket
from Client import Client
from Assets.constants import Game_Type, get_local_ip, read_local_data, write_local_data

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setCentralWidget(self.gridLayoutWidget)
        
        #LAYOUTS SETUP
        self.Global_Chat_Tab.setLayout(self.Global_Chat_Tab_Layout)
        self.Lobby_Chat_Tab.setLayout(self.Lobby_Chat_Tab_Layout)
        
        self.Connection_Page.setLayout(self.Connection_Page_Layout)
        self.Lobby_List_Page.setLayout(self.Lobby_List_Page_Layout)
        self.Lobby_Creation_Page.setLayout(self.Lobby_Creation_Layout)
        self.Lobby_Info_Page.setLayout(self.Lobby_Info_Page_Layout)
        self.Game_Page.setLayout(self.Game_Page_Layout)
        
        #BUTTONS SETUP
        self.Online_Button.clicked.connect(self.Online_Button_Action)
        self.Offline_Button.clicked.connect(self.Offline_Button_Action)
        self.Create_Lobby_Button.clicked.connect(self.Create_Lobby_Action)
        self.Join_Lobby_Button.clicked.connect(self.Join_Lobby_Action)
        self.Update_Lobby_List_Button.clicked.connect(self.Update_Lobby_List_Action)
        self.Exit_Lobby_Creation_Button.clicked.connect(self.Exit_Lobby_Creation_Action)
        self.Chess_2_Button.clicked.connect(self.Chess_2_Action)
        self.Chess_4_Button.clicked.connect(self.Chess_4_Action)
        self.Checkers_2_Button.clicked.connect(self.Checkers_2_Action)
        self.Leave_Lobby_Button.clicked.connect(self.Leave_Lobby_Action)
        self.Start_Lobby_Button.clicked.connect(self.Start_Lobby_Action)
        self.Kick_Player_Button.clicked.connect(self.Kick_Player_Action)
        
        #MESSAGE INPUT SETUP
        self.Message_Input_Box.returnPressed.connect(self.message_input_action)

        self.Name_Input_Box.setText("Bodzioo")
        self.IP_Input_Box.setText(get_local_ip())
        self.Client = Client(self)

        self.Stacked_Widget.setCurrentWidget(self.Connection_Page)
        #self.setFixedSize(850, 580)
        self.resize(850, 580)
        #TODO this is good shit, work on proper scaling tho (for the chat too!!)
        #TODO merge that with resizeEvent?
        #self.setSizeIncrement(85,58)
        self.setWindowTitle("Game Client")

        #TODO add a way to remember previous name and ip (somekind of logging)
        #for ip in read_local_data():
        #    self.IP_ComboBox.addItem(ip)
        #    self.IP_ComboBox.setCurrentIndex(0)
        #for name in read_local_data():
        #    self.Name_ComboBox.addItem(name)
        #    self.Name_ComboBox.setCurrentIndex(0)

    """
    PYGAME INEGRATION STUFF
    """
    #TODO ideally create the widget on init, and just change its state when needed
    #FIXME even tho widget is being redefined on each reconnect, sometimes it goes crazy (displays 2 boards at once? some surface issues?)
    #its hard to reproduce
    def start_game_widget(self, game):
        print("Creating new pygame widget!!")
        self.Game_Widget = PygameWidget(game, self)
        self.Game_Page_Layout.addWidget(self.Game_Widget)
        self.Stacked_Widget.setCurrentWidget(self.Game_Page)

    def stop_game_widget(self):
        self.Game_Widget.stop_timer()
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)

    """
    CONNECTION PAGE STUFF
    """

    def Offline_Button_Action(self):
        pass
    
    def Online_Button_Action(self):
        try:
            self.Client.connect(self.Name_Input_Box.text(), self.IP_Input_Box.text()) 
            self.thread = ListeningThread(self.Client)
            self.thread.signal.connect(self.Client.message_handler)
            self.thread.start()
            print("setting lobby list page from inside online button")
            self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)
        except socket.error as error:
            print(f"Could not connect to the server, check the address and try again. {error}")

    """
    LOBBY LIST PAGE STUFF
    """
    def Create_Lobby_Action(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_Creation_Page)
    
    def Join_Lobby_Action(self):
        if selected := self.Lobby_List_Tree_Widget.selectedItems():
            print(f"Selected lobby: {selected[0].text(0)}")
            self.Client.send({"Join_Lobby":selected[0].text(0)})
        else:
            print("No lobby selected.")
            
    def Update_Lobby_List_Action(self):
        self.Client.send({"Request_Lobbies":None})
        
        
    """
    LOBBY CREATION PAGE STUFF
    """
    #TODO again, check if this is the best way to send over the game type
    def Exit_Lobby_Creation_Action(self):
        self.Stacked_Widget.setCurrentWidget(self.Lobby_List_Page)
    def Chess_2_Action(self):
        self.Client.send({"Create_Lobby":Game_Type.Chess_2.name})
    def Chess_4_Action(self):
        self.Client.send({"Create_Lobby":Game_Type.Chess_4.name})
    def Checkers_2_Action(self):
        self.Client.send({"Create_Lobby":Game_Type.Checkers_2.name})
    
    """
    LOBBY INFO PAGE STUFF    
    """
    def Leave_Lobby_Action(self):
        self.Client.send({"Leave_Lobby":None})
        
    def Start_Lobby_Action(self):
        self.Client.send({"Start_Lobby":None})
    
    def Kick_Player_Action(self):
        if selected := self.Lobby_Info_Tree_Widget.selectedItems():
            print(f"Selected player: {selected[0].text(0)}")
            self.Client.send({"Kick_Player":selected[0].text(0)})
        else:
            print("No player selected.")
            
    
    """
    CHAT TAB WIDGET STUFF
    """
    def message_input_action(self):
        message = self.Message_Input_Box.text()
        if self.Client.running:
            if message:
                current_message_box = self.Chat_Tab_Widget.currentWidget().findChildren(QTextEdit)[0]
                self.Client.send({current_message_box.objectName():[f"{self.Client.name}: "+message]})
        else:
            print("You are not connected to the server.")
            
    #TODO add a nice flash whenever message is received
    #TODO save chat history and display it on connect?
    def update_global_chat(self, data:str):
        for message in data:
            self.Global_Chat_Text_Edit.append(message)
        self.Global_Chat_Text_Edit.verticalScrollBar().setValue(self.Global_Chat_Text_Edit.verticalScrollBar().maximum())
        self.Message_Input_Box.clear()
        
    def update_lobby_chat(self, data:str):
        for message in data:
            self.Lobby_Chat_Text_Edit.append(message)
        self.Lobby_Chat_Text_Edit.verticalScrollBar().setValue(self.Lobby_Chat_Text_Edit.verticalScrollBar().maximum())
        self.Message_Input_Box.clear()


    """
    TREE WIDGETS AND LABELS STUFF
    """
    #TODO look again into updating the list by single entires, instead of sending the whole list every time
    #TODO maybe add colors, and display players some other way
    def add_lobby_tree_item(self, data:list):
        self.Lobby_List_Tree_Widget.clear()
        for lobby_info in data:
            item = QTreeWidgetItem()
            for i, value in enumerate(lobby_info):
                item.setText(i, str(value))
            self.Lobby_List_Tree_Widget.addTopLevelItem(item)
            
    def add_lobby_info_item(self, data:list):
        self.Lobby_Info_Tree_Widget.clear()
        for player_info in data:
            item = QTreeWidgetItem()
            for i, value in enumerate(player_info):
                item.setText(i, str(value))
            self.Lobby_Info_Tree_Widget.addTopLevelItem(item)

    def set_lobby_info_label(self, data:list):
        self.Lobby_ID_Label.setText("Lobby ID: " + str(data[0]))
        self.Lobby_Type_Label.setText("Game Type: "+str(data[1]))
        self.Lobby_Players_Label.setText("Players: "+str(data[2]))
    

    """
    REDEFINING PYQT EVENTS STUFF
    """

    #FIXME Best one that worked so far.
    """
    def resizeEvent(self, event):
        newWidth = event.size().width()
        newHeight = int(newWidth / self.aspectRatio)
        if newHeight > event.size().height():  # If the calculated height is greater than the current height
            newHeight = event.size().height()  # Use the current height instead
            newWidth = int(newHeight * self.aspectRatio)  # And calculate the width based on the aspect ratio
        self.resize(newWidth, newHeight)
    """

    def closeEvent(self, event):
        print("GUI was closed...")
        if self.Client.running:
            self.Client.disconnect()
        print("Disconnected. Goodbye!")
        event.accept()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())