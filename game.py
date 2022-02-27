class Game():
    def __init__(self, id):
        self.id = id
        self.ready = False

    def connected(self):  # this will check if players have connected
        return self.ready

