import socket

PORT = 5050
HEADER = 8 # 8 byte header -> length of the next message
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(client=client, msg="My Balls!")
    send(client=client, msg=DISCONNECT_MESSAGE)
# end main


if __name__ == "__main__":
    main()


