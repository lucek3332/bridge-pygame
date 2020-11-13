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
        self.empty = True
        self.board_history = []

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

    def next_board(self, boardID):
        """
        Initializing new board with specific ID.
        :return: None
        """
        self.board = Board(boardID)
        self.board.players = self.players
