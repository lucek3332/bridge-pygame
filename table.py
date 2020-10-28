class Table:
    def __init__(self, table_id):
        self.id = table_id
        self.players = [None, None, None, None]  # S, E, N, W
        self.connected = [False, False, False, False]  # the same order as self.players
        self.board = None
        self.nr_boards = 0

    def is_ready(self):
        if all(p for p in self.connected):
            return True
        return False

    def set_player(self, index, username, address):
        self.players[index] = (username, address)

    def set_connected(self, index):
        self.connected[index] = True

    def __repr__(self):
        return f"Table nr {self.id}"
