class Table:
    def __init__(self, table_id):
        self.id = table_id
        self.players = [None, None, None, None]  # S, E, N, W
        self.connected = [False, False, False, False]  # the same order as self.players
        self.board = None
        self.nr_boards = 0
        self.empty = True

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
