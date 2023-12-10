
import socket
import pickle
import numpy as np
from deepface import DeepFace
import cv2
from PIL import Image
from sklearn.linear_model import LogisticRegression

from cryptography.fernet import Fernet

import params
import messages as msgs
import biocapsule

MODEL = "ArcFace"

# load reference subject image
def load_ref_subj_feat_vector(path:str)->np.ndarray:
    # load image as a numpy array
    rs_image_arr = np.asarray(Image.open(path))

    # convert to feature vector
    rs_feature_vector = DeepFace.represent(
        img_path = rs_image_arr, 
        model_name = MODEL,
        enforce_detection=False,
        detector_backend="mtcnn"
    )[0]["embedding"] # end embedding retrieval

    rs_feature_vector = np.asarray(rs_feature_vector)
    print(len(rs_feature_vector))
    return rs_feature_vector
# end load_ref_subj_feat_vector


# generate a biocapsule for the user
def get_biocapsule(video_cap:cv2.VideoCapture, rs_feature_vector:np.ndarray)-> np.ndarray:
    # grab frame
    ret, frame = video_cap.read()
    # convert frame to feature vector
    user_feature = DeepFace.represent(
        img_path = frame, 
        model_name = MODEL,
        enforce_detection=False,
        detector_backend="mtcnn"
    )[0]["embedding"] # end embedding retrieval
   
    user_feature = np.asarray(user_feature)
    print(len(user_feature))
    # convert to biocapsule
    bc_gen = biocapsule.BioCapsuleGenerator()
    bc = bc_gen.biocapsule(user_feature=user_feature, rs_feature=rs_feature_vector)
    return bc
# end get_biocapsule


# load pkl file with face classifier data
def load_classifier(pkl_file_path:str):
    with open(pkl_file_path, "rb") as file:
        return pickle.load(file)
# end load_classifier


# does face authentication on client side
def face_auth_client(
    conn:socket.socket,
    sess_key:Fernet,
    video_cap:cv2.VideoCapture,
    rs_feature:np.ndarray)->bool:
    # generate biocapsule
    bc = get_biocapsule(video_cap=video_cap, rs_feature_vector=rs_feature) 

    # send reply back to server with biocapsule data
    data = msgs.get_msg_format()
    data["payload"] = params.BIOCAPSULE
    data["biocapsule"] = bc.tolist()
    msgs.send_msg_dict_encrypted(conn=conn, sess_key=sess_key, data=data)
# end face_auth_client


# authenticate the user's face on the server
def face_auth_server(classifier_model:LogisticRegression, bc:np.ndarray)->bool:
    bc = bc.reshape(1, -1)
    pred = classifier_model.predict_proba(bc)
    if pred[0][1] >= 0.5:
        return True
    return False
# end face_authenticate
