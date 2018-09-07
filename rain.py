import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import random


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)


time.sleep(0.1)

while True:
    img = np.tile((0,0,0), (10,10,1)).astype(np.uint8)

    points = [(5,9), (2, 4)]
    for i in range(400):
        newpts = []
        for x, y in points:
            if y == 0 or img[x][y-1][0] > 0:
                x = random.randint(0, 9)
                y = 9
                newpts.append((x, y))
            else:
                img[x][y] = (0,0,0)
                y -= 1
                newpts.append((x, y))
#            img[x][y] = (255,255,255)
            img[x][y] = (255, 192, 203)
           # img[x][y] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        points = newpts
        leds.draw(img)
        time.sleep(0.0051)

    for i in range(400):
        newpts = []
        for x, y in points:
            if y == 0 or img[x][y-1][0] == 0:
                x = random.randint(0, 9)
                y = 9
                newpts.append((x, y))
            else:
                img[x][y] = (255,255,255)
                y -= 1
                newpts.append((x, y))
            img[x][y] = (0,0,0)
        points = newpts
        leds.draw(img)
        time.sleep(0.0051)
