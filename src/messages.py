
import json
import socket

import params


def main():
    pass


# sends a dictionary of data over a connection
def seng_msg_dict(conn:socket.socket, data:dict)->None:
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


if __name__ == "__main__":
    main()
