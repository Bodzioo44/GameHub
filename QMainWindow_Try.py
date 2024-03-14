# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QMainWindow_Try.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(936, 744)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 50, 821, 621))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.Chat_Tab_Widget = QtWidgets.QTabWidget(self.gridLayoutWidget)
        self.Chat_Tab_Widget.setObjectName("Chat_Tab_Widget")
        self.Global_Chat_Tab = QtWidgets.QWidget()
        self.Global_Chat_Tab.setObjectName("Global_Chat_Tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Global_Chat_Tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 211, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Global_Chat_Tab_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Global_Chat_Tab_Layout.setContentsMargins(0, 0, 0, 0)
        self.Global_Chat_Tab_Layout.setObjectName("Global_Chat_Tab_Layout")
        self.Global_Chat_Text_Edit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.Global_Chat_Text_Edit.setObjectName("Global_Chat_Text_Edit")
        self.Global_Chat_Tab_Layout.addWidget(self.Global_Chat_Text_Edit)
        self.Chat_Tab_Widget.addTab(self.Global_Chat_Tab, "")
        self.Lobby_Chat_Tab = QtWidgets.QWidget()
        self.Lobby_Chat_Tab.setObjectName("Lobby_Chat_Tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.Lobby_Chat_Tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 211, 541))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.Lobby_Chat_Tab_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.Lobby_Chat_Tab_Layout.setContentsMargins(0, 0, 0, 0)
        self.Lobby_Chat_Tab_Layout.setObjectName("Lobby_Chat_Tab_Layout")
        self.Lobby_Chat_Text_Edit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.Lobby_Chat_Text_Edit.setObjectName("Lobby_Chat_Text_Edit")
        self.Lobby_Chat_Tab_Layout.addWidget(self.Lobby_Chat_Text_Edit)
        self.Chat_Tab_Widget.addTab(self.Lobby_Chat_Tab, "")
        self.gridLayout.addWidget(self.Chat_Tab_Widget, 0, 1, 1, 1)
        self.Message_Input_Box = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Message_Input_Box.setInputMask("")
        self.Message_Input_Box.setObjectName("Message_Input_Box")
        self.gridLayout.addWidget(self.Message_Input_Box, 1, 1, 1, 1)
        self.Stacked_Widget = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.Stacked_Widget.setObjectName("Stacked_Widget")
        self.Connection_Page = QtWidgets.QWidget()
        self.Connection_Page.setObjectName("Connection_Page")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.Connection_Page)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 10, 501, 551))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.Connection_Page_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.Connection_Page_Layout.setContentsMargins(0, 0, 0, 0)
        self.Connection_Page_Layout.setObjectName("Connection_Page_Layout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Connection_Page_Layout.addItem(spacerItem)
        self.Offline_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Offline_Button.setObjectName("Offline_Button")
        self.Connection_Page_Layout.addWidget(self.Offline_Button)
        self.IP_Input_Box = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.IP_Input_Box.setObjectName("IP_Input_Box")
        self.Connection_Page_Layout.addWidget(self.IP_Input_Box)
        self.Name_Input_Box = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.Name_Input_Box.setObjectName("Name_Input_Box")
        self.Connection_Page_Layout.addWidget(self.Name_Input_Box)
        self.Online_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.Online_Button.setObjectName("Online_Button")
        self.Connection_Page_Layout.addWidget(self.Online_Button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Connection_Page_Layout.addItem(spacerItem1)
        self.Stacked_Widget.addWidget(self.Connection_Page)
        self.Lobby_List_Page = QtWidgets.QWidget()
        self.Lobby_List_Page.setObjectName("Lobby_List_Page")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.Lobby_List_Page)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 10, 561, 581))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.Lobby_List_Page_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.Lobby_List_Page_Layout.setContentsMargins(0, 0, 0, 0)
        self.Lobby_List_Page_Layout.setObjectName("Lobby_List_Page_Layout")
        self.Lobby_List_Tree_Widget = QtWidgets.QTreeWidget(self.verticalLayoutWidget_3)
        self.Lobby_List_Tree_Widget.setObjectName("Lobby_List_Tree_Widget")
        self.Lobby_List_Page_Layout.addWidget(self.Lobby_List_Tree_Widget)
        self.Lobby_List_Page_Buttons_Layout = QtWidgets.QHBoxLayout()
        self.Lobby_List_Page_Buttons_Layout.setObjectName("Lobby_List_Page_Buttons_Layout")
        self.Create_Lobby_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.Create_Lobby_Button.setObjectName("Create_Lobby_Button")
        self.Lobby_List_Page_Buttons_Layout.addWidget(self.Create_Lobby_Button)
        self.Join_Lobby_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.Join_Lobby_Button.setObjectName("Join_Lobby_Button")
        self.Lobby_List_Page_Buttons_Layout.addWidget(self.Join_Lobby_Button)
        self.Update_lobby_List_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.Update_lobby_List_Button.setObjectName("Update_lobby_List_Button")
        self.Lobby_List_Page_Buttons_Layout.addWidget(self.Update_lobby_List_Button)
        self.Lobby_List_Page_Layout.addLayout(self.Lobby_List_Page_Buttons_Layout)
        self.Stacked_Widget.addWidget(self.Lobby_List_Page)
        self.Lobby_Info_Page = QtWidgets.QWidget()
        self.Lobby_Info_Page.setObjectName("Lobby_Info_Page")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.Lobby_Info_Page)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 611, 581))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.Lobby_Info_Page_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.Lobby_Info_Page_Layout.setContentsMargins(0, 0, 0, 0)
        self.Lobby_Info_Page_Layout.setObjectName("Lobby_Info_Page_Layout")
        self.Lobby_Info_Labels_Layout = QtWidgets.QHBoxLayout()
        self.Lobby_Info_Labels_Layout.setObjectName("Lobby_Info_Labels_Layout")
        self.Lobby_ID_Label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.Lobby_ID_Label.setObjectName("Lobby_ID_Label")
        self.Lobby_Info_Labels_Layout.addWidget(self.Lobby_ID_Label)
        self.Lobby_Type_Label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.Lobby_Type_Label.setObjectName("Lobby_Type_Label")
        self.Lobby_Info_Labels_Layout.addWidget(self.Lobby_Type_Label)
        self.Lobby_Players_Label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.Lobby_Players_Label.setObjectName("Lobby_Players_Label")
        self.Lobby_Info_Labels_Layout.addWidget(self.Lobby_Players_Label)
        self.Lobby_Info_Page_Layout.addLayout(self.Lobby_Info_Labels_Layout)
        self.Lobby_Info_Tree_Widget = QtWidgets.QTreeWidget(self.verticalLayoutWidget_5)
        self.Lobby_Info_Tree_Widget.setObjectName("Lobby_Info_Tree_Widget")
        self.Lobby_Info_Page_Layout.addWidget(self.Lobby_Info_Tree_Widget)
        self.Lobby_Info_Buttons_Layput = QtWidgets.QHBoxLayout()
        self.Lobby_Info_Buttons_Layput.setObjectName("Lobby_Info_Buttons_Layput")
        self.Leave_Lobby_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.Leave_Lobby_Button.setObjectName("Leave_Lobby_Button")
        self.Lobby_Info_Buttons_Layput.addWidget(self.Leave_Lobby_Button)
        self.Start_Lobby_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.Start_Lobby_Button.setObjectName("Start_Lobby_Button")
        self.Lobby_Info_Buttons_Layput.addWidget(self.Start_Lobby_Button)
        self.Kick_Player_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.Kick_Player_Button.setObjectName("Kick_Player_Button")
        self.Lobby_Info_Buttons_Layput.addWidget(self.Kick_Player_Button)
        self.Lobby_Info_Page_Layout.addLayout(self.Lobby_Info_Buttons_Layput)
        self.Stacked_Widget.addWidget(self.Lobby_Info_Page)
        self.Game_Page = QtWidgets.QWidget()
        self.Game_Page.setObjectName("Game_Page")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.Game_Page)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 29, 591, 571))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.Game_Page_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.Game_Page_Layout.setContentsMargins(0, 0, 0, 0)
        self.Game_Page_Layout.setObjectName("Game_Page_Layout")
        self.Stacked_Widget.addWidget(self.Game_Page)
        self.gridLayout.addWidget(self.Stacked_Widget, 0, 0, 2, 1)
        self.gridLayout.setColumnStretch(0, 8)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.Chat_Tab_Widget.setCurrentIndex(0)
        self.Stacked_Widget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Chat_Tab_Widget.setTabText(self.Chat_Tab_Widget.indexOf(self.Global_Chat_Tab), _translate("MainWindow", "Global Chat"))
        self.Chat_Tab_Widget.setTabText(self.Chat_Tab_Widget.indexOf(self.Lobby_Chat_Tab), _translate("MainWindow", "Lobby Chat"))
        self.Message_Input_Box.setPlaceholderText(_translate("MainWindow", "Enter message..."))
        self.Offline_Button.setText(_translate("MainWindow", "Offline"))
        self.IP_Input_Box.setPlaceholderText(_translate("MainWindow", "Enter server ip..."))
        self.Name_Input_Box.setPlaceholderText(_translate("MainWindow", "Enter your name..."))
        self.Online_Button.setText(_translate("MainWindow", "Online"))
        self.Lobby_List_Tree_Widget.headerItem().setText(0, _translate("MainWindow", "Lobby ID"))
        self.Lobby_List_Tree_Widget.headerItem().setText(1, _translate("MainWindow", "Players"))
        self.Lobby_List_Tree_Widget.headerItem().setText(2, _translate("MainWindow", "Game Type"))
        self.Lobby_List_Tree_Widget.headerItem().setText(3, _translate("MainWindow", "Live"))
        self.Create_Lobby_Button.setText(_translate("MainWindow", "Create Lobby"))
        self.Join_Lobby_Button.setText(_translate("MainWindow", "Join Lobby"))
        self.Update_lobby_List_Button.setText(_translate("MainWindow", "Update List"))
        self.Lobby_ID_Label.setText(_translate("MainWindow", "Lobby ID:"))
        self.Lobby_Type_Label.setText(_translate("MainWindow", "Lobby Type:"))
        self.Lobby_Players_Label.setText(_translate("MainWindow", "Players:"))
        self.Lobby_Info_Tree_Widget.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.Lobby_Info_Tree_Widget.headerItem().setText(1, _translate("MainWindow", "Color"))
        self.Leave_Lobby_Button.setText(_translate("MainWindow", "Leave Lobby"))
        self.Start_Lobby_Button.setText(_translate("MainWindow", "Start Lobby"))
        self.Kick_Player_Button.setText(_translate("MainWindow", "Kick Player"))
