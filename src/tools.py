"""
    Secure Remote Desktop
    Edwin Sanchez

    tools.py

    This module contains code generally useful functions
    for other modules in this project.
"""

import io
import json
import math
import socket

from PIL import Image

MAX_BYTES = 1024

def main():
    pass


# collect useful data to send to the client
def send_data(conn:socket.socket, data:dict):
    # append the sending data with a flag
    # to tell that the data has started.
    # we're sending more than we can send in one go, so
    # it need to be in chunks.
    # we need the recvr to know how many chunks they're
    # recieving. post_stamp contains that data.
    
    # serialize data into a string
    data_str = json.dumps(data)
    
    # break into pieces of a maximum size
    chunks = []
    data_bytes = data_str.encode()
    num_bytes = len(data_bytes)
    num_chunks = math.ceil(num_bytes / MAX_BYTES)

    # generate chunks
    for i in range(num_bytes):
        start = i*MAX_BYTES
        end = min((i+1)*MAX_BYTES, num_bytes)
        chunk = data_bytes[start:end]
        chunks.append(chunk)
    # end for
    
    # create & send post stamp for data
    post_stamp = f"{num_chunks}".encode()
    conn.send(post_stamp)

    # send each chunk separately
    for chunk in chunks:
        conn.send(chunk)
    # end for
# end send_data


# parse the data that has been recieved.
def recv_data(conn:socket.socket)->dict:
    # get post stamp (must start with this)
    post_stamp = int(conn.recv(MAX_BYTES).decode())
    
    # parse data into a full string & convert back to dict
    data_str = ""
    for _ in range(post_stamp):
        data_str += conn.recv(MAX_BYTES).decode()
    # end for

    # convert the string back into a json dict
    data = json.loads(data_str)

    # return the data collected,
    # whether to end connection,
    # and whether to full-shutoff
    return data
# end recv_data


# convert PIL Image to a byte array to be sent over 
# an internet connection
def image_to_byte_array(image: Image.Image) -> bytes:
    # BytesIO is a file-like buffer stored in memory
    imgByteArr = io.BytesIO()
    # image.save expects a file-like as a argument
    image.save(imgByteArr, format=image.format)
    # Turn the BytesIO object back into a bytes object
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
# end image_to_byte_array


# convert PIL Image to a byte array to be sent over 
# an internet connection
def byte_array_to_image(bytes:str) -> Image.Image:
    byte_obj = bytes.encode()
    # image.save expects a file-like as a argument
    image = Image.open(byte_obj)
    return image
# end image_to_byte_array





if __name__ == "__main__":
    main()
