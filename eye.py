import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)

time.sleep(0.1)

img = cv2.imread("EYE.png")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
leds.draw(img)
time.sleep(0.1)





