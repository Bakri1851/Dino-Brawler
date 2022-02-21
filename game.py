class Game():
    def __init__(self, id, players):
        self.players = players
        self.id = id
        self.ready = False
        # self.lives = [players[0].lives, players[1].lives]

    def connected(self):  # this will check if players have connected
        return self.ready

    '''
    def check_lives(self):
        if players[0].current_health <= 0:
            self.lives[0] -= 1

        if players[1].current_health <= 0:
            self.lives[1] -= 1

        if (players[0].current_health <= 0 and self.lives[0] <= 0) or (
                players[1].current_health <= 0 and self.lives[1] <= 0):
            self.check_winner()
    
    def check_winner(self):
        # p1 winner = 0
        # p2 winner = 1
        if self.lives[0] <= 0:
            winner = 0
        else:
            winner = 1
        return winner
    '''
