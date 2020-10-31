import socket
import pickle
import time


# Global constants
SERVER_IP = "192.168.0.220"
SERVER_PORT = 5555
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
HEADER_SIZE = 30
BUFSIZE = 1024


class Player:
    def __init__(self, username):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome = self.connect()
        self.username = username
        self.position = None
        print(self.welcome)

    def connect(self):
        self.socket_client.connect(SERVER_ADDR)
        return self.socket_client.recv(BUFSIZE).decode("utf-8")

    def send(self, msg):
        try:
            data = pickle.dumps(msg)
            sending_header = f"{len(data):<{HEADER_SIZE}}"
            sending_data = bytes(sending_header, "utf-8") + data
            self.socket_client.send(sending_data)

            received = b""
            new_msg = True
            while True:
                if new_msg:
                    message_header = self.socket_client.recv(HEADER_SIZE)
                    if message_header:
                        message_len = int(message_header)
                        new_msg = False
                    else:
                        break
                elif len(received) != message_len:
                    message_chunk = self.socket_client.recv(BUFSIZE)
                    received += message_chunk
                else:
                    break

            if not received:
                self.socket_client.close()
                return None

        except Exception as e:
            print("[EXCEPTION]: ", e)
            self.socket_client.close()
            return None

        return pickle.loads(received)
