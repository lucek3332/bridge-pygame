import random
from card import Card
from bid import Bid, BidButton, BidButtonSuit, SpecialBid


class Board:
    deck = ["".join([suit, str(honour)]) for suit in "CDHS" for honour in range(2, 15)]
    bids = ["1C", "1D", "1H", "1S", "1N",
            "2C", "2D", "2H", "2S", "2N",
            "3C", "3D", "3H", "3S", "3N",
            "4C", "4D", "4H", "4S", "4N",
            "5C", "5D", "5H", "5S", "5N",
            "6C", "6D", "6H", "6S", "6N",
            "7C", "7D", "7H", "7S", "7N",
            ]

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
        self.status = "bidding"
        self.bidding = []
        self.winning_bid = None
        self.winning_side = []
        self.vulnerable = [False, False, False, False]
        self.vulnerable_txt = "Wszyscy przed"
        self.set_vulnerable()
        self.set_dealer()
        self.shuffle()

    def shuffle(self):
        shuffle_deck = self.deck
        random.shuffle(shuffle_deck)
        self.north = [Card(symbol) for symbol in sorted(shuffle_deck[:13], key=lambda x: (x[0], -int(x[1:])))]
        self.south = [Card(symbol) for symbol in sorted(shuffle_deck[13:26], key=lambda x: (x[0], -int(x[1:])))]
        self.west = [Card(symbol) for symbol in sorted(shuffle_deck[26:39], key=lambda x: (x[0], -int(x[1:])))]
        self.east = [Card(symbol) for symbol in sorted(shuffle_deck[39:52], key=lambda x: (x[0], -int(x[1:])))]

    def set_vulnerable(self):
        if self.id % 16 == 2 or self.id % 16 == 5 or self.id % 16 == 12 or self.id % 16 == 15:
            self.vulnerable = [True, False, True, False]
            self.vulnerable_txt = "NS po"
        elif self.id % 16 == 4 or self.id % 16 == 7 or self.id % 16 == 10 or self.id % 16 == 13:
            self.vulnerable = [True, True, True, True]
            self.vulnerable_txt = "Wszyscy po"
        elif self.id % 16 == 3 or self.id % 16 == 6 or self.id % 16 == 9 or self.id % 16 == 0:
            self.vulnerable = [False, True, False, True]
            self.vulnerable_txt = "WE po"
        else:
            self.vulnerable = [False, False, False, False]
            self.vulnerable_txt = "Wszyscy przed"

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
            y = 790
        elif seat == 1:
            x = 60
            y = round(win.get_height() / 2 - height / 2)
            vertical = True
        elif seat == 2:
            x = round(win.get_width() / 2 - width / 2)
            y = 150
        else:
            x = 1000
            y = round(win.get_height() / 2 - height / 2)
            vertical = True

        for card in drawing_hand:
            card.draw(win, x, y, user)
            if vertical:
                y += 30
            else:
                x += 30

    def make_bid(self, user, bid):
        if bid != "pas":
            if bid == "ktr" or bid == "rktr":
                self.winning_bid = self.winning_bid + "X"
            else:
                self.winning_bid = bid
            if user in [0, 2]:
                self.winning_side = [0, 2]
            else:
                self.winning_side = [1, 3]
        self.turn += 1
        if self.turn > 3:
            self.turn = 0
        self.bidding.append(Bid(bid))
        if self.end_bidding():
            if self.dealer == 0:
                self.bidding = [None, None, None] + self.bidding
            else:
                self.bidding = [None] * (self.dealer - 1) + self.bidding

    def get_available_bids(self, user):
        special_bids = ["pas"]
        if self.winning_bid:
            indx = self.bids.index(self.winning_bid[:2])
            if user not in self.winning_side:
                if self.winning_bid[-1] == "X" and len(self.winning_bid) == 3:
                    special_bids = special_bids + ["rktr"]
                elif self.winning_bid[-1] == "X" and len(self.winning_bid) == 4:
                    pass
                else:
                    special_bids = special_bids + ["ktr"]
            available_bids = self.bids[indx + 1:]
        else:
            available_bids = self.bids
        available_bids_dictio = dict()
        for b in available_bids:
            if available_bids_dictio.get(b[0]):
                available_bids_dictio[b[0]].append(b[1])
            else:
                available_bids_dictio[b[0]] = [b[1]]
        special_bids = [SpecialBid(b) for b in special_bids]
        normal_bids = dict()
        for k, values in available_bids_dictio.items():
            new_key = BidButton(k)
            normal_bids[new_key] = [BidButtonSuit(v, new_key) for v in values]
        return normal_bids, special_bids

    def end_bidding(self):
        if all(b.bid == "pas" for b in self.bidding[:4]):
            self.status = "play"
            return True
        elif all(b.bid == "pas" for b in self.bidding[-3:]) and len(self.bidding) > 3:
            self.status = "play"
            return True
        return False
