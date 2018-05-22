import socket

class UpperHost:
    def __init__(self, host='192.168.1.103', port=5555):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        
    def read(self):
        data = self.sock.recv(1024).decode()
        return data
    
    def send(self, message):
        try:
            self.sock.send(message.encode())
            return True
        except:
            return False
