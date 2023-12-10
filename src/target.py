
import time
import socket

from cryptography.fernet import Fernet
import pyautogui
import numpy as np

import params
import messages as msgs
import security

SERVER = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
ADDR = (SERVER, params.PORT)


def main():
    # initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR) # use specified server & port
    server.listen(1) # only allow 1 connection at a time
    print(f"[LISTENING]: Server is listening on {SERVER}")
    
    # run the server
    keep_running = True
    while keep_running:
        print("Running...")
        conn, addr = server.accept()

        # create session key
        sess_key:Fernet = security.session.gen_session_server(conn=conn)
        
        # authenticate
        security.authenticate.server_auth(conn=conn, path="./data.json")

        keep_running = handle_interface(conn=conn, addr=addr, sess_key=sess_key)
    # end while

    print("Server Shutting Down!")
# end main


# handles a connection to the client
# if returns false, shut down server
def handle_interface(conn:socket.socket, addr, sess_key:Fernet)->bool:
    # create a timer for face authentication
    start_time = time.time()
    current_time = start_time
    classifier_model = security.face_authentication.load_classifier(pkl_file_path="./edwin_classifier.pkl")

    print(f"[NEW CONNECTION]: {addr} connected.")
    keep_server_running = True
    connected = True
    while connected:
        data = msgs.recv_msg_dict_encrypted(conn=conn, sess_key=sess_key)
        if data: # if data exists...
            print(f"[{addr}]: {data}")
            print(f"[{addr}]: {data['payload']}")

            # send screen capture data
            screen_capture = pyautogui.screenshot()
            msgs.send_msg_image(conn=conn, image=screen_capture)

            # request face authentication
            current_time = time.time()
            if current_time >= params.FACE_AUTH_DELAY_SEC:
                # send request to authenticate using biocapsule
                req_bc = msgs.get_msg_format()
                req_bc["payload"] = params.BIOCAPSULE
                print("Req BC...")
                msgs.send_msg_dict_encrypted(conn=conn, sess_key=sess_key, data=req_bc)
                bc_resp = msgs.recv_msg_dict_encrypted(conn=conn, sess_key=sess_key)
                while bc_resp["payload"] != params.BIOCAPSULE:
                    bc_resp = msgs.recv_msg_dict_encrypted(conn=conn, sess_key=sess_key)
                bc = np.asarray(bc_resp["biocapsule"])
                auth_decision = security.face_authentication.face_auth_server(
                    classifier_model=classifier_model, bc=bc
                ) # end authentication decision
                if auth_decision == False:
                    connected = False
                # end if
            # end if

            # check if we should disconnect
            if data["disconnect"] == True:
                print("Disconnecting...")
                connected = False
            # end if

            # check if we should close the server
            if data["shutdown"] == True:
                print("Shutting Down Server...")
                keep_server_running = False
            # end if
        # end if
    # end while
    conn.close()
    print("Connection Closed!")
    return keep_server_running
# end handle_client


if __name__ == "__main__":
    main()
