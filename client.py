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


class SeatingButton(Button):
    def __init__(self, width, height, color, string, x, y, table, seat):
        super().__init__(width, height, color, string, x, y)
        self.table = table
        self.seat = seat


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


def redraw_user_exist(win, font):
    win.fill((40, 125, 67))
    user_exist_text = font.render("Użytkownik o podanej nazwie istnieje już", 1, (0, 0, 0))
    win.blit(user_exist_text, (round(win.get_width() / 2 - user_exist_text.get_width() / 2),
                               round(win.get_height() / 2 - user_exist_text.get_height() / 2)))
    pygame.display.update()


def redraw_tables(win, font, font2, buttons, online_players):
    win.fill((40, 125, 67))
    tables_text = font2.render("Dostępne stoły", 1, (0, 0, 0))
    max_tables_text = font.render("Maksymalna liczba oczekujących stołów: 3", 1, (0, 0, 0))
    online_players_text = font.render(f"Graczy online {online_players}", 1, (0, 0, 0))
    win.blit(tables_text, (round(win.get_width() / 2 - tables_text.get_width() / 2), 20))
    win.blit(max_tables_text, (120, 730))
    win.blit(online_players_text, (760, 150))
    for btn in buttons:
        btn.draw(win)


def draw_seats(win, empty_tables):
    seating_buttons = []
    if empty_tables:
        for i, table in enumerate(empty_tables):
            pygame.draw.rect(win, (100, 131, 227), (80, 120 + 200 * i, 500, 180))
            for j, p in enumerate(table.players):
                if p:
                    user_text = p[0]
                else:
                    user_text = "Usiądź"
                if j == 0:
                    x = 80 + 250 - 60
                    y = 120 + 200 * i + 135 - 30
                elif j == 1:
                    x = 40 + 125 - 60
                    y = 120 + 200 * i + 90 - 30
                elif j == 2:
                    x = 80 + 250 - 60
                    y = 120 + 200 * i + 45 - 30
                else:
                    x = 120 + 375 - 60
                    y = 120 + 200 * i + 90 - 30

                seating_buttons.append(SeatingButton(120, 60, (7, 32, 110), user_text, x, y, table, j))
    for btn in seating_buttons:
        btn.draw(win)
    return seating_buttons


def redraw_sitting(win):
    win.fill((40, 125, 67))
    pygame.display.update()


# Buttons
confirm_name_btn = Button(200, 80, (7, 32, 110), "POTWIERDŹ", 400, 500)
create_table_btn = Button(200, 80, (7, 32, 110), "ZAŁÓŻ STÓŁ", 750, 680)


def mainLoop():
    # Initial values
    run = True
    status_game = "insert name"
    player_name = InputString()
    font = pygame.font.SysFont("Arial", 32)
    font2 = pygame.font.SysFont("Arial", 64)
    while run:

        if status_game == "insert name":
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
                            buttons = [create_table_btn]
                            p = Player(player_name.string)
                    elif event.key == 8:
                        player_name.remove_letter()
                    elif event.unicode:
                        player_name.add_letter(event.unicode)
                if event.type == pygame.MOUSEBUTTONUP:
                    if confirm_name_btn.on_button() and player_name.get_string():
                        status_game = "tables"
                        buttons = [create_table_btn]
                        p = Player(player_name.string)

        elif status_game == "user exist":
            redraw_user_exist(screen, font2)
            pygame.time.delay(2000)
            status_game = "insert name"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

        elif status_game == "tables":
            response = p.send({"command": "waiting in lobby",
                               "user": p.username})
            if response.get("response") != "ok":
                if response.get("response") == "user exist":
                    status_game = "user exist"
            empty_tables = response.get("empty_tables").values()
            currentPlayers = response.get("count_players")
            redraw_tables(screen, font, font2, buttons, currentPlayers)
            seating_buttons = draw_seats(screen, empty_tables)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if create_table_btn.on_button() and len(empty_tables) < 3:
                        response = p.send({"command": "create table",
                                           "user": p.username})
                        status_game = "sitting"
                        table = response.get("table")
                    for seat in seating_buttons:
                        if seat.on_button() and seat.string == "Usiądź":
                            print("taking a seat")
                            response = p.send({"command": "take seat",
                                               "user": p.username,
                                               "table nr": seat.table.id,
                                               "seat": seat.seat})
                            status_game = "sitting"

        elif status_game == "sitting":
            redraw_sitting(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()


mainLoop()
