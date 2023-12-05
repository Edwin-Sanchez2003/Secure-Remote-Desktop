"""
    Secure Remote Desktop
    Edwin Sanchez

    interface.py

    This module is run on the machine that 
    will be used to remote access another 
    machine. Once authenticated, this device
    will be able to remotely connect to the
    target device.

    This program acts as a 'Client' using
    python sockets.    
"""

import time

import socket

import argparse # for input parameters

# Parameter details #
prg_descr = """"""

# construct an argument parser
parser = argparse.ArgumentParser(
    prog='Interface',
    description=prg_descr
) # end ArgumentParser construction

# arguments to be passed in by the user via the command line/terminal
parser.add_argument('-p', '--port', choices=range(1024, 65535), type=int, default=6969, help="The port to use when connecting to the target device.")
parser.add_argument('-ip', "--ip_address", type=str, help="The ip address of the device you want to connect to.")


# get arguments from user
args = parser.parse_args()

# Constants
TARGET_PORT = args.port
HOST = args.ip_address


def main():
    # 0) Start up a client socket to connect to the server
    client_socket = init_client(host=HOST, port=TARGET_PORT)

    # busy work for a sec
    print("Doing Nothing...")
    time.sleep(5)
    print("Done.")
    client_socket.send("end".encode())

    client_socket.close()  # close the connection
# end main


# create a client socket, used to connect to the server
def init_client(host:str, port:int)-> socket.socket:
    client_socket = socket.socket()  # create client socket
    client_socket.connect((host, port))  # connect to the server
    client_socket.setblocking(1) # should wait if not recving data
    return client_socket



def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
# end client_program


if __name__ == "__main__":
    main()
    

