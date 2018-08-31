import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)
while True:
	for i in range (0, 255, 5):
    		img = np.tile([i,255,255], (10,10,1)).astype(np.uint8)
    		img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    		leds.draw(img)
    		time.sleep(0.05)
    		img = np.tile([0,0,0], (10,10,1)).astype(np.uint8)
    		leds.draw(img)
    		time.sleep(0.05)




