import pygame
from buttons import SeatingButton


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


def redraw_sitting(win, font, table, user):
    win.fill((40, 125, 67))
    for i, p in enumerate(table.players):
        if p:
            if p[0] == user:
                user_seat = i
    for i, p in enumerate(table.players):
        if p:
            if i == 0:
                player_text = font.render(f"S - {p[0]}", 1, (0, 0, 0))
            if i == 1:
                player_text = font.render(f"W - {p[0]}", 1, (0, 0, 0))
            if i == 2:
                player_text = font.render(f"N - {p[0]}", 1, (0, 0, 0))
            if i == 3:
                player_text = font.render(f"E - {p[0]}", 1, (0, 0, 0))
        else:
            if i == 0:
                player_text = font.render("S", 1, (0, 0, 0))
            elif i == 1:
                player_text = font.render("W", 1, (0, 0, 0))
            elif i == 2:
                player_text = font.render("N", 1, (0, 0, 0))
            else:
                player_text = font.render("E", 1, (0, 0, 0))
        i -= user_seat
        if i < 0:
            i += 4
        if i == 0:
            win.blit(player_text, (round(win.get_width() / 2 - player_text.get_width() / 2), 700))
        elif i == 1:
            win.blit(player_text, (50, round(win.get_height() / 2 - player_text.get_height() / 2)))
        elif i == 2:
            win.blit(player_text, (round(win.get_width() / 2 - player_text.get_width() / 2), 100))
        elif i == 3:
            win.blit(player_text, (850, round(win.get_height() / 2 - player_text.get_height() / 2)))


def redraw_waiting_at_table(win, font, font2, buttons, table, user):
    redraw_sitting(win, font, table, user)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    waiting_text = font.render("Oczekiwanie na graczy", 1, (0, 0, 0), 1)
    win.blit(waiting_text, (round(win.get_width() / 2 - waiting_text.get_width() / 2),
                            round(win.get_height() / 2 - waiting_text.get_height() / 2)))
    for btn in buttons:
        btn.draw(win)
    pygame.display.update()


def redraw_dealing(win, font, font2, buttons, table, user):
    redraw_sitting(win, font, table, user)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    game_ready_text = font2.render("GRAMY", 1, (0, 0, 0))
    win.blit(game_ready_text, (round(win.get_width() / 2 - game_ready_text.get_width() / 2), round(win.get_height() / 2 - game_ready_text.get_height() / 2)))
    for btn in buttons:
        btn.draw(win)
    pygame.display.update()
