from player import Player


class Game():
    def __init__(self, id):
        player1 = Player(None, 400, 350, 48, 48, 100, 725, 100, 755, "RIGHT")
        player2 = Player(None, 800, 350, 48, 48, 900, 725, 900, 755, "LEFT")
        players = [player1, player2]
        self.players = players
        self.id = id
        self.ready = False

    def connected(self):  # this will check if players have connected
        return self.ready

