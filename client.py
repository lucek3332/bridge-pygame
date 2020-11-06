from player import Player
from drawing_func import *  # importing pygame as well
from buttons import Button


pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

# Sounds
card_sound = pygame.mixer.Sound()

# Screen settings
screenWidth = 1200
screenHeight = 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Bridge")
pygame.display.set_icon(icon)


# Helpful classes
class InputString:
    """
    Handling user input. Utilizing for typing username.
    """

    def __init__(self):
        self.string = ""

    def add_letter(self, char):
        """
        Adding specific character to stored string.
        :param char: string
        :return: None
        """
        self.string += char

    def remove_letter(self):
        """
        Removing last character from stored string.
        :return: None
        """
        if len(self.string) >= 1:
            self.string = self.string[:-1]
        else:
            self.reset()

    def reset(self):
        """
        Setting stored string to empty string.
        :return: None
        """
        self.string = ""

    def get_string(self):
        """
        Getting stored string.
        :return: string
        """
        return self.string


# Buttons
confirm_name_btn = Button(200, 80, (7, 32, 110), "POTWIERDŹ", 500, 580)
create_table_btn = Button(200, 80, (7, 32, 110), "ZAŁÓŻ STÓŁ", 950, 880)
lobby_btn = Button(200, 80, (7, 32, 110), "WSTAŃ", 30, 900)


