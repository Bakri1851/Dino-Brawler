from player import Player
import random


class Game():
    def __init__(self, id):
        player1 = Player(400, 350, 48, 48, 100, 725, 100, 755, "RIGHT")
        player2 = Player(800, 350, 48, 48, 900, 725, 900, 755, "LEFT")
        players = [player1, player2]
        self.players = players
        self.id = id
        self.map_for_game = None
        self.map_been_decided = False

    def world_vote(self):
        if self.players[0].chosen_map == self.players[1].chosen_map:
            self.map_for_game = self.players[0].chosen_map

        else:
            self.map_for_game = random.choice([self.players[0].chosen_map, self.players[1].chosen_map])
        self.players[0].decided_map = self.map_for_game
        self.players[1].decided_map = self.map_for_game
