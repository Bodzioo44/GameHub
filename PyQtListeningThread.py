from PyQt5.QtCore import QThread, pyqtSignal
import select
import socket

class ListeningThread(QThread):
    signal = pyqtSignal(dict)
    
    def __init__(self, Client, parent = None):
        super().__init__()
        self.Client = Client
    
    def run(self):
        while self.Client.running:
            #print("dat is working")
            read_sockets, write_sockets, error_sockets = select.select([self.Client.sock], [], [], 2)
            if read_sockets:
                try:
                    message = self.Client._receive()
                    #print(f"Sending this through signal: {message}")
                    self.signal.emit(message)
                except socket.error as error:
                    
                    print(f"BIG SOCKET ERROR DETECTED: {error}")
                    self.Client.disconnect()