def mainLoop():
    """
    Game loop
    :return: None
    """

    # Initial values
    run = True
    status_game = "insert name"
    player_name = InputString()
    font = pygame.font.SysFont("Arial", 32)
    font2 = pygame.font.SysFont("Arial", 64)

    while run:

        # View for bringing in username
        if status_game == "insert name":
            buttons = [confirm_name_btn]
            redraw_insert_name(screen, font, player_name, buttons)

            # Controls in specific view
            for event in pygame.event.get():
                # Possibility of quiting game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Pressed keys
                if event.type == pygame.KEYDOWN:
                    # Confirm username by ENTER and move to the next view
                    if event.key == 13 or event.key == 271:
                        if player_name.get_string():
                            status_game = "tables"
                            buttons = [create_table_btn]
                            p = Player(player_name.string)
                    # Removing letter
                    elif event.key == 8:
                        player_name.remove_letter()
                    # Adding specific letter
                    elif event.unicode:
                        player_name.add_letter(event.unicode)
                # Confirm username by clicking button and move to the next view
                if event.type == pygame.MOUSEBUTTONUP:
                    if confirm_name_btn.on_button() and player_name.get_string():
                        status_game = "tables"
                        buttons = [create_table_btn]
                        p = Player(player_name.string)

        # Username is already in use, back to previous view
        elif status_game == "user exist":
            redraw_user_exist(screen, font2)
            pygame.time.delay(2000)
            status_game = "insert name"
            # Possibility of quiting game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

        # View for displaying available tables
        elif status_game == "tables":
            response = p.send({"command": "waiting in lobby",
                               "user": p.username})
            if response.get("response") != "ok":
                if response.get("response") == "user exist":
                    status_game = "user exist"
            empty_tables = list(response.get("empty_tables").values())[:4]
            currentPlayers = response.get("count_players")
            redraw_tables(screen, font, font2, buttons, currentPlayers)
            seating_buttons = draw_seats(screen, empty_tables)
            pygame.display.update()
            # Controls in specific view
            for event in pygame.event.get():
                # Possibility of quiting game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Pressed mouse button
                if event.type == pygame.MOUSEBUTTONUP:
                    # Create a new, empty table
                    if create_table_btn.on_button() and len(empty_tables) < 4:
                        response = p.send({"command": "create table",
                                           "user": p.username})
                        status_game = "waiting at table"
                        p.position = 0
                        buttons = [lobby_btn]
                        table = response.get("table")
                    # Taking seat on the existing table
                    for seat in seating_buttons:
                        if seat.on_button() and seat.string == "Usiądź":
                            response = p.send({"command": "take seat",
                                               "user": p.username,
                                               "table nr": seat.table.id,
                                               "seat": seat.seat})
                            p.position = seat.seat
                            table = response.get("table")
                            status_game = "waiting at table"
                            buttons = [lobby_btn]

        # Waiting for other players on the table
        elif status_game == "waiting at table":
            response = p.send({"command": "waiting at table",
                              "user": p.username,
                              "table nr": table.id})
            table = response.get("table")

            # Starting bidding phase, when the table is full
            if table.is_full():
                status_game = "bidding"
                response = p.send({"command": "shuffle",
                                   "user": p.username,
                                   "table nr": table.id})
                continue
            redraw_waiting_at_table(screen, font, font2, buttons, table, p)

            # Controls in specific view
            for event in pygame.event.get():
                # Possibility of quiting game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Pressed mouse button
                if event.type == pygame.MOUSEBUTTONUP:
                    # Back to table view, free up the seat
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        p.position = None
                        status_game = "tables"
                        buttons = [create_table_btn]

        # Bidding phase
        elif status_game == "bidding":
            response = p.send({"command": "bidding",
                               "user": p.username,
                               "table nr": table.id})

            # Somebody has left table during bidding phase
            if response.get("response") == "sb left table":
                status_game = "waiting at table"
                continue

            table = response.get("table")
            board = response.get("board")

            # Starting playing phase
            if board.status == "play":
                status_game = "playing"
                continue

            normal_bids = dict()
            special_bids = []

            # Displaying bidding box if it's user turn
            if p.position == board.turn:
                normal_bids = board.available_bids
                special_bids = board.special_bids
            redraw_bidding(screen, font, font2, buttons, table, board, p, normal_bids, special_bids)
            if not table.is_full():
                status_game = "waiting at table"

            # Controls in specific view
            for event in pygame.event.get():
                # Possibility of quiting game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Pressed mouse button
                if event.type == pygame.MOUSEBUTTONUP:
                    # Back to table view, free up the seat
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        status_game = "tables"
                        p.position = None
                        buttons = [create_table_btn]
                    # Iterating over levels and their denominations
                    for bid, bidSuits in normal_bids.items():
                        # Clicking on the level bid
                        if bid.click():
                            for b in normal_bids.keys():
                                b.active = False
                            bid.active = True
                            response = p.send({"command": "click number",
                                               "user": p.username,
                                               "table nr": table.id,
                                               "bid": bid
                                               })
                            break
                        # Clicking on the denomination, if the level bid has been chosen
                        if bid.active:
                            for bidSuit in bidSuits:
                                if bidSuit.click():
                                    clicked_bid = bid.bid + bidSuit.bid
                                    response = p.send({"command": "make bid",
                                                       "user": p.username,
                                                       "table nr": table.id,
                                                       "bid": clicked_bid,
                                                       "user pos": p.position
                                                       })
                                    break

                    # Clicking on fold or double/redouble bids
                    for special_bid in special_bids:
                        if special_bid.click():
                            response = p.send({"command": "make bid",
                                               "user": p.username,
                                               "table nr": table.id,
                                               "bid": special_bid.bid,
                                               "user pos": p.position
                                               })
        # Playing phase
        elif status_game == "playing":
            response = p.send({"command": "playing",
                               "user": p.username,
                               "table nr": table.id})

            # Somebody has left table during playing phase
            if response.get("response") == "sb left table":
                status_game = "waiting at table"
                continue

            table = response.get("table")
            board = response.get("board")
            if p.position == 0:
                hand = board.south
            elif p.position == 1:
                hand = board.west
            elif p.position == 2:
                hand = board.north
            else:
                hand = board.east

            # The board is passed out, dealing next board
            if not board.declarer:
                redraw_score(screen, font, font2, buttons, table, board, p)
                pygame.time.delay(2000)
                status_game = "waiting at table"
                response = p.send({"command": "score",
                                   "user": p.username,
                                   "table nr": table.id
                                   })
                continue

            # Board is done, displaying score and dealing next board
            if board.score:
                pygame.time.delay(500)
                redraw_score(screen, font, font2, buttons, table, board, p)
                pygame.time.delay(4000)
                status_game = "waiting at table"
                response = p.send({"command": "score",
                                   "user": p.username,
                                   "table nr": table.id
                                   })
            redraw_playing(screen, font, font2, buttons, table, board, p)

            # Controls in specific view
            for event in pygame.event.get():
                # Possibility of quiting game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Pressed mouse button
                if event.type == pygame.MOUSEBUTTONUP:
                    # Back to table view, free up the seat
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        p.position = None
                        status_game = "tables"
                        buttons = [create_table_btn]

                    # Dummy can't do any move
                    if p.position != board.dummy:
                        # Player's turn
                        if p.position == board.turn:
                            for card in hand:
                                # Play specific card (if able to do so)
                                if card.click():
                                    if board.color_lead and any(c.symbol[0] == board.color_lead for c in hand):
                                        if card.symbol[0] == board.color_lead:
                                            pygame.time.delay(200)
                                            card_sound.play()
                                            response = p.send({"command": "make move",
                                                               "user": p.username,
                                                               "table nr": table.id,
                                                               "card": card.symbol
                                                               })
                                    else:
                                        pygame.time.delay(200)
                                        card_sound.play()
                                        response = p.send({"command": "make move",
                                                           "user": p.username,
                                                           "table nr": table.id,
                                                           "card": card.symbol
                                                           })

                        # Declarer plays dummy hand too
                        elif p.position in board.declarer[1]:
                            if board.dummy == board.turn:
                                if board.dummy == 0:
                                    dummy_hand = board.south
                                elif board.dummy == 1:
                                    dummy_hand = board.west
                                elif board.dummy == 2:
                                    dummy_hand = board.north
                                else:
                                    dummy_hand = board.east

                                for card in dummy_hand:
                                    # Play specific card (if able to do so)
                                    if card.click():
                                        if board.color_lead and any(c.symbol[0] == board.color_lead for c in dummy_hand):
                                            if card.symbol[0] == board.color_lead:
                                                pygame.time.delay(200)
                                                card_sound.play()
                                                response = p.send({"command": "make move",
                                                                   "user": p.username,
                                                                   "table nr": table.id,
                                                                   "card": card.symbol
                                                                   })
                                        else:
                                            pygame.time.delay(200)
                                            card_sound.play()
                                            response = p.send({"command": "make move",
                                                               "user": p.username,
                                                               "table nr": table.id,
                                                               "card": card.symbol
                                                               })


mainLoop()
