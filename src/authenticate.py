
import json
import socket

import bcrypt

import params
import messages as msgs


# compose server tasks for authentication
def client_auth(conn:socket.socket)->None:
    # recv the challenge
    data = msgs.recv_msg_dict(conn=conn)
    if data["payload"] == params.CHALLENGE:
        # prompt user for password
        password = input("Please type in your password to authenticate:")

        # respond to challenge
        pass_salt = data["salt"]
        send_challenge_resp(conn=conn, password=password, pass_salt=pass_salt)
    # end if
# end client_auth


# compose client tasks for authentication
def server_auth(conn:socket.socket, path:str="./password.json")-> bool:
    # load the password from our file
    password = load_password(path=path)

    # send a challenge to the new connection
    pass_hash, _ = send_challenge(conn=conn, password=password)

    # accept or deny the connection
    data = msgs.recv_msg_dict(conn=conn)
    if data["payload"] == params.RESPONSE:
        recv_hash:str = data["hash"]
        recv_hash = recv_hash.encode(params.FORMAT)
        accept_deny_conn(conn=conn, pass_hash=pass_hash, recv_hash=recv_hash)
    # end if
# end server_auth


# loads the passwrod from the json file
def load_password(path:str)-> str:
    with open(path, "r") as file:
        pass_dict = json.load(file)
        return pass_dict["password"]
    # end open password json file
# end load_password


# send a challenge to the client
def send_challenge(conn:socket.socket, password:str)-> tuple[bytes, bytes]:
    # send challenge
    # generate one-time salt to send with challenge
    pass_salt = bcrypt.gensalt()
    data = msgs.get_msg_format()
    data["payload"] = params.CHALLENGE
    data["salt"] = pass_salt.decode(params.FORMAT)
    msgs.send_msg_dict(conn=conn, data=data)

    # take password & hash it, return the value
    pass_bytes = password.encode(params.FORMAT)
    pass_hash = bcrypt.hashpw(password=pass_bytes, salt=pass_salt)
    return (pass_hash, pass_salt)
# end send_challenge


# respond to challenge from server
def send_challenge_resp(conn:socket.socket, password:str, pass_salt:str)->None:
    # create hash of password, using the given salt
    pass_salt = pass_salt.encode(params.FORMAT)
    pass_bytes = password.encode(params.FORMAT)
    pass_hash = bcrypt.hashpw(password=pass_bytes, salt=pass_salt)

    # send hash back to server for verification
    data = msgs.get_msg_format()
    data["payload"] = params.RESPONSE
    data["hash"] = pass_hash.decode(params.FORMAT)
    msgs.send_msg_dict(conn=conn, data=data)
# end send_challenge_resp

    
# accept or deny the connection, based on the recieved password hash
def accept_deny_conn(conn:socket.socket, pass_hash:bytes, recv_hash:bytes)->None:
    # check to see if the hashes are the same
    # if not, break connection with client
    if pass_hash != recv_hash:
        conn.close()
    # end if
# end accept_deny_conn