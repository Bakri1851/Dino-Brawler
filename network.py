import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())  # attempt at online hosting
        self.port = 5555  # this port has to be the same as the one I used in the server file
        self.address = (self.server, self.port)
        self.p = self.connect()

    def get_player(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except:  # this will send information straight away
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
