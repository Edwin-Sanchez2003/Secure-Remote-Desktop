
import json
import socket

import params

SERVER = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
ADDR = (SERVER, params.PORT)


def main():
    # initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR) # use specified server & port
    server.listen(1) # only allow 1 connection at a time
    print(f"[LISTENING]: Server is listening on {SERVER}")
    
    # run the server
    keep_running = True
    while keep_running:
        print("Running...")
        conn, addr = server.accept()
        keep_running = handle_interface(conn=conn, addr=addr)
    # end while

    print("Server Shutting Down!")
# end main


# handles a connection to the client
# if returns false, shut down server
def handle_interface(conn:socket.socket, addr)->bool:
    print(f"[NEW CONNECTION]: {addr} connected.")
    keep_server_running = True
    connected = True
    while connected:
        msg_length = conn.recv(params.HEADER).decode(params.FORMAT)
        if msg_length: # make sure that the message is an actual message
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(params.FORMAT)
            data = json.loads(msg)
            print(data["disconnect"])
            print(data["shutdown"])
            print(f"[{addr}]: {data}")
            print(f"[{addr}]: {data['payload']}")

            # check if we should disconnect
            if data["disconnect"] == True:
                print("Disconnecting...")
                connected = False
            # end if

            # check if we should close the server
            if data["shutdown"] == True:
                print("Shutting Down Server...")
                keep_server_running = False
            # end if
        # end if
    # end while
    conn.close()
    print("Connection Closed!")
    return keep_server_running
# end handle_client


if __name__ == "__main__":
    main()
