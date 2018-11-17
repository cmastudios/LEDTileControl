import random
import numpy as np

iteration = 0

def display(board, leds, pixeldelay=0.05, flashdelay=0.2, skip=0):
    global iteration
    pixeldelay = float(pixeldelay)
    flashdelay = float(flashdelay)
    skip = int(skip)


    # pick a random color
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # make an empty, black canvas
    img = np.tile([0, 0, 0], board.shape).astype(np.uint8)
    # draw color on the canvas pixel by pixel
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            img[i][j] = color
            if iteration % skip == 0:
                leds.draw(img, delay=pixeldelay)
            iteration += 1

    # disco flash the tile
    for i in range(3):
        img = np.tile([0, 0, 0], board.shape).astype(np.uint8)
        leds.draw(img, delay=flashdelay)
        img = np.tile(color, board.shape).astype(np.uint8)
        leds.draw(img, delay=flashdelay)
