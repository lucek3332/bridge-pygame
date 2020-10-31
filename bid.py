import pygame

pygame.init()

# Images of cards
font = pygame.font.SysFont("Arial", 20)
C = pygame.image.load("images/bid/004-club.png")
D = pygame.image.load("images/bid/002-diamond.png")
H = pygame.image.load("images/bid/003-like.png")
S = pygame.image.load("images/bid/001-spades.png")
N = font.render("N", 1, (0, 0, 0))


class Bid:
    font = pygame.font.SysFont("Arial", 20)

    def __init__(self, bid):
        self.bid = bid
        self.text = self.font.render(bid, 1, (0, 0, 0))
        self.rect = None

    def draw(self, win, x, y):
        win.blit(self.text, (x, y))
        self.rect = (x, y, 20, 20)

    def __repr__(self):
        return f"Bid: {self.bid}"


class BidButton:
    font = pygame.font.SysFont("Arial", 20)

    def __init__(self, bid):
        self.bid = bid
        self.active = False
        self.rect = None
        self.text = self.font.render(bid, 1, (0, 0, 0), 1)

    def draw(self, win, x, y):
        self.rect = (x, y, 20, 20)
        pygame.draw.rect(win, (255, 255, 255), self.rect, width=0, border_radius=5)
        win.blit(self.text, (x, y))

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                self.active = True
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
        self.image = eval(bid)

    def draw(self, win, x, y):
        if self.first_part_bid.active:
            self.rect = (x, y, 20, 20)
            pygame.draw.rect(win, (255, 255, 255), self.rect, width=0, border_radius=5)
            win.blit(self.image, (x, y))
        pass

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
    font = pygame.font.SysFont("Arial", 20)

    def __init__(self, bid):
        self.bid = bid
        self.bidded = False
        self.rect = None
        if bid == "ktr":
            self.text = self.font.render('X', 1, (0, 0, 0), 1)
        elif bid == "rktr":
            self.text = self.font.render('XX', 1, (0, 0, 0), 1)
        else:
            self.text = self.font.render('pas', 1, (0, 0, 0), 1)

    def draw(self, win, x, y):
        self.rect = (x, y, 20, 20)
        pygame.draw.rect(win, (255, 255, 255), self.rect, width=0, border_radius=5)
        win.blit(self.text, (x, y))

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                self.bidded = True
                return True
        return False

    def __repr__(self):
        return f"SpecialButton {self.text}"
