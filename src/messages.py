
import io
import copy
import json
import socket

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from cryptography.fernet import Fernet

import params

# MSG FORMAT #
MSG_FORMAT = {
    "payload": None,
    "salt": None,
    "hash": None,
    "public": None,
    "session": None,
    "signature": None,
    "disconnect": False,
    "shutdown": False
} # end MSG_FORMAT dict


def main():
    pass


# gets a copy of the message format to use to fill with message data
def get_msg_format()->dict:
    return copy.deepcopy(MSG_FORMAT)

# send encrypted msgs
def send_msg_dict_encrypted(conn:socket.socket, sess_key:Fernet, data:dict)->None:
    # encrypt data using session key
    data_bytes = json.dumps(data).encode(params.FORMAT)
    encrypted_data_bytes = sess_key.encrypt(data=data_bytes)
    encrypted_data_str = encrypted_data_bytes.decode(params.FORMAT)
    send_msg(conn=conn, msg=encrypted_data_str)
# end send_msg_dict_encrypted


# recieve encrypted data & decrypt into a dictionary
def recv_msg_dict_encrypted(conn:socket.socket, sess_key:Fernet)-> dict:
    # recieve a message
    msg_encrypted_str = recv_msg(conn=conn)
    if msg_encrypted_str == None:
        return None
    
    # decrypt msg
    msg_encrypted_bytes = msg_encrypted_str.encode(params.FORMAT)
    msg_bytes = sess_key.decrypt(msg_encrypted_bytes)
    msg = msg_bytes.decode(params.FORMAT)
    data = json.loads(msg)
    return data
# end recv_msg_dict_encrypted


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


# send the session key as bytes
def send_session_key(conn:socket.socket, session_key:bytes)->None:
    # prep message
    msg_length = len(session_key)
    send_length = str(msg_length).encode(params.FORMAT)
    send_length += b' ' * (params.HEADER - len(send_length))
    
    # send message
    conn.send(send_length)
    conn.send(session_key)
# end send


# function for recieving session key as bytes
def recv_session_key(conn:socket.socket)->bytes:
    msg_length = conn.recv(params.HEADER).decode(params.FORMAT)
    if msg_length: # make sure that the message is an actual message
        # recieve message
        msg_length = int(msg_length)
        session_key = conn.recv(msg_length)
        return session_key
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
    msg_length = None
    try:
        msg_length = conn.recv(params.HEADER).decode(params.FORMAT)
    except UnicodeDecodeError:
        return None
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
