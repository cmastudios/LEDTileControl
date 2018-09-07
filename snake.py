import cv2
import tile
import time
import numpy as np
from random import *

WIDTH = 10
HEIGHT = 10

board = tile.TileArray(rows=1, cols=1, height=HEIGHT, width=WIDTH)
leds = tile.LEDStrip(board)

def main():
    while True:
        b_color = (randint(0,200),randint(0,50),randint(0,50))
        f_color = (randint(0,100),randint(0,100),randint(150,255))
        start = (0, 0)
        lines = []
        for i in range(HEIGHT):
            if i%2 == 0:
                beg = 0 
                end = WIDTH
                step = 1
            else:
                beg = WIDTH - 1
                end = -1
                step = -1
            for j in range(beg, end, step):
                img = np.tile(b_color, (WIDTH, HEIGHT, 1)).astype(np.uint8)
                lines.append((start, (i, j)))
                for line in lines:
                    cv2.line(img, line[0], line[1],f_color, thickness=1)
                start = (i, j)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                leds.draw(img)
                time.sleep(0.1)

if __name__ == "__main__":
    main()
