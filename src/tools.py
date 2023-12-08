"""
    Secure Remote Desktop
    Edwin Sanchez

    tools.py

    This module contains code generally useful functions
    for other modules in this project.
"""

from io import BytesIO
import json
import socket
import base64

from PIL import Image

def main():
    pass


def send_image(sock, image):
    # Convert PIL image to bytes
    img_byte_array = BytesIO()
    image.save(img_byte_array, format="JPEG")
    img_bytes = img_byte_array.getvalue()

    # Convert bytes to base64-encoded string
    img_str = img_bytes.decode("base64")

    # Create a dictionary to store image information
    image_info = {
        "width": image.width,
        "height": image.height,
        "data": img_str
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(image_info)

    # Send the length of the JSON data first
    length = len(json_data)
    sock.sendall(length.to_bytes(4, byteorder='big'))

    # Send the actual JSON data
    sock.sendall(json_data.encode())


def send_data(conn:socket.socket, data:dict)-> None:
    # Convert data to bytes
    data_bytes = json.dumps(data).encode()

    # Send the length of the data first
    length = len(data_bytes)
    conn.sendall(length.to_bytes(4, byteorder='big'))

    # Send the actual data
    conn.sendall(data_bytes)

def recv_data(conn:socket.socket)-> dict:
    # Receive the length of the data
    length_bytes = conn.recv(4)
    length = int.from_bytes(length_bytes, byteorder='big')

    # Receive the actual data
    data_bytes = conn.recv(length)

    # Convert bytes to string then to dict
    data = json.loads(data_bytes.decode())

    return data

# convert PIL Image to a byte array to be sent over 
# an internet connection
def image_to_byte_array(image: Image.Image) -> str:
    output = io.BytesIO()
    image.save(output, format="png")
    image_as_string = base64.b64encode(output.getvalue()).hex()
    return image_as_string
# end image_to_byte_array


# convert PIL Image to a byte array to be sent over 
# an internet connection
def byte_array_to_image(byte_data:str) -> Image.Image:
    # image.save expects a file-like as a argument
    image = Image.open(io.BytesIO(base64.b64decode(bytes.fromhex(byte_data))))
    return image
# end image_to_byte_array





if __name__ == "__main__":
    main()
