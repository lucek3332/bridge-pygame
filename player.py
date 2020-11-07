import socket
import pickle


# Global constants
SERVER_IP = "34.105.199.145"  # write your local IP for local
SERVER_PORT = 5555
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
HEADER_SIZE = 30
BUFSIZE = 1024


class Player:
    """
    Class for handling client connection.
    """
    def __init__(self, username):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome = self.connect()
        self.username = username
        self.position = None
        print(self.welcome)

    def connect(self):
        """
        Connecting client socket to server socket.
        Receiving welcome message from server.
        :return: string
        """
        self.socket_client.connect(SERVER_ADDR)
        return self.socket_client.recv(BUFSIZE).decode("utf-8")

    def send(self, msg):
        """
        Sending objects to server using pickle and the fixed length header and receiving data from the server in the same way.
        :param msg: object
        :return: object
        """
        try:
            # Sending data
            data = pickle.dumps(msg)
            sending_header = f"{len(data):<{HEADER_SIZE}}"
            sending_data = bytes(sending_header, "utf-8") + data
            self.socket_client.send(sending_data)

            # Receiving data
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
