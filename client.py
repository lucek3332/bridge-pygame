import pygame
from player import Player

pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

# Screen settings
screenWidth = 1000
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Bridge")
pygame.display.set_icon(icon)


# Helpful classes
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


class InputString:

    def __init__(self):
        self.string = ""

    def add_letter(self, char):
        self.string += char

    def remove_letter(self):
        if len(self.string) >= 1:
            self.string = self.string[:-1]
        else:
            self.reset()

    def reset(self):
        self.string = ""

    def get_string(self):
        return self.string


# Display functions
def redraw_insert_name(win, font, player_name, buttons):
    win.fill((40, 125, 67))
    player_name_text = font.render(player_name.get_string(), 1, (255, 255, 255))
    type_your_name = font.render("Wpisz swoją nazwę użytkownika", 1, (0, 0, 0))
    pygame.draw.rect(win, (7, 32, 110), (round(win.get_width() / 2 - 150), round(win.get_height() / 2 - 50), 300, 100))
    win.blit(type_your_name, (round(win.get_width() / 2 - type_your_name.get_width() / 2), 300))
    win.blit(player_name_text, (round(win.get_width() / 2 - player_name_text.get_width() / 2), round(win.get_height() / 2 - player_name_text.get_height() / 2)))
    for btn in buttons:
        btn.draw(win)
    pygame.display.update()


def redraw_tables(win, font, buttons):
    win.fill((40, 125, 67))
    tables_text = font.render("Dostępne stoły", 1, (0, 0, 0))
    win.blit(tables_text, (400, 400))
    pygame.display.update()


# Buttons
confirm_name_btn = Button(200, 80, (7, 32, 110), "POTWIERDŹ", 400, 500)

def mainLoop():
    # Initial values
    run = True
    status_game = "insert_name"
    player_name = InputString()
    font = pygame.font.SysFont("Arial", 32)
    while run:

        if status_game == "insert_name":
            buttons = [confirm_name_btn]
            redraw_insert_name(screen, font, player_name, buttons)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == 13 or event.key == 271:
                        if player_name.get_string():
                            status_game = "tables"
                            buttons = []
                    elif event.key == 8:
                        player_name.remove_letter()
                    elif event.unicode:
                        player_name.add_letter(event.unicode)
                if event.type == pygame.MOUSEBUTTONUP:
                    if confirm_name_btn.on_button() and player_name.get_string():
                        status_game = "tables"
                        buttons = []

        elif status_game == "tables":
            redraw_tables(screen, font, buttons)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()


mainLoop()
