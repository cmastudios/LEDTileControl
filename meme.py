import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)
for i in range(-20, 100):
    img = np.tile([255,0,0], (10,10,1)).astype(np.uint8)
    cv2.putText(img, "IEEE", (-i, 8), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255))

    cv2.imshow("Test", img)
    cv2.waitKey(1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    leds.draw(img)
    time.sleep(0.1)
cv2.waitKey(5000)
