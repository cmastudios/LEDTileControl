import cv2
import numpy as np

i = 0


def display(board, leds, message="IEEE", increment=1, delay=0.1, fsize=None):
    global i
    message = message.replace("_", " ")
    increment = int(increment)
    delay = float(delay)
    if fsize is None:
        fsize = 0.075 * board.shape[0]
    else:
        fsize = float(fsize)
    # create blue canvas
    img = np.tile([0, 0, 255], board.shape).astype(np.uint8)
    # draw red message
    cv2.putText(img, message, (board.shape[1] - i, board.shape[0] - 2), cv2.FONT_HERSHEY_PLAIN, fsize,
                (255, 0, 0), int(0.1 * board.shape[0]))
    # display
    leds.draw(img, delay=delay)
    # move message across the screen
    i += increment
    if i > len(message)*10*0.1 * board.shape[0]:
        i = 0
