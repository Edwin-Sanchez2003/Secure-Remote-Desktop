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

def send(client:socket.socket, msg:str):
    # prep message
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    # send message
    client.send(send_length)
    client.send(message)
# end send


if __name__ == "__main__":
    main()


