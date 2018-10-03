import random

import numpy as np


def display(board, leds, delay=0.5):
    delay = float(delay)
    c1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    c2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
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
