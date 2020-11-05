import pygame
from buttons import SeatingButton


# Images of cards
bid_font = pygame.font.SysFont("Arial", 24)
C = pygame.image.load("images/bid/clubs.png")
D = pygame.image.load("images/bid/diamonds.png")
H = pygame.image.load("images/bid/hearts.png")
S = pygame.image.load("images/bid/spades.png")
N = bid_font.render("N", 1, (0, 0, 0), 1)


def redraw_insert_name(win, font, player_name, buttons):
    win.fill((40, 125, 67))
    player_name_text = font.render(player_name.get_string(), 1, (255, 255, 255))
    type_your_name = font.render("Wpisz swoją nazwę użytkownika", 1, (0, 0, 0))
    pygame.draw.rect(win, (7, 32, 110), (round(win.get_width() / 2 - 150), round(win.get_height() / 2 - 50), 300, 100))
    win.blit(type_your_name, (round(win.get_width() / 2 - type_your_name.get_width() / 2), 400))
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
    max_tables_text = font.render("Maksymalna liczba oczekujących stołów: 4", 1, (0, 0, 0))
    online_players_text = font.render(f"Graczy online {online_players}", 1, (0, 0, 0))
    win.blit(tables_text, (round(win.get_width() / 2 - tables_text.get_width() / 2), 20))
    win.blit(max_tables_text, (120, 930))
    win.blit(online_players_text, (960, 150))
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
                    x = 30 + 125 - 60
                    y = 120 + 200 * i + 90 - 30
                elif j == 2:
                    x = 80 + 250 - 60
                    y = 120 + 200 * i + 45 - 30
                else:
                    x = 110 + 375 - 60
                    y = 120 + 200 * i + 90 - 30

                seating_buttons.append(SeatingButton(140, 60, (7, 32, 110), user_text, x, y, table, j))
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
            win.blit(player_text, (round(win.get_width() / 2 - player_text.get_width() / 2), 950))
        elif i == 1:
            win.blit(player_text, (round(120 - player_text.get_width() / 2), 100))
        elif i == 2:
            win.blit(player_text, (round(win.get_width() / 2 - player_text.get_width() / 2), 100))
        elif i == 3:
            win.blit(player_text, (round(1050 - player_text.get_width() / 2), 100))


def redraw_waiting_at_table(win, font, font2, buttons, table, user):
    redraw_sitting(win, font, table, user.username)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    waiting_text = font2.render("Oczekiwanie na graczy", 1, (0, 0, 0), 1)
    win.blit(waiting_text, (round(win.get_width() / 2 - waiting_text.get_width() / 2),
                            round(win.get_height() / 2 - waiting_text.get_height() / 2)))
    for btn in buttons:
        btn.draw(win)
    pygame.display.update()


def draw_cards(win, font, table, board, user):
    if board.dealer == 0:
        dealer = "Dealer: S"
    elif board.dealer == 1:
        dealer = "Dealer: W"
    elif board.dealer == 2:
        dealer = "Dealer: N"
    else:
        dealer = "Dealer: E"
    dealer_text = font.render(dealer, 1, (0, 0, 0))
    vulnerable_text = font.render(board.vulnerable_txt, 1, (0, 0, 0))
    win.blit(dealer_text, (20, 10))
    win.blit(vulnerable_text, (20, 50))

    for i, p in enumerate(table.players):
        is_my_hand = False
        if p[0] == user.username:
            is_my_hand = True

        if board.dummy is not None and not board.first_lead:
            if user.position in board.declarer[1] and i in board.declarer[1]:
                is_my_hand = True
        hand = i
        i -= user.position
        if i < 0:
            i += 4
        board.draw_hand(win, hand, i, is_my_hand)


