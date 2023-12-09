import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 8 # 8 byte header -> length of the next message
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def main():
    server.listen(1)
    print(f"[LISTENING]: Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn=conn, addr=addr)
# end main


def handle_client(conn:socket.socket, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # make sure that the message is an actual message
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}]: {msg}")

            # check if we should disconnect
            if msg == DISCONNECT_MESSAGE:
                connected = False
            # end if
        # end if
    # end while
    conn.close()
# end handle_client


if __name__ == "__main__":
    main()
