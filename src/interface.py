
import json
import socket

from cryptography.fernet import Fernet
import cv2

import params
import messages as msgs
import security

SERVER = "192.168.56.1"
ADDR = (SERVER, params.PORT)


def main():
    # open camera
    video_cap:cv2.VideoCapture = cv2.VideoCapture(0)
    # get reference subject data
    rs_feature_vector = security.face_authentication.load_ref_subj_feat_vector(path="./rs_00.jpg")

    # initialize interface
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    # establish session key
    sess_key:Fernet = security.session.gen_session_client(conn=client)

    # authenticate
    security.authenticate.client_auth(conn=client)

    # begin use-loop
    keep_connection = True
    counter = 0
    test_counts = 30
    while keep_connection:
        counter += 1
        print(f"Counter: {counter} of {test_counts}")
        # send instructions
        data = msgs.get_msg_format()
        data["payload"] = "Hello!"
        if counter <= test_counts:
            data["disconnect"] = False
            data["shutdown"] = False
        else:
            data["disconnect"] = True
            data["shutdown"] = True
            keep_connection = False
        msgs.send_msg_dict_encrypted(conn=client, sess_key=sess_key, data=data)

        # recieve image data & update UI
        image = msgs.recv_msg_image(conn=client)
        
        # if type is bytes, then it isn't an image, it's a biocapsule message
        # load the data
        if type(image) is bytes:
            msg_bytes = sess_key.decrypt(image)
            msg = msg_bytes.decode(params.FORMAT)
            bc_req = json.loads(msg)
            if bc_req["payload"] == params.BIOCAPSULE:
                security.face_authentication.face_auth_client(
                    conn=client,
                    sess_key=sess_key,
                    video_cap=video_cap,
                    rs_feature=rs_feature_vector
                ) # end face_auth_client
            # end if
        else:
            while image is None:
                image = msgs.recv_msg_image(conn=client)
            image.save(f"../test/screenshot_{counter}.png")
        # end if
    # end of connection

    # After the loop release the video_cap object 
    video_cap.release()
    # Destroy all the windows 
    cv2.destroyAllWindows() 
# end main


if __name__ == "__main__":
    main()
