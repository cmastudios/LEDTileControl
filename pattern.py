import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import random

board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)
last_color = (0,0,0)
while True:
    spot = (random.randint(0, 10), random.randint(0, 10))
    color1 = [random.randint(0, 256), random.randint(0, 256), random.randint(0,256)]
    color2 = [random.randint(0, 256), random.randint(0, 256), random.randint(0,256)]
    color1 = [c/1 for c in color1];
    color2 = [c/1 for c in color2];
    for i in range(0,15): 
        img = np.tile(last_color, (10,10,1)).astype(np.uint8)
        cv2.circle(img, (5,5), i, color1, thickness=-1)
        #cv2.circle(img, (5,5), i+5, color1)
        cv2.circle(img, spot, i, color2, thickness=1) 
        
    #    cv2.imshow("Test", img)
#        cv2.waitKey(1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        leds.draw(img)
        time.sleep(0.1)
    last_color = color1
