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
    """
    Drawing all elements for input the username.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param player_name: InputString instance
    :param buttons: Button instance
    :return: None
    """
    # Background
    win.fill((40, 125, 67))
    # Drawing username with blue background
    player_name_text = font.render(player_name.get_string(), 1, (255, 255, 255))
    pygame.draw.rect(win, (7, 32, 110), (round(win.get_width() / 2 - 150), round(win.get_height() / 2 - 50), 300, 100))
    win.blit(player_name_text, (round(win.get_width() / 2 - player_name_text.get_width() / 2),
                                round(win.get_height() / 2 - player_name_text.get_height() / 2)))
    # Drawing messages
    type_your_name = font.render("Wpisz swoją nazwę użytkownika", 1, (0, 0, 0))
    win.blit(type_your_name, (round(win.get_width() / 2 - type_your_name.get_width() / 2), 400))
    # Buttons
    for btn in buttons:
        btn.draw(win)
    # Updating pygame window
    pygame.display.update()


def redraw_user_exist(win, font):
    """
    Drawing all elements, when the username is already in use.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :return: None
    """
    # Background
    win.fill((40, 125, 67))
    # Drawing messages
    user_exist_text = font.render("Użytkownik o podanej nazwie już istnieje", 1, (0, 0, 0))
    win.blit(user_exist_text, (round(win.get_width() / 2 - user_exist_text.get_width() / 2),
                               round(win.get_height() / 2 - user_exist_text.get_height() / 2)))
    # Updating pygame window
    pygame.display.update()


def redraw_tables(win, font, font2, buttons, online_players):
    """
    Drawing all elements, when the user is waiting in lobby.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param font2: pygame Surface instance
    :param buttons: list
    :param online_players: int
    :return: None
    """
    # Background
    win.fill((40, 125, 67))
    # Drawing title
    tables_text = font2.render("Dostępne stoły", 1, (0, 0, 0))
    win.blit(tables_text, (round(win.get_width() / 2 - tables_text.get_width() / 2), 20))
    # Drawing messages
    max_tables_text = font.render("Maksymalna liczba oczekujących stołów: 4", 1, (0, 0, 0))
    win.blit(max_tables_text, (120, 930))
    # Drawing the number of online players
    online_players_text = font.render(f"Graczy online {online_players}", 1, (0, 0, 0))
    win.blit(online_players_text, (960, 150))
    # Buttons
    for btn in buttons:
        btn.draw(win)


def draw_seats(win, empty_tables):
    """
    Drawing buttons for taking a seat.
    :param win: pygame Surface instance
    :param empty_tables: list
    :return: list
    """
    seating_buttons = []
    if empty_tables:
        # Iterating over tables in empty_tables list
        for i, table in enumerate(empty_tables):
            # Background for button
            pygame.draw.rect(win, (100, 131, 227), (80, 120 + 200 * i, 500, 180))
            # Iterating over players on the table
            for j, p in enumerate(table.players):
                # Determining if seat is free
                if p:
                    user_text = p[0]
                else:
                    user_text = "Usiądź"
                # Coordinates for button depending on player position
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
                # Initializing SeatingButton instances and appending button list
                seating_buttons.append(SeatingButton(140, 60, (7, 32, 110), user_text, x, y, table, j))
    # Drawing seating buttons
    for btn in seating_buttons:
        btn.draw(win)
    return seating_buttons


def redraw_sitting(win, font, table, user):
    """
    Drawing seats on the table.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param table: Table instance
    :param user: Player instance
    :return: None
    """
    # Background
    win.fill((40, 125, 67))
    # Iterating over players at the table
    player_text = None
    for i, p in enumerate(table.players):
        # Seat taken
        if p:
            if i == 0:
                player_text = font.render(f"S - {p[0]}", 1, (0, 0, 0))
            if i == 1:
                player_text = font.render(f"W - {p[0]}", 1, (0, 0, 0))
            if i == 2:
                player_text = font.render(f"N - {p[0]}", 1, (0, 0, 0))
            if i == 3:
                player_text = font.render(f"E - {p[0]}", 1, (0, 0, 0))
        # Free seat
        else:
            if i == 0:
                player_text = font.render("S", 1, (0, 0, 0))
            elif i == 1:
                player_text = font.render("W", 1, (0, 0, 0))
            elif i == 2:
                player_text = font.render("N", 1, (0, 0, 0))
            else:
                player_text = font.render("E", 1, (0, 0, 0))
        # Rotating players for display client username on the bottom of window
        i -= user.position
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
    """
    Drawing all elements, when user is waiting at the table.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param font2: pygame Surface instance
    :param buttons: list
    :param table: Table instance
    :param user: Player instance
    :return: None
    """
    # Drawing seats
    redraw_sitting(win, font, table, user)
    # Drawing title with table ID
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    # Drawing messages
    waiting_text = font2.render("Oczekiwanie na graczy", 1, (0, 0, 0), 1)
    win.blit(waiting_text, (round(win.get_width() / 2 - waiting_text.get_width() / 2),
                            round(win.get_height() / 2 - waiting_text.get_height() / 2)))
    # Buttons
    for btn in buttons:
        btn.draw(win)
    # Updating pygame window
    pygame.display.update()


