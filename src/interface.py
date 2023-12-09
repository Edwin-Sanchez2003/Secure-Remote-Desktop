
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
    data = msgs.get_msg_format()
    data["payload"] = "Hello!"
    data["disconnect"] = True
    data["shutdown"] = True
    msgs.seng_msg_dict(conn=client, data=data)
# end main


if __name__ == "__main__":
    main()
