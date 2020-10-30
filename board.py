import random
from card import Card


class Board:
    deck = ["".join([suit, str(honour)]) for suit in "CDHS" for honour in range(2, 15)]

    def __init__(self, board_id):
        self.id = board_id
        self.players = [None, None, None, None]
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.dealer = None
        self.turn = None
        self.history = []
        self.vulnerable = [False, False, False, False]
        self.set_vulnerable()
        self.set_dealer()
        self.shuffle()

    def shuffle(self):
        shuffle_deck = self.deck
        random.shuffle(shuffle_deck)
        self.north = [Card(symbol) for symbol in sorted(shuffle_deck[:14], key=lambda x: (x[0], -int(x[1:])))]
        self.south = [Card(symbol) for symbol in sorted(shuffle_deck[14:27], key=lambda x: (x[0], -int(x[1:])))]
        self.west = [Card(symbol) for symbol in sorted(shuffle_deck[27:40], key=lambda x: (x[0], -int(x[1:])))]
        self.east = [Card(symbol) for symbol in sorted(shuffle_deck[40:53], key=lambda x: (x[0], -int(x[1:])))]

    def set_vulnerable(self):
        if self.id % 16 == 2 or self.id % 16 == 5 or self.id % 16 == 12 or self.id % 16 == 15:
            self.vulnerable = [True, False, True, False]
        elif self.id % 16 == 4 or self.id % 16 == 7 or self.id % 16 == 10 or self.id % 16 == 13:
            self.vulnerable = [True, True, True, True]
        elif self.id % 16 == 3 or self.id % 16 == 6 or self.id % 16 == 9 or self.id % 16 == 0:
            self.vulnerable = [False, True, False, True]
        else:
            self.vulnerable = [False, False, False, False]

    def set_dealer(self):
        if self.id % 4 == 1:
            self.dealer = 2
        elif self.id % 4 == 2:
            self.dealer = 3
        elif self.id % 4 == 3:
            self.dealer = 0
        else:
            self.dealer = 1
        self.turn = self.dealer

    def draw_hand(self, win, hand, seat, user=False):
        if hand == 0:
            drawing_hand = self.south
        elif hand == 1:
            drawing_hand = self.west
        elif hand == 2:
            drawing_hand = self.north
        else:
            drawing_hand = self.east

        width = (len(drawing_hand) - 1) * 30 + 100
        height = (len(drawing_hand) - 1) * 30 + 100
        vertical = False

        if seat == 0:
            x = round(win.get_width() / 2 - width / 2)
            y = 600
        elif seat == 1:
            x = 60
            y = round(win.get_height() / 2 - height / 2)
            vertical = True
        elif seat == 2:
            x = round(win.get_width() / 2 - width / 2)
            y = 150
        else:
            x = 800
            y = round(win.get_height() / 2 - height / 2)
            vertical = True

        for card in drawing_hand:
            card.draw(win, x, y, user)
            if vertical:
                y += 30
            else:
                x += 30
