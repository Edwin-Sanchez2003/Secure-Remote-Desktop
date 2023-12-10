
import socket

import params
import messages as msgs

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


# CLIENT #
def gen_session_client(conn:socket.socket)->Fernet:
    # recv public key from server
    data = msgs.recv_msg_dict(conn=conn)
    server_pub_key:rsa.RSAPublicKey = None
    if data["payload"] == params.PUBLIC_KEY:
        server_pub_key_str:str = data["public"]
        server_pub_key_bytes = server_pub_key_str.encode(params.FORMAT)
        server_pub_key:rsa.RSAPublicKey = load_pem_public_key(server_pub_key_bytes)
    # end if

    # generate public key & send to server
    private_key = gen_and_send_asym_key(conn=conn)

    # recv session key & verify from server
    signature = msgs.recv_session_key(conn=conn)
    sess_key_encrypted = msgs.recv_session_key(conn=conn)
    print(sess_key_encrypted)
    
    # get signature
    server_pub_key.verify(
        signature,
        sess_key_encrypted,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    ) # end verification of signature
    
    # get session key
    sess_key = private_key.decrypt(
        sess_key_encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    print(sess_key)
    sess_key = Fernet(key=sess_key)
    return sess_key
# end gen_session_client


# SERVER #

# generates a session between the client & the server
# creates a session key to use for encryption
def gen_session_server(conn:socket.socket)->Fernet:
    # send public key to client
    private_key = gen_and_send_asym_key(conn=conn)

    # recv public key from client
    data = msgs.recv_msg_dict(conn=conn)
    client_pub_key:rsa.RSAPublicKey = None
    if data["payload"] == params.PUBLIC_KEY:
        # get public key
        client_public_key_str:str = data["public"]
        client_public_key_bytes = client_public_key_str.encode(params.FORMAT)
        client_pub_key:rsa.RSAPublicKey = load_pem_public_key(client_public_key_bytes)
    # end if

    # generate session key & send to client (signed)
    session_key = gen_and_sign_and_send_session_key(conn=conn,
                                                    private_key=private_key,
                                                    client_pub_key=client_pub_key)
    return session_key
# end gen_session_server


# generate session key and send to client using our private key
# make sure to sign message
def gen_and_sign_and_send_session_key(conn:socket.socket,
                                      private_key:rsa.RSAPrivateKey,
                                      client_pub_key:rsa.RSAPublicKey)->Fernet:
    # generate session key
    sess_bytes, session_key = gen_session_key()
    session_key_bytes = session_key._encryption_key
    print(session_key_bytes)
    # encrypt session key
    session_key_encrypted_bytes:bytes = client_pub_key.encrypt(
        sess_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))

    # sign session key
    signature = private_key.sign(
        session_key_encrypted_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    ) # end signature

    # send msg
    msgs.send_session_key(conn=conn, session_key=signature)
    print(session_key_encrypted_bytes)
    msgs.send_session_key(conn=conn, session_key=session_key_encrypted_bytes)
    return session_key
# end gen_and_sign_and_seng_session_key


# create an asymmetric key & send public key to client/server
def gen_and_send_asym_key(conn:socket.socket)->rsa.RSAPrivateKey:
    private_key = gen_asymmetric_key()
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ) # end public_key_bytes
    public_key_str = public_key_bytes.decode(params.FORMAT)
    data = msgs.get_msg_format()
    data["payload"] = params.PUBLIC_KEY
    data["public"] = public_key_str
    msgs.send_msg_dict(conn=conn, data=data)
    return private_key
# end gen_and_send_asym_key


# generate public key
def gen_asymmetric_key()->rsa.RSAPrivateKey:
    private_key:rsa.RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    ) # end generate_private_key
    return private_key
# end gen_asymmetric_key


# create session key
def gen_session_key(key:bytes=None)->tuple[bytes, Fernet]:
    if key == None: # if key is not given generate one
        key = Fernet.generate_key()
    session_key = Fernet(key=key)
    return (key, session_key)
# gen_session_key