def draw_cards(win, font, table, board, user):
    """
    Drawing all cards in hands.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param table: Table instance
    :param board: Board instance
    :param user: Player instance
    :return: None
    """
    # Assignation the dealer text
    if board.dealer == 0:
        dealer = "Dealer: S"
    elif board.dealer == 1:
        dealer = "Dealer: W"
    elif board.dealer == 2:
        dealer = "Dealer: N"
    else:
        dealer = "Dealer: E"
    # Drawing dealer info
    dealer_text = font.render(dealer, 1, (0, 0, 0))
    win.blit(dealer_text, (20, 10))
    # Drawing board condition
    vulnerable_text = font.render(board.vulnerable_txt, 1, (0, 0, 0))
    win.blit(vulnerable_text, (20, 50))

    # Iterating over players at the table
    for i, p in enumerate(table.players):
        # Client can see only his cards
        is_my_hand = False
        if p[0] == user.username:
            is_my_hand = True
        # Dummy can see declarer hand after first lead
        if board.dummy is not None and not board.first_lead:
            if user.position in board.declarer[1] and i in board.declarer[1]:
                is_my_hand = True
        # Rotating hands for drawing client cards always on the bottom of window
        hand = i
        i -= user.position
        if i < 0:
            i += 4
        # Drawing hand
        board.draw_hand(win, hand, i, is_my_hand)


