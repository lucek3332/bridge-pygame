import pygame

pygame.init()

# Images of cards
# blue_back = pygame.image.load("images/deck/width 100/blue_back.png")


class Bid:
    def __init__(self, bid):
        self.bid = bid
        self.image = eval(bid)
        self.image_table = eval(bid + "_table")
        self.rect = None

    def draw(self, win, x, y):
        win.blit(self.image, (x, y))
        self.rect = (x, y, 20, 20)

    def draw_in_table(self, win, x, y):
        win.blit(self.image_table, (x, y))

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect[0] < pos[0] < self.rect[0] + self.rect[2]:
            if self.rect[1] < pos[1] < self.rect[1] + self.rect[3]:
                return True
        return False

    def __repr__(self):
        return f"Bid: {self.bid}"
