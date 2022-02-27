class Game():
    def __init__(self, id, players):
        self.players = players
        self.id = id
        self.ready = False

    def connected(self):  # this will check if players have connected
        return self.ready

