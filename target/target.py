"""
    Secure Remote Desktop
    Edwin Sanchez

    target.py

    This module is the module run on the target
    machine. Running this program will allow
    another machine to remotely connect to it, and
    once authenticated, remotely control it.

    This program acts as a 'Server' using python
    sockets.
"""

import socket

import argparse # for input parameters

# Parameter details #
prg_descr = """"""

# construct an argument parser
parser = argparse.ArgumentParser(
    prog='Target',
    description=prg_descr
) # end ArgumentParser construction

# arguments to be passed in by the user via the command line/terminal
parser.add_argument('-p', '--port', choices=range(1025, 65535), type=int, default=6969, help="The port to be used by this program on the target device.")

# get arguments from user
args = parser.parse_args()

# Constants
PORT = args.port
HOST = None
BYTE_COUNT = 1024


def main():
    # 0) Initialize the server.
    server_socket = init_server(port=PORT)

    # seamless connect & disconnect
    keepGoing = True
    while keepGoing:
        # 1)  Wait for connection
        conn, address = wait_for_connection(server_socket=server_socket)

        # 2) Loop during connection, doing work
        should_full_terminate:bool = do_things(conn=conn)

        # 3) The session has finished - close the connection
        print("Closing Connection!")
        conn.close()

        # 4) When terminate connection, check if
        #    user said to close completely. If
        #    yes, then close target.py program.
        if should_full_terminate:
            keepGoing = False
        # end if
    # end while
# end main


# wait for a connection from the client socket
def wait_for_connection(server_socket:socket.socket):
    print("Waiting for a Connection...")
    conn, address = server_socket.accept()  # accept new connection
    print(f"Connection from: {address}")
    return conn, address
# end wait_for_connection


# does things. place holder
def do_things(conn:socket.socket)-> bool:
    keepGoing = True
    while keepGoing:
        msg = conn.recv(BYTE_COUNT).decode()
        print(f"Message: {msg}")

        if msg == "end":
            print("Connection ended.")
            keepGoing = False
        # end if
    # end while

    # write connection logs???
    # good security practice I guess...

    return prompt_full_terminate()
# end do_things


# handles the task of asking if the 
# server process should be terminated
# completely (this process killed)
# if yes, server will not be able to connect
# until this process is re-started manually.
def prompt_full_terminate()-> bool:
    return False


# start up server socket
def init_server(port:int=5000)-> socket.socket:
    # get the hostname
    HOST = socket.gethostname()
    print(f"Host IP: {HOST}")

    # create a socket object instance
    server_socket = socket.socket()
    server_socket.bind((HOST, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    # ONLY ONE ALLOWED!!!
    server_socket.listen(1)

    # should wait if not recving data
    server_socket.setblocking(1)

    return server_socket
# end init_server


# send image data through UDP connection
def send_screen_capture():
    pass


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port number above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

if __name__ == "__main__":
    main()
    