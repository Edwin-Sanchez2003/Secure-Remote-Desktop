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

import remote_desktop as rd # functionality for remote desktop
import tools # useful functions that could be used anywhere

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
        should_full_terminate:bool = execution(conn=conn)

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


# sends & recvs data to & from interface program
def execution(conn:socket.socket)-> bool:
    # loop until a command to end is given
    keepGoing = True
    recv_data = None
    while keepGoing:
        # send data
        send_data = rd.get_local_device_data()
        tools.send_data(conn=conn, data=send_data)

        # recv data
        recv_data = tools.recv_data(conn=conn)

        # whether to continue
        keepGoing = recv_data["session"]
    # end while

    # write connection logs???
    # good security practice I guess...

    # return whether we should only terminate
    # the session or fully terminate
    return recv_data["full"]
# end do_things


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


if __name__ == "__main__":
    main()
    