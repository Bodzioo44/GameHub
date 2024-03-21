from PyQt5.QtWidgets import QTreeWidgetItem

class TreeItem(QTreeWidgetItem):
    def __init__(self, parent = None):
        super().__init__(parent)