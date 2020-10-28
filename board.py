import random


class Board:
    deck = ["".join([suit, str(honour)]) for suit in "CDHS" for honour in range(2, 15)]

    def __init__(self, board_id):
        self.id = board_id
        self.players = [None, None, None, None]
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.history = []
        self.shuffle()

    def shuffle(self):
        shuffle_deck = self.deck
        random.shuffle(shuffle_deck)
        self.north = sorted(shuffle_deck[:14], key=lambda x: (x[0], -int(x[1:])))
        self.south = sorted(shuffle_deck[14:27], key=lambda x: (x[0], -int(x[1:])))
        self.west = sorted(shuffle_deck[27:40], key=lambda x: (x[0], -int(x[1:])))
        self.east = sorted(shuffle_deck[40:53], key=lambda x: (x[0], -int(x[1:])))
