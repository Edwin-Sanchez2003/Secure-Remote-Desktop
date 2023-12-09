
import io
import copy
import json
import socket

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


import params

# MSG FORMAT #
MSG_FORMAT = {
    "payload": None,
    "screen_capture": None,
    "disconnect": False,
    "shutdown": False
} # end MSG_FORMAT dict


def main():
    pass


# gets a copy of the message format to use to fill with message data
def get_msg_format()->dict:
    return copy.deepcopy(MSG_FORMAT)


# sends a dictionary of data over a connection
def send_msg_dict(conn:socket.socket, data:dict)->None:
    # convert data to a string
    msg = json.dumps(data)
    send_msg(conn=conn, msg=msg)
# end send_msg_dict


# function for sending messages along a connection
def send_msg(conn:socket.socket, msg:str)->None:
    # prep message
    message = msg.encode(params.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(params.FORMAT)
    send_length += b' ' * (params.HEADER - len(send_length))
    
    # send message
    conn.send(send_length)
    conn.send(message)
# end send


# revieves a message as a dictionary along a connection
def recv_msg_dict(conn:socket.socket)->dict:
    # recieve a message
    msg = recv_msg(conn=conn)
    if msg == None:
        return None
    
    # convert to a dictionary
    data = json.loads(msg)
    return data
# end recv_msg_dict


# function for recieving messages
def recv_msg(conn:socket.socket)->str:
    msg_length = conn.recv(params.HEADER).decode(params.FORMAT)
    if msg_length: # make sure that the message is an actual message
        # recieve message
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(params.FORMAT)
        return msg
    # end if
    return None
# end recv_msg


# send image data over a connection
def send_msg_image(conn:socket.socket, image:Image.Image)->None:
    # prep message
    # convert to bytes then to a string 
    image_bytes = None
    with io.BytesIO() as output:
        image.save(output, format=params.IMG_FORMAT)
        image_bytes = output.getvalue()
    msg_length = len(image_bytes)
    send_length = str(msg_length).encode(params.FORMAT)
    send_length += b' ' * (params.HEADER - len(send_length))

    # send message
    conn.send(send_length)
    conn.send(image_bytes)
# end send_msg_image


# recieve image data over connection
def recv_msg_image(conn:socket.socket)-> Image.Image:
    msg_length = conn.recv(params.HEADER).decode(params.FORMAT)
    if msg_length: # make sure that the message is an actual message
        # recieve message
        msg_length = int(msg_length)
        image_bytes = conn.recv(msg_length)
        image = Image.open(io.BytesIO(image_bytes))
        return image
    # end if
    return None
# end recv_msg_image


if __name__ == "__main__":
    main()
