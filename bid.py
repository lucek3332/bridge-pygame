import pygame


pygame.init()


class Bid:
    # font = pygame.font.SysFont("Arial", 20)

    def __init__(self, bid):
        self.bid = bid
        # self.text = self.font.render(bid, 1, (0, 0, 0))
        self.rect = None

    """def draw(self, win, x, y):
        win.blit(self.text, (x, y))
        self.rect = (x, y, 20, 20)"""

    def __repr__(self):
        return f"Bid: {self.bid}"


class BidButton:

    def __init__(self, bid):
        self.bid = bid
        self.active = False
        self.rect = None

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                return True
        return False

    def deactivate(self):
        self.active = False

    def __repr__(self):
        return f"Button {self.bid}"


class BidButtonSuit:
    def __init__(self, bid, first_button):
        self.bid = bid
        self.first_part_bid = first_button
        self.rect = None
        self.bidded = False

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                self.bidded = True
                return True
        return False

    def __repr__(self):
        return f"ButtonSuit {self.bid}"


class SpecialBid:

    def __init__(self, bid):
        self.bid = bid
        self.bidded = False
        self.rect = None
        if bid == "ktr":
            self.text = 'X'
        elif bid == "rktr":
            self.text = 'XX'
        else:
            self.text = 'P'

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                self.bidded = True
                return True
        return False

    def __repr__(self):
        return f"SpecialButton {self.text}"
