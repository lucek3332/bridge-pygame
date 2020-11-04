from board import Board


class Table:
    def __init__(self, table_id):
        self.id = table_id
        self.players = [None, None, None, None]  # S, W, N, E
        self.connected = [False, False, False, False]  # the same order as self.players
        self.board = None
        self.nr_boards = 0
        self.empty = True
        self.queue = 0

    def set_queue(self):
        self.queue += 1
        if self.queue > 3:
            self.queue = 0

    def is_full(self):
        if all(p for p in self.connected):
            self.empty = False
            return True
        return False

    def set_player(self, index, username, address):
        self.players[index] = (username, address)

    def remove_player(self, index):
        self.players[index] = None

    def set_connected(self, index):
        self.connected[index] = True

    def set_disconnected(self, index):
        self.connected[index] = False

    def __repr__(self):
        return f"Table nr {self.id}"

    def next_board(self):
        self.nr_boards += 1
        self.board = Board(self.nr_boards)
        self.board.players = self.players
