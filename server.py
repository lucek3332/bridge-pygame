import socket
import pickle
from _thread import start_new_thread
from table import Table

# Global constants
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5555
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
HEADER_SIZE = 30
BUFSIZE = 1024

# Global variables
countingPlayer = 0
users = {}
tables = {}
empty_tables = {}
tableID = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen()
print("[STARTED]: Server is running, waiting for connections")


def handle_connection(conn, addr):
    run = True
    global countingPlayer, empty_tables, tableID
    conn.send(bytes(f"{addr} connected to the server.", "utf-8"))
    while run:
        try:
            received = b""
            new_msg = True
            while True:
                if new_msg:
                    message_header = conn.recv(HEADER_SIZE)
                    if message_header:
                        message_len = int(message_header)
                        new_msg = False
                    else:
                        break
                elif len(received) != message_len:
                    message_chunk = conn.recv(BUFSIZE)
                    received += message_chunk
                else:
                    break
            if not received:
                break

            received_obj = pickle.loads(received)

            if received_obj.get("command") == "waiting in lobby":

                if received_obj.get("user") in users and users.get(received_obj.get("user")) != addr:
                    sending_bytes = pickle.dumps({"response": "user exist",
                                                  "empty_tables": empty_tables,
                                                  "count_players": countingPlayer})

                elif received_obj.get("user") not in users:
                    users[received_obj.get("user")] = addr
                    print(f"[USER ONLINE] The user {received_obj.get('user')} is currently online.")
                    sending_bytes = pickle.dumps({"response": "ok",
                                                  "empty_tables": empty_tables,
                                                  "count_players": countingPlayer})

                else:
                    sending_bytes = pickle.dumps({"response": "ok",
                                                  "empty_tables": empty_tables,
                                                  "count_players": countingPlayer})

            elif received_obj.get("command") == "create table":
                t = Table(tableID)
                t.set_player(0, received_obj.get("user"), addr)
                t.set_connected(0)
                empty_tables[tableID] = t
                print(f"[CREATE TABLE] The table nr {tableID} has been created.")
                tableID += 1
                sending_bytes = pickle.dumps({"response": "ok",
                                              "empty_tables": empty_tables,
                                              "count_players": countingPlayer,
                                              "table": t})

            elif received_obj.get('command') == "take seat":
                t = empty_tables.get(received_obj.get('table nr'))
                seat = received_obj.get("seat")
                t.set_player(seat, received_obj.get("user"), addr)
                t.set_connected(seat)
                if t.is_full():
                    tables[t.id] = t
                    del empty_tables[t.id]

                sending_bytes = pickle.dumps({"response": "ok",
                                              "empty_tables": empty_tables,
                                              "count_players": countingPlayer,
                                              "table": t})

            elif received_obj.get("command") == "waiting at table":
                t = empty_tables.get(received_obj.get("table nr"))
                if t is None:
                    t = tables.get(received_obj.get("table nr"))
                sending_bytes = pickle.dumps({"response": "ok",
                                              "table": t})

            elif received_obj.get("command") == "stand":
                t = empty_tables.get(received_obj.get("table nr"))
                if t:
                    for indx, p in enumerate(t.players):
                        if (received_obj.get("user"), addr) == p:
                            t.remove_player(indx)
                            t.set_disconnected(indx)
                            if sum(1 if p else 0 for p in t.players) == 0:
                                del empty_tables[received_obj.get("table nr")]
                                print(f"[DELETE TABLE] The table nr {received_obj.get('table nr')} has been deleted.")
                else:
                    t = tables.get(received_obj.get("table nr"))
                    for indx, p in enumerate(t.players):
                        if (received_obj.get("user"), addr) == p:
                            t.remove_player(indx)
                            t.set_disconnected(indx)
                            t.empty = True
                            empty_tables[received_obj.get("table nr")] = t
                            del tables[received_obj.get("table nr")]

                sending_bytes = pickle.dumps({"response": "ok",
                                              "empty_tables": empty_tables,
                                              "count_players": countingPlayer})

            elif received_obj.get("command") == "shuffle":
                t = tables.get(received_obj.get("table nr"))
                if not t.board and t.queue % 4 == 0:
                    t.next_board()
                t.set_queue()
                sending_bytes = pickle.dumps({"response": "ok",
                                              "table": t,
                                              "board": t.board})
            else:
                t = None
                if received_obj.get("command") == "bidding":
                    t = tables.get(received_obj.get("table nr"))
                    if t:
                        sending_bytes = pickle.dumps({"response": "ok",
                                                      "table": t,
                                                      "board": t.board})

                elif received_obj.get("command") == "click number":
                    t = tables.get(received_obj.get("table nr"))
                    if t:
                        for bid in t.board.available_bids:
                            if received_obj.get("bid").bid == bid.bid:
                                bid.active = True
                            else:
                                bid.active = False
                        sending_bytes = pickle.dumps({"response": "ok",
                                                      "table": t,
                                                      "board": t.board})

                elif received_obj.get("command") == "make bid":
                    t = tables.get(received_obj.get("table nr"))
                    if t:
                        t.board.make_bid(received_obj.get("user pos"), received_obj.get("bid"))
                        sending_bytes = pickle.dumps({"response": "ok",
                                                      "table": t,
                                                      "board": t.board})

                elif received_obj.get("command") == "playing":
                    t = tables.get(received_obj.get("table nr"))
                    if t:
                        sending_bytes = pickle.dumps({"response": "ok",
                                                      "table": t,
                                                      "board": t.board})
                elif received_obj.get("command") == "score":
                    t = tables.get(received_obj.get("table nr"))
                    if t:
                        if t.board and t.queue % 4 == 0:
                            t.board = None
                        sending_bytes = pickle.dumps({"response": "ok",
                                                      "table": t,
                                                      "board": t.board})
                if not t:
                    t = empty_tables.get(received_obj.get("table nr"))
                    if t.board:
                        t.board = None
                    sending_bytes = pickle.dumps({"response": "sb left table",
                                                  "table": t,
                                                  "board": t.board})

            sending_header = f"{len(sending_bytes):<{HEADER_SIZE}}"
            sending_data = bytes(sending_header, "utf-8") + sending_bytes
            conn.send(sending_data)

        except Exception as e:
            print(f"[EXCEPTION]: {e} from {addr[1]}")
            run = False

    print(f"[DISCONNECTION]: {addr} has been disconnected")
    countingPlayer -= 1
    conn.close()

    # Deleting user from server dictionary of users
    user_to_delete = None
    for k, v in users.items():
        if v == addr:
            user_to_delete = k
    if user_to_delete:
        del users[user_to_delete]
        print(f"[USER OFFLINE] The user {user_to_delete} is currently offline.")

    # Closing table if disconnected user was last on the table
    table_to_delete = None
    for t_id, t in empty_tables.items():
        if sum(1 if p else 0 for p in t.players) == 1:
            if (user_to_delete, addr) in t.players:
                table_to_delete = t.id
        # Removing user from the table with remaining players
        else:
            for indx, p in enumerate(t.players):
                if (user_to_delete, addr) == p:
                    t.remove_player(indx)
                    t.set_disconnected(indx)
    if table_to_delete:
        del empty_tables[table_to_delete]
        print(f"[DELETE TABLE] The table nr {table_to_delete} has been deleted.")

    # Removing user from full table and moving table to the empty table dictionary
    table_to_delete = None
    for t_id, t in tables.items():
        for indx, p in enumerate(t.players):
            if (user_to_delete, addr) == p:
                t.remove_player(indx)
                t.set_disconnected(indx)
                t.empty = True
                empty_tables[t.id] = t
                table_to_delete = t_id
    if table_to_delete:
        del tables[table_to_delete]


while True:
    conn, addr = server_socket.accept()
    print(f"[CONNECTED]: The connection has been established from {addr[0]}, {addr[1]}")
    countingPlayer += 1
    start_new_thread(handle_connection, (conn, addr))