def redraw_bidding(win, font, font2, buttons, table, board, user, normal_bids, special_bids):
    redraw_sitting(win, font, table, user.username)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    board_text = font.render(f"Rozdanie {board.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    win.blit(board_text, (1000, 20))
    draw_cards(win, font, table, board, user)
    if board.turn == user.position:
        last_x = 0
        for i, bids in enumerate(normal_bids.items()):
            x = 835 + i * 38
            y = 850
            rect = (x, y, 35, 35)
            bids[0].rect = rect
            bids[0].rect = (x, y, 35, 35)
            text = font.render(bids[0].bid, 1, (0, 0, 0), 1)
            if bids[0].active:
                pygame.draw.rect(win, (49, 224, 105), rect)
            else:
                pygame.draw.rect(win, (255, 255, 255), rect)
            win.blit(text, (round(x + rect[2] / 2 - text.get_width() / 2), round(y + rect[3] / 2 - text.get_height() / 2)))
            last_x = x
            if bids[0].active:
                for j, suitbid in enumerate(bids[1]):
                    image = eval(suitbid.bid)
                    x = 835 + j * 38
                    y = 890
                    rect = (x, y, 35, 35)
                    suitbid.rect = rect
                    pygame.draw.rect(win, (255, 255, 255), rect)
                    win.blit(image, (round(x + rect[2] / 2 - image.get_width() / 2), round(y + rect[3] / 2 - image.get_height() / 2)))
        for j, b in enumerate(special_bids):
            if last_x:
                x = last_x + 38 + j * 45
            else:
                x = 835 + j * 45
            y = 850
            rect = (x, y, 42, 35)
            b.rect = rect
            pygame.draw.rect(win, (255, 255, 255), rect)
            text = font.render(b.text, 1, (0, 0, 0), 1)
            win.blit(text, (round(x + rect[2] / 2 - text.get_width() / 2),
                            round(y + rect[3] / 2 - text.get_height() / 2)))

    seats_rotation = [(1, "W"), (2, "N"), (3, "E"), (0, "S"), (1, "W"), (2, "N"), (3, "E"), (0, "S")]
    for i, seat in enumerate(seats_rotation[user.position:user.position + 4]):
        if board.vulnerable[seat[0]]:
            color_rect = (166, 20, 3)
            color_text = (255, 255, 255)
        else:
            color_rect = (255, 255, 255)
            color_text = (0, 0, 0)
        header_txt = font.render(seat[1], 1, color_text)
        pygame.draw.rect(win, color_rect, (round(win.get_width() / 2 + (i - 2) * 60), 310, 60, 38))
        win.blit(header_txt, (round(win.get_width() / 2 + (i - 1.5) * 60 - header_txt.get_width() / 2), round(310 + 19 - header_txt.get_height() / 2)))
    if not board.end_bidding():
        if board.dealer == user.position:
            board.bidding = [None, None, None] + board.bidding
        else:
            first_seat = user.position + 1
            if first_seat > 3:
                first_seat = 0
            if first_seat != board.dealer:
                if board.dealer - first_seat > 0:
                    board.bidding = [None] * (board.dealer - first_seat) + board.bidding
                else:
                    board.bidding = [None] * (board.dealer - first_seat + 4) + board.bidding
    for i, b in enumerate(board.bidding):
        if b:
            text = font.render(b.bid, 1, (0, 0, 0))
            win.blit(text, (round(win.get_width() / 2 + (i % 4 - 1.5) * 60 - text.get_width() / 2), round(345 + (i // 4) * 35 + 19 - text.get_height() / 2)))

    for btn in buttons:
        btn.draw(win)
    pygame.display.update()


def redraw_playing(win, font, font2, buttons, table, board, user):
    redraw_sitting(win, font, table, user.username)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    game_ready_text = font2.render("ROZGRYWKA", 1, (0, 0, 0))
    win.blit(game_ready_text, (round(win.get_width() / 2 - game_ready_text.get_width() / 2),
                               round(win.get_height() / 2 - game_ready_text.get_height() / 2)))
    draw_cards(win, font, table, board, user)
    if board.declarer[1] == [0, 2]:
        contract_text = font.render(f"Kontrakt {board.winning_bid} - NS", 1, (0, 0, 0))
        if board.declarer[0] == 0:
            declarer_text = font.render("Rozgrywa: S", 1, (0, 0, 0))
        else:
            declarer_text = font.render("Rozgrywa: N", 1, (0, 0, 0))
    else:
        contract_text = font.render(f"Kontrakt {board.winning_bid} - WE", 1, (0, 0, 0))
        if board.declarer[0] == 1:
            declarer_text = font.render("Rozgrywa: W", 1, (0, 0, 0))
        else:
            declarer_text = font.render("Rozgrywa: E", 1, (0, 0, 0))
    win.blit(contract_text, (920, 880))
    win.blit(declarer_text, (920, 920))
    tricks_text = font.render(f"NS: {board.tricks[0]}  EW: {board.tricks[1]}", 1, (0, 0, 0))
    win.blit(tricks_text, (920, 840))

    for i, p in enumerate(table.players):
        card = i
        i -= user.position
        if i < 0:
            i += 4
        if board.trick[card]:
            if i == 0:
                board.trick[card].draw(win, round(win.get_width() / 2 - 50), 600, True)
            elif i == 2:
                board.trick[card].draw(win, round(win.get_width() / 2 - 50), 330, True)
            elif i == 1:
                board.trick[card].draw(win, 400, round(win.get_height() / 2 - 153 / 2), True)
            else:
                board.trick[card].draw(win, 700, round(win.get_height() / 2 - 153 / 2), True)

    for btn in buttons:
        btn.draw(win)
    pygame.display.update()


def redraw_score(win, font, font2, buttons, table, board, user):
    redraw_sitting(win, font, table, user.username)
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    if not board.declarer:
        score_text = font2.render("ROZDANIE PRZEPASOWANE", 1, (0, 0, 0))
    else:
        if board.declarer[1] == [0, 2]:
            score_text = font2.render(f"NS {board.result} {board.score}", 1, (0, 0, 0), 1)
        else:
            score_text = font2.render(f"EW {board.result} {board.score}", 1, (0, 0, 0), 1)
    win.blit(score_text, (round(win.get_width() / 2 - score_text.get_width() / 2),
                          round(win.get_height() / 2 - score_text.get_height() / 2)))
    pygame.display.update()