def redraw_bidding(win, font, font2, buttons, table, board, user, normal_bids, special_bids):
    """
    Drawing all elements during bidding phase.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param font2: pygame Surface instance
    :param buttons: list
    :param table: Table instance
    :param board: Board instance
    :param user: Player instance
    :param normal_bids: dictionary
    :param special_bids: list
    :return: None
    """
    # Drawing seats
    redraw_sitting(win, font, table, user)
    # Drawing title with table ID
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    # Drawing board info
    board_text = font.render(f"Rozdanie {board.id}", 1, (0, 0, 0))
    win.blit(board_text, (1000, 20))
    # Drawing cards
    draw_cards(win, font, table, board, user)
    # Drawing bidding box, when it's user turn
    if board.turn == user.position:
        last_x = 0
        for i, bids in enumerate(normal_bids.items()):
            # Drawing level bids sequentially
            x = 835 + i * 38
            y = 850
            rect = (x, y, 35, 35)
            bids[0].rect = rect
            bids[0].rect = (x, y, 35, 35)
            text = font.render(bids[0].bid, 1, (0, 0, 0), 1)
            # Marking active the level bid by light green color
            if bids[0].active:
                pygame.draw.rect(win, (49, 224, 105), rect)
            else:
                pygame.draw.rect(win, (255, 255, 255), rect)
            win.blit(text, (round(x + rect[2] / 2 - text.get_width() / 2), round(y + rect[3] / 2 - text.get_height() / 2)))
            last_x = x
            # Drawing denomination bids for specific level bid
            if bids[0].active:
                for j, suitbid in enumerate(bids[1]):
                    image = eval(suitbid.bid)
                    x = 835 + j * 38
                    y = 890
                    rect = (x, y, 35, 35)
                    suitbid.rect = rect
                    pygame.draw.rect(win, (255, 255, 255), rect)
                    win.blit(image, (round(x + rect[2] / 2 - image.get_width() / 2), round(y + rect[3] / 2 - image.get_height() / 2)))
        # Drawing special bids like fold and double/redouble
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

    # Drawing bidding table rotated for client
    seats_rotation = [(1, "W"), (2, "N"), (3, "E"), (0, "S"), (1, "W"), (2, "N"), (3, "E"), (0, "S")]
    for i, seat in enumerate(seats_rotation[user.position:user.position + 4]):
        # Red background/white text for vulnerable
        if board.vulnerable[seat[0]]:
            color_rect = (166, 20, 3)
            color_text = (255, 255, 255)
        # White background/black text for vulnerable
        else:
            color_rect = (255, 255, 255)
            color_text = (0, 0, 0)
        header_txt = font.render(seat[1], 1, color_text)
        pygame.draw.rect(win, color_rect, (round(win.get_width() / 2 + (i - 2) * 60), 310, 60, 38))
        win.blit(header_txt, (round(win.get_width() / 2 + (i - 1.5) * 60 - header_txt.get_width() / 2), round(310 + 19 - header_txt.get_height() / 2)))
    # Displaying called bids on the table with correct localization
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
    # Drawing called bids
    for i, b in enumerate(board.bidding):
        if b:
            text = font.render(b.bid, 1, (0, 0, 0))
            win.blit(text, (round(win.get_width() / 2 + (i % 4 - 1.5) * 60 - text.get_width() / 2), round(345 + (i // 4) * 35 + 19 - text.get_height() / 2)))
    # Buttons
    for btn in buttons:
        btn.draw(win)
    # Updating pygame window
    pygame.display.update()


def redraw_playing(win, font, font2, buttons, table, board, user):
    """
    Drawing all elements during playing phase.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param font2: pygame Surface instance
    :param buttons: list
    :param table: Table instance
    :param board: Board instance
    :param user: Player instance
    :return: None
    """
    # Drawing seats
    redraw_sitting(win, font, table, user)
    # Drawing title with table ID
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    # Drawing table status
    game_ready_text = font2.render("ROZGRYWKA", 1, (0, 0, 0))
    win.blit(game_ready_text, (round(win.get_width() / 2 - game_ready_text.get_width() / 2),
                               round(win.get_height() / 2 - game_ready_text.get_height() / 2)))
    # Drawing cards
    draw_cards(win, font, table, board, user)
    # Drawing info about declarer, final contract and taken tricks by each side
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

    # Drawing the trick
    for i, p in enumerate(table.players):
        card = i
        i -= user.position
        if i < 0:
            i += 4
        if board.trick[card]:
            # Rotating the trick to client
            if i == 0:
                board.trick[card].draw(win, round(win.get_width() / 2 - 50), 600, True)
            elif i == 2:
                board.trick[card].draw(win, round(win.get_width() / 2 - 50), 330, True)
            elif i == 1:
                board.trick[card].draw(win, 400, round(win.get_height() / 2 - 153 / 2), True)
            else:
                board.trick[card].draw(win, 700, round(win.get_height() / 2 - 153 / 2), True)
    # Buttons
    for btn in buttons:
        btn.draw(win)
    # Updating pygame window
    pygame.display.update()


def redraw_score(win, font, font2, buttons, table, board, user):
    """
    Drawing score after finished board.
    :param win: pygame Surface instance
    :param font: pygame Surface instance
    :param font2: pygame Surface instance
    :param buttons: list
    :param table: Table instance
    :param board: Board instance
    :param user: Player instance
    :return: None
    """
    # Drawing seats
    redraw_sitting(win, font, table, user)
    # Drawing title with table ID
    table_text = font2.render(f"Stół nr {table.id}", 1, (0, 0, 0))
    win.blit(table_text, (round(win.get_width() / 2 - table_text.get_width() / 2), 10))
    # Drawing score
    if not board.declarer:
        score_text = font2.render("ROZDANIE PRZEPASOWANE", 1, (0, 0, 0))
    else:
        if board.declarer[1] == [0, 2]:
            score_text = font2.render(f"NS {board.result}, {board.score}", 1, (0, 0, 0), 1)
        else:
            score_text = font2.render(f"EW {board.result}, {board.score}", 1, (0, 0, 0), 1)
    win.blit(score_text, (round(win.get_width() / 2 - score_text.get_width() / 2),
                          round(win.get_height() / 2 - score_text.get_height() / 2)))
    # Updating pygame window
    pygame.display.update()
