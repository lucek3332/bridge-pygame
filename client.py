from player import Player
from drawing_func import *  # importing pygame as well
from buttons import Button


pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

# Screen settings
screenWidth = 1200
screenHeight = 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Bridge")
pygame.display.set_icon(icon)


# Helpful classes
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


# Buttons
confirm_name_btn = Button(200, 80, (7, 32, 110), "POTWIERDŹ", 500, 580)
create_table_btn = Button(200, 80, (7, 32, 110), "ZAŁÓŻ STÓŁ", 950, 880)
lobby_btn = Button(200, 80, (7, 32, 110), "WSTAŃ", 30, 900)


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
            empty_tables = list(response.get("empty_tables").values())[:4]
            currentPlayers = response.get("count_players")
            redraw_tables(screen, font, font2, buttons, currentPlayers)
            seating_buttons = draw_seats(screen, empty_tables)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if create_table_btn.on_button() and len(empty_tables) < 4:
                        response = p.send({"command": "create table",
                                           "user": p.username})
                        status_game = "waiting at table"
                        p.position = 0
                        buttons = [lobby_btn]
                        table = response.get("table")
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

        elif status_game == "waiting at table":
            response = p.send({"command": "waiting at table",
                              "user": p.username,
                              "table nr": table.id})
            table = response.get("table")
            if table.is_full():
                status_game = "bidding"
                response = p.send({"command": "shuffle",
                                   "user": p.username,
                                   "table nr": table.id})
                continue
            redraw_waiting_at_table(screen, font, font2, buttons, table, p)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        p.position = None
                        status_game = "tables"
                        buttons = [create_table_btn]

        elif status_game == "bidding":
            response = p.send({"command": "bidding",
                               "user": p.username,
                               "table nr": table.id})
            if response.get("response") == "sb left table":
                status_game = "waiting at table"
                continue
            table = response.get("table")
            board = response.get("board")
            if board.status == "play":
                status_game = "playing"
                continue
            normal_bids = dict()
            special_bids = []
            if p.position == board.turn:
                normal_bids = board.available_bids
                special_bids = board.special_bids
            redraw_bidding(screen, font, font2, buttons, table, board, p, normal_bids, special_bids)
            if not table.is_full():
                status_game = "waiting at table"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        status_game = "tables"
                        p.position = None
                        buttons = [create_table_btn]
                    for bid, bidSuits in normal_bids.items():
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
                    for special_bid in special_bids:
                        if special_bid.click():
                            response = p.send({"command": "make bid",
                                               "user": p.username,
                                               "table nr": table.id,
                                               "bid": special_bid.bid,
                                               "user pos": p.position
                                               })

        elif status_game == "playing":
            response = p.send({"command": "playing",
                               "user": p.username,
                               "table nr": table.id})
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

            if not board.declarer:
                redraw_score(screen, font, font2, buttons, table, board, p)
                pygame.time.delay(2000)
                status_game = "waiting at table"
                response = p.send({"command": "score",
                                   "user": p.username,
                                   "table nr": table.id
                                   })
                continue
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if lobby_btn.on_button():
                        response = p.send({"command": "stand",
                                           "user": p.username,
                                           "table nr": table.id})
                        p.position = None
                        status_game = "tables"
                        buttons = [create_table_btn]
                    if p.position != board.dummy:
                        if p.position == board.turn:
                            for card in hand:
                                if card.click():
                                    if board.color_lead and any(c.symbol[0] == board.color_lead for c in hand):
                                        if card.symbol[0] == board.color_lead:
                                            pygame.time.delay(300)
                                            response = p.send({"command": "make move",
                                                               "user": p.username,
                                                               "table nr": table.id,
                                                               "card": card.symbol
                                                               })
                                    else:
                                        pygame.time.delay(300)
                                        response = p.send({"command": "make move",
                                                           "user": p.username,
                                                           "table nr": table.id,
                                                           "card": card.symbol
                                                           })
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
                                    if card.click():
                                        if board.color_lead and any(c.symbol[0] == board.color_lead for c in dummy_hand):
                                            if card.symbol[0] == board.color_lead:
                                                pygame.time.delay(300)
                                                response = p.send({"command": "make move",
                                                                   "user": p.username,
                                                                   "table nr": table.id,
                                                                   "card": card.symbol
                                                                   })
                                        else:
                                            pygame.time.delay(300)
                                            response = p.send({"command": "make move",
                                                               "user": p.username,
                                                               "table nr": table.id,
                                                               "card": card.symbol
                                                               })


mainLoop()
