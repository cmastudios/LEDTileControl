import cv2
import numpy as np

i = 0


def display(board, leds, delay=0.05):
    """
    Rainbow rave pattern by Julia
    :param board:
    :param leds:
    :param delay:
    """
    global i
    delay = float(delay)
    img = np.tile([i, 255, 255], board.shape).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    leds.draw(img, delay=delay)
    img = np.tile([0, 0, 0], board.shape).astype(np.uint8)
    leds.draw(img, delay=delay)
    i += 5
    if i > 255:
        i = 0
