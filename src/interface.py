
import time
import socket

import params
import messages as msgs

SERVER = "192.168.56.1"
ADDR = (SERVER, params.PORT)



def main():
    # initialize interface
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    # authenticate

    # establish session key

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
        msgs.send_msg_dict(conn=client, data=data)

        # recieve image data & update UI
        image = msgs.recv_msg_image(conn=client)
        while image is None:
            image = msgs.recv_msg_image(conn=client)
        image.save(f"../test/screenshot_{counter}.png")

# end main


if __name__ == "__main__":
    main()
