from game.board import Board


class Table:
    """
    Class for handling empty or full tables.
    """

    def __init__(self, table_id):
        self.id = table_id
        self.players = [None, None, None, None]  # S, W, N, E
        self.connected = [False, False, False, False]  # the same order as self.players
        self.board = None
        self.nr_boards = 0
        self.empty = True
        self.queue = 0

    def set_queue(self):
        """
        Changing value of queue attribute for executing some server requests once.
        :return: None
        """
        self.queue += 1
        if self.queue > 3:
            self.queue = 0

    def is_full(self):
        """
        Checking that the table is full or empty.
        :return: boolean
        """
        if all(p for p in self.connected):
            self.empty = False
            return True
        return False

    def set_player(self, index, username, address):
        """
        Setting player on the specific table seat.
        :param index: int
        :param username: string
        :param address: tuple
        :return: None
        """
        self.players[index] = (username, address)

    def remove_player(self, index):
        """
        Removing player from the specific table seat.
        :param index: int
        :return: None
        """
        self.players[index] = None

    def set_connected(self, index):
        """
        Marking player as connected.
        :param index: int
        :return: None
        """
        self.connected[index] = True

    def set_disconnected(self, index):
        """
        Marking player as disconnected.
        :param index: int
        :return: None
        """
        self.connected[index] = False

    def __repr__(self):
        return f"Table nr {self.id}"

    def next_board(self):
        """
        Initializing new board with increased ID.
        :return: None
        """
        self.nr_boards += 1
        self.board = Board(self.nr_boards)
        self.board.players = self.players
