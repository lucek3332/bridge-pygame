import random
import pygame


pygame.init()

# Images of cards
blue_back = pygame.image.load("images/deck/width 100/blue_back.png")
C2 = pygame.image.load("images/deck/width 100/C2.png")
C3 = pygame.image.load("images/deck/width 100/C3.png")
C4 = pygame.image.load("images/deck/width 100/C4.png")
C5 = pygame.image.load("images/deck/width 100/C5.png")
C6 = pygame.image.load("images/deck/width 100/C6.png")
C7 = pygame.image.load("images/deck/width 100/C7.png")
C8 = pygame.image.load("images/deck/width 100/C8.png")
C9 = pygame.image.load("images/deck/width 100/C9.png")
C10 = pygame.image.load("images/deck/width 100/C10.png")
C11 = pygame.image.load("images/deck/width 100/C11.png")
C12 = pygame.image.load("images/deck/width 100/C12.png")
C13 = pygame.image.load("images/deck/width 100/C13.png")
C14 = pygame.image.load("images/deck/width 100/C14.png")
D2 = pygame.image.load("images/deck/width 100/D2.png")
D3 = pygame.image.load("images/deck/width 100/D3.png")
D4 = pygame.image.load("images/deck/width 100/D4.png")
D5 = pygame.image.load("images/deck/width 100/D5.png")
D6 = pygame.image.load("images/deck/width 100/D6.png")
D7 = pygame.image.load("images/deck/width 100/D7.png")
D8 = pygame.image.load("images/deck/width 100/D8.png")
D9 = pygame.image.load("images/deck/width 100/D9.png")
D10 = pygame.image.load("images/deck/width 100/D10.png")
D11 = pygame.image.load("images/deck/width 100/D11.png")
D12 = pygame.image.load("images/deck/width 100/D12.png")
D13 = pygame.image.load("images/deck/width 100/D13.png")
D14 = pygame.image.load("images/deck/width 100/D14.png")
H2 = pygame.image.load("images/deck/width 100/H2.png")
H3 = pygame.image.load("images/deck/width 100/H3.png")
H4 = pygame.image.load("images/deck/width 100/H4.png")
H5 = pygame.image.load("images/deck/width 100/H5.png")
H6 = pygame.image.load("images/deck/width 100/H6.png")
H7 = pygame.image.load("images/deck/width 100/H7.png")
H8 = pygame.image.load("images/deck/width 100/H8.png")
H9 = pygame.image.load("images/deck/width 100/H9.png")
H10 = pygame.image.load("images/deck/width 100/H10.png")
H11 = pygame.image.load("images/deck/width 100/H11.png")
H12 = pygame.image.load("images/deck/width 100/H12.png")
H13 = pygame.image.load("images/deck/width 100/H13.png")
H14 = pygame.image.load("images/deck/width 100/H14.png")
S2 = pygame.image.load("images/deck/width 100/S2.png")
S3 = pygame.image.load("images/deck/width 100/S3.png")
S4 = pygame.image.load("images/deck/width 100/S4.png")
S5 = pygame.image.load("images/deck/width 100/S5.png")
S6 = pygame.image.load("images/deck/width 100/S6.png")
S7 = pygame.image.load("images/deck/width 100/S7.png")
S8 = pygame.image.load("images/deck/width 100/S8.png")
S9 = pygame.image.load("images/deck/width 100/S9.png")
S10 = pygame.image.load("images/deck/width 100/S10.png")
S11 = pygame.image.load("images/deck/width 100/S11.png")
S12 = pygame.image.load("images/deck/width 100/S12.png")
S13 = pygame.image.load("images/deck/width 100/S13.png")
S14 = pygame.image.load("images/deck/width 100/S14.png")


class Board:
    deck = ["".join([suit, str(honour)]) for suit in "CDHS" for honour in range(2, 15)]

    def __init__(self, board_id):
        self.id = board_id
        self.players = [None, None, None, None]
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.northHidden = True
        self.southHidden = True
        self.eastHidden = True
        self.westHidden = True
        self.history = []
        self.vulnerable = [False, False, False, False]
        self.set_vulnerable()
        self.shuffle()

    def shuffle(self):
        shuffle_deck = self.deck
        random.shuffle(shuffle_deck)
        self.north = sorted(shuffle_deck[:14], key=lambda x: (x[0], -int(x[1:])))
        self.south = sorted(shuffle_deck[14:27], key=lambda x: (x[0], -int(x[1:])))
        self.west = sorted(shuffle_deck[27:40], key=lambda x: (x[0], -int(x[1:])))
        self.east = sorted(shuffle_deck[40:53], key=lambda x: (x[0], -int(x[1:])))

    def set_vulnerable(self):
        if self.id % 16 == 2 or self.id % 16 == 5 or self.id % 16 == 12 or self.id % 16 == 15:
            self.vulnerable = [True, False, True, False]
        elif self.id % 16 == 4 or self.id % 16 == 7 or self.id % 16 == 10 or self.id % 16 == 13:
            self.vulnerable = [True, True, True, True]
        elif self.id % 16 == 3 or self.id % 16 == 6 or self.id % 16 == 9 or self.id % 16 == 0:
            self.vulnerable = [False, True, False, True]
        else:
            self.vulnerable = [False, False, False, False]

    def draw_hand(self, hand, seat):
        if seat == 0:
            pass
        elif seat == 1:
            pass
        elif seat == 2:
            pass
        else:
            pass
