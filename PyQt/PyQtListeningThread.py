from PyQt5.QtCore import QThread, pyqtSignal
from Assets.constants import API
import select
import socket
import json

class ListeningThread(QThread):
    signal = pyqtSignal(str)
    
    def __init__(self, Client, parent = None):
        super().__init__()
        self.Client = Client
    
    def run(self):
        while self.Client.running:
            read_sockets, write_sockets, error_sockets = select.select([self.Client.sock], [], [], 2)
            if read_sockets:
                try:
                    message = self.Client.sock.recv(self.Client.buff_size).decode(self.Client.format)
                    if not message:
                        message = json.dumps({API.Empty_Message:None})
                except socket.error as error:
                    message = json.dumps({API.Socket_Error:[error]})
                finally:
                    self.signal.emit(message)

    def stop(self):
        self.Client.running = False
        self.wait()
