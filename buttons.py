import pygame


pygame.init()


class Button:
    button_font = pygame.font.SysFont("Arial", 32)

    def __init__(self, width, height, color, string, x, y):
        self.width = width
        self.height = height
        self.color = color
        self.string = string
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        button_text = self.button_font.render("{}".format(self.string), True, (255, 255, 255))
        win.blit(button_text, (round(self.x + self.width / 2 - button_text.get_width() / 2), round(self.y + self.height / 2 - button_text.get_height() / 2)))

    def on_button(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False


class SeatingButton(Button):
    def __init__(self, width, height, color, string, x, y, table, seat):
        super().__init__(width, height, color, string, x, y)
        self.table = table
        self.seat = seat
