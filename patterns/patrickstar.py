import random

import cv2
import numpy as np

import helpers

last_color = (0, 0, 0)


def display(board, leds, delay=0.1):
    global last_color
    delay = float(delay)
    spot = (random.randint(0, board.shape[1]), random.randint(0, board.shape[0]))
    hue = random.random()
    hue2 = hue + 0.37
    hue2 = hue2 if hue2 < 1 else hue2 - 1
    color1 = helpers.hsl_to_rgb(hue, 1, 0.5)
    color2 = helpers.hsl_to_rgb(hue2, 1, 0.5)
    for i in range(0, int(1.5 * board.shape[0])):
        img = np.tile(last_color, board.shape).astype(np.uint8)
        cv2.circle(img, (5, 5), i, color1, thickness=-1)
        cv2.circle(img, spot, i, color2, thickness=1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        leds.draw(img, delay=delay)
    last_color = color1
