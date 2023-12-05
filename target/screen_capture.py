"""
    Secure Remote Desktop
    Edwin Sanchez

    screen_capture.py

    This module contains code relevant to the
    target's screen capture. These screen captures
    are sent to the remote desktop user (interface.py),
    who can then see the current screen. 
"""

import pyautogui
from PIL.Image import Image

def main():
    # test data capture functionality
    for _ in range(5):
        data = get_local_device_data()
        for key, val in data.items():
            if key == "screenCap":
                val:Image
                val.save("./test/screen_shot.png")
            else: 
                print(f"{key}: {val}")
            # end if
        # end for
    # end for
# end main


# collects information on the local device &
# returns it in a neat package
def get_local_device_data()->dict:
    # Get the size of the primary monitor.
    screenWidth, screenHeight = pyautogui.size()
    
    # get the current mouse position
    currentMouseX, currentMouseY = pyautogui.position()

    # screenshot the screen
    screenCapture = pyautogui.screenshot()

    # package data in python dict
    data = {
        "width": screenWidth,
        "height": screenHeight,
        "mouseX": currentMouseX,
        "mouseY": currentMouseY,
        "screenCap": screenCapture
    } # end data

    return data
# end get_local_device_data


# end main


if __name__ == "__main__":
    main()
