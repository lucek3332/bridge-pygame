import socket
import pickle
from _thread import start_new_thread

# Global constants
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5555
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
HEADER_SIZE = 30
BUFSIZE = 1024

# Global variables
countingPlayer = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen()
print("[STARTED]: Server is running, waiting for connections")


def handle_connection(conn, addr):
    run = True
    global countingPlayer
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
            print(received_obj)

            sending_message = pickle.dumps(f"{addr} connected to the server.")
            sending_header = f"{len(sending_message):<{HEADER_SIZE}}"
            sending_data = bytes(sending_header, "utf-8") + sending_message
            conn.send(sending_data)

        except Exception as e:
            print("[EXCEPTION]: {}".format(e))
            run = False

    print(f"[DISCONNECTION]: {addr} has been disconnected")
    countingPlayer -= 1
    conn.close()


while True:
    conn, addr = server_socket.accept()
    print("[CONNECTED]: The connection has been established from {}, {}".format(addr[0], addr[1]))
    countingPlayer += 1
    start_new_thread(handle_connection, (conn, addr))
