import numpy as np

def display(board, leds, r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    image = np.tile((r, g, b), board.shape)

    leds.draw(image, delay=1)
