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


import socket

import pygame
from PIL.Image import Image

import tools

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
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    # 0) initialize pygame display
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # 1) Start up a client socket to connect to the server
    client_socket = init_client(host=HOST, port=TARGET_PORT)

    # 2) begin displaying screen
    execution(conn=client_socket, screen=screen)

    # 3) once done, close connection
    client_socket.close()

    # 4) close pygame window
    pygame.quit()
# end main


# sends & recvs data to & from target program
def execution(conn:socket.socket, screen:pygame.Surface)-> None:
    # loop until a command to end is given
    keepGoing = True
    recv_data = None
    while keepGoing:
        # send data
        send_data = {
            "session": True,
            "full": False
        } # end send_data
        tools.send_data(conn=conn, data=send_data)

        # recv data
        recv_data = tools.recv_data(conn=conn)

        # display
        display(
            image=tools.byte_array_to_image(bytes=recv_data["screenCap"]),
            screen=screen
        ) # end display
        
        # whether to continue
        keepGoing = user_initiate_end()
    # end while

    # send session end to server
    send_data = {
        "session": False,
        "full": False
    } # end send_data
    tools.send_data(conn=conn, data=send_data)

    # write connection logs???
    # good security practice I guess...
# end do_things


# display images for user
def display(image:Image, screen:pygame.Surface):
    # convert PIL image to pygame image
    mode = image.mode
    size = image.size
    data = image.tobytes()
    py_image = pygame.image.fromstring(data, size, mode)

    # create rectangle to define where image goes
    rect = py_image.get_rect()
    rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

    # Set the background color 
    bckgrnd_color = (255, 255, 255)

    # set screen info
    screen.fill(bckgrnd_color) 
    screen.blit(py_image, rect)
      
    # Update the GUI pygame 
    pygame.display.update() 
# end display


# initiate the end of the program - close
def user_initiate_end()-> bool:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False


# create a client socket, used to connect to the server
def init_client(host:str, port:int)-> socket.socket:
    client_socket = socket.socket()  # create client socket
    client_socket.connect((host, port))  # connect to the server
    client_socket.setblocking(1) # should wait if not recving data
    return client_socket




if __name__ == "__main__":
    main()
    

