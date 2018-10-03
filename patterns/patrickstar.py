import random

import cv2
import numpy as np

last_color = (0, 0, 0)


def display(board, leds):
    global last_color
    spot = (random.randint(0, board.shape[1]), random.randint(0, board.shape[0]))
    color1 = [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    color2 = [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    color1 = [c / 1 for c in color1]
    color2 = [c / 1 for c in color2]
    for i in range(0, int(1.5 * board.shape[0])):
        img = np.tile(last_color, board.shape).astype(np.uint8)
        cv2.circle(img, (5, 5), i, color1, thickness=-1)
        cv2.circle(img, spot, i, color2, thickness=1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        leds.draw(img, delay=0.04)
    last_color = color1
