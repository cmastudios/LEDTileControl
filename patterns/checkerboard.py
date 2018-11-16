import random

import numpy as np
import helpers


def display(board, leds, delay=0.5):
    delay = float(delay)
    hue = random.random()
    hue2 = hue + 0.37
    hue2 = hue2 if hue2 < 1 else hue2 - 1
    c1 = helpers.hsl_to_rgb(hue, 1, 0.5)
    c2 = helpers.hsl_to_rgb(hue2, 1, 0.5)
    image = np.tile(c1, board.shape).astype(np.uint8)
    for ty in range(board.rows):
        for tx in range(board.cols):
            ystart = ty * board.height
            yend = (ty + 1) * board.height
            xstart = tx * board.width
            xend = (tx + 1) * board.width
            if (ty + tx) % 2 == 0:
                image[ystart:yend, xstart:xend] = c2
    leds.draw(image, delay=delay)
