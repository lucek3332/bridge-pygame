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
        self.available_bids = None
        self.special_bids = None
        self.declarer = None
        self.dummy = None
        self.dummy_visible = False
        self.trump = None
        self.lead = None
        self.first_lead = True
        self.color_lead = None
        self.trick = [None, None, None, None]
        self.tricks = [0, 0]
        self.score = 0
        self.result = None
        self.set_vulnerable()
        self.set_dealer()
        self.shuffle()

    def __repr__(self):
        return f"Board nr {self.id}"

    def shuffle(self):
        shuffle_deck = self.deck
        random.shuffle(shuffle_deck)
        self.north = [Card(symbol) for symbol in sorted(shuffle_deck[:13], key=lambda x: (x[0], -int(x[1:])))]
        self.south = [Card(symbol) for symbol in sorted(shuffle_deck[13:26], key=lambda x: (x[0], -int(x[1:])))]
        self.west = [Card(symbol) for symbol in sorted(shuffle_deck[26:39], key=lambda x: (x[0], -int(x[1:])))]
        self.east = [Card(symbol) for symbol in sorted(shuffle_deck[39:52], key=lambda x: (x[0], -int(x[1:])))]
        self.north[-1].last_card = True
        self.south[-1].last_card = True
        self.west[-1].last_card = True
        self.east[-1].last_card = True

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
        self.available_bids, self.special_bids = self.get_available_bids()

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

    def set_actual_declarer(self, user):
        if user in [0, 2]:
            self.declarer = (user, [0, 2], self.trump)
        else:
            self.declarer = (user, [1, 3], self.trump)

    def set_lead(self):
        self.lead = self.declarer[0] + 1
        if self.lead > 3:
            self.lead = 0

    def make_bid(self, user, bid):
        if bid != "pas":
            if bid == "ktr" or bid == "rktr":
                self.winning_bid = self.winning_bid + "X"
            else:
                self.winning_bid = bid
                if not self.declarer:
                    self.trump = self.winning_bid[1]
                    self.set_actual_declarer(user)
                else:
                    if self.winning_bid[1] != self.trump:
                        self.set_actual_declarer(user)
                    elif user not in self.declarer[1]:
                        self.set_actual_declarer(user)
            if user in [0, 2]:
                self.winning_side = [0, 2]
            else:
                self.winning_side = [1, 3]
        self.turn += 1
        if self.turn > 3:
            self.turn = 0
        self.bidding.append(Bid(bid))
        self.available_bids, self.special_bids = self.get_available_bids()
        if self.end_bidding():
            if self.dealer == 0:
                self.bidding = [None, None, None] + self.bidding
            else:
                self.bidding = [None] * (self.dealer - 1) + self.bidding

    def get_available_bids(self):
        special_bids = ["pas"]
        if self.winning_bid:
            indx = self.bids.index(self.winning_bid[:2])
            if self.turn not in self.winning_side:
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
        if all(b.bid == "pas" for b in self.bidding[:4]) and len(self.bidding) == 4:
            self.status = "play"
            return True
        elif all(b.bid == "pas" for b in self.bidding[-3:]) and len(self.bidding) > 3:
            self.status = "play"
            self.set_lead()
            for player in self.declarer[1]:
                if self.declarer[0] != player:
                    self.dummy = player
            self.turn = self.lead
            if self.trump != "N":
                self.setting_trumps()
            return True
        return False

    def setting_trumps(self):
        for hand in [self.south, self.north, self.east, self.west]:
            for card in hand:
                if card.symbol[0] == self.trump:
                    card.trump = True

    def make_move(self, card_symbol):
        self.first_lead = False
        if all(t for t in self.trick):
            self.history.append(self.trick)
            self.trick = [None, None, None, None]
        card = None
        if self.turn == 0:
            hand = self.south
        elif self.turn == 1:
            hand = self.west
        elif self.turn == 2:
            hand = self.north
        else:
            hand = self.east
        for c in hand:
            if c.symbol == card_symbol:
                card = c
                hand.remove(c)
        if len(hand) > 0:
            hand[-1].last_card = True
        card.hidden = False
        self.trick[self.turn] = card
        if self.lead is not None:
            self.color_lead = card_symbol[0]
        self.lead = None
        if not self.dummy_visible:
            self.dummy_visible = True
            if self.dummy == 0:
                dummy_cards = self.south
            elif self.dummy == 1:
                dummy_cards = self.west
            elif self.dummy == 2:
                dummy_cards = self.north
            else:
                dummy_cards = self.east
            for c in dummy_cards:
                c.hidden = False
        self.turn += 1
        if self.turn > 3:
            self.turn = 0
        if all(t for t in self.trick):
            for t in self.trick:
                t.set_value(self.color_lead)
            self.turn = self.trick.index(max(self.trick))
            if self.turn in [0, 2]:
                self.tricks[0] += 1
            else:
                self.tricks[1] += 1
            self.lead = self.turn
            self.color_lead = None
            if len(hand) == 0:
                self.set_score()
                self.status = "score"

    def set_score(self):
        level_contract = int(self.winning_bid[0]) + 6
        if self.declarer[1] == [0, 2]:
            vul = self.vulnerable[0]
            taken_tricks = self.tricks[0]
        else:
            vul = self.vulnerable[1]
            taken_tricks = self.tricks[1]
        score = taken_tricks - level_contract
        if score == 0:
            self.result = self.winning_bid + "=="
        elif score > 0:
            self.result = self.winning_bid + f"+{score}"
        else:
            self.result = self.winning_bid + f"{score}"
        doubled = False
        redoubled = False
        if self.winning_bid.endswith("X"):
            if len(self.winning_bid) == 3:
                doubled = True
            else:
                redoubled = True
        making_game = False
        making_slam = False
        making_grand_slam = False
        if level_contract == 7 and score == 0:
            making_grand_slam = True
        elif level_contract == 7 and score >= 0:
            making_slam = True
        if score >= 0:
            if (self.trump == "C" or self.trump == "D") and level_contract >= 5:
                making_game = True
            elif (self.trump == "H" or self.trump == "S") and level_contract >= 4:
                making_game = True
            elif self.trump == "N" and level_contract >= 3:
                making_game = True

            if vul:
                if making_game:
                    self.score += 500
                elif making_slam:
                    self.score += 750
                elif making_grand_slam:
                    self.score += 1500
                else:
                    self.score += 50 * (doubled * 2 + redoubled * 2)
            else:
                if making_game:
                    self.score += 300
                elif making_slam:
                    self.score += 500
                elif making_grand_slam:
                    self.score += 1000
                else:
                    self.score += 50 * (doubled * 2 + redoubled * 2)
            if vul:
                if self.trump == "C" or self.trump == "D":
                    self.score += level_contract * 20 + score * (20 + 180 * doubled + 200 * redoubled)
                elif self.trump == "H" or self.trump == "S":
                    self.score += level_contract * 30 + score * (30 + 170 * doubled + 200 * redoubled)
                elif self.trump == "N":
                    self.score += 40 + (level_contract - 1) * 30 + score * (30 + 170 * doubled + 200 * redoubled)
            else:
                if self.trump == "C" or self.trump == "D":
                    self.score += 100 + score * (20 + 80 * doubled + 100 * redoubled)
                elif self.trump == "H" or self.trump == "S":
                    self.score += 120 + score * (30 + 70 * doubled + 100 * redoubled)
                elif self.trump == "N":
                    self.score += 100 + score * (30 + 70 * doubled + 100 * redoubled)
        elif score == -1:
            if vul:
                self.score -= 100 + 100 * doubled + 200 * redoubled
            else:
                self.score -= 50 + 50 * doubled + 100 * redoubled
        elif score == -2:
            if vul:
                self.score -= 200 + 300 * doubled + 500 * redoubled
            else:
                self.score -= 100 + 200 * doubled + 300 * redoubled
        elif score == -3:
            if vul:
                self.score -= 300 + 500 * doubled + 800 * redoubled
            else:
                self.score -= 150 + 350 * doubled + 500 * redoubled
        else:
            if vul:
                self.score -= 300 + 500 * doubled + 800 * redoubled + abs(score + 3) * (100 + 200 * doubled + 300 * redoubled)
            else:
                self.score -= 150 + 350 * doubled + 500 * redoubled + abs(score + 3) * (50 + 250 * doubled + 300 * redoubled)
