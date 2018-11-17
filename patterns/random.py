import numpy as np

def display(board, leds, delay=0.1):
    delay = float(delay)
    image = np.random.rand(board.shape[0], board.shape[1], 3)
    leds.draw(image, delay)