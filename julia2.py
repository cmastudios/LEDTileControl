import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import random


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)


img = np.tile([0,0,0], (10,10,1)).astype(np.uint8)

while True:
	color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	img = np.tile([0,0,0], (10,10,1)).astype(np.uint8)
	for i in range(10) :
		for j in range(10) :	
			img[i][j] = color
			leds.draw(img)
			time.sleep(0.05)

	for i in range(3):
		img = np.tile([0,0,0], (10,10,1)).astype(np.uint8)
		leds.draw(img)
		time.sleep(0.2)
		img = np.tile(color, (10,10,1)).astype(np.uint8)
		leds.draw(img)
		time.sleep(0.2)

