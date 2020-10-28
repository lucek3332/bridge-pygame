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
tables = []
empty_tables = []
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
                    sending_bytes = pickle.dumps({"response": "user exist"})
                elif received_obj.get("user") not in users:
                    users[received_obj.get("user")] = addr
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
                empty_tables.append(t)
                tableID += 1
                sending_bytes = pickle.dumps({"response": "ok",
                                              "empty_tables": empty_tables,
                                              "count_players": countingPlayer,
                                              "table": t})
            sending_header = f"{len(sending_bytes):<{HEADER_SIZE}}"
            sending_data = bytes(sending_header, "utf-8") + sending_bytes
            conn.send(sending_data)

        except Exception as e:
            print("[EXCEPTION]: {}".format(e))
            run = False

    print(f"[DISCONNECTION]: {addr} has been disconnected")
    countingPlayer -= 1
    conn.close()

    for k, v in users.items():
        if v == addr:
            user_to_delete = k
    del users[user_to_delete]

    for t in empty_tables:
        if sum(1 if p else 0 for p in t.players) == 1:
            if (user_to_delete, addr) in t.players:
                empty_tables.remove(t)


while True:
    conn, addr = server_socket.accept()
    print(f"[CONNECTED]: The connection has been established from {addr[0]}, {addr[1]}")
    countingPlayer += 1
    start_new_thread(handle_connection, (conn, addr))
