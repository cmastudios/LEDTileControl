from random import randint

import cv2
import numpy as np


def display(board, leds):
    b_color = (randint(0, 200), randint(0, 50), randint(0, 50))
    f_color = (randint(0, 100), randint(0, 100), randint(150, 255))
    start = (0, 0)
    lines = []
    for i in range(board.shape[0]):
        if i % 2 == 0:
            beg = 0
            end = board.shape[1]
            step = 1
        else:
            beg = board.shape[1] - 1
            end = -1
            step = -1
        for j in range(beg, end, step):
            img = np.tile(b_color, board.shape).astype(np.uint8)
            lines.append((start, (i, j)))
            for line in lines:
                cv2.line(img, line[0], line[1], f_color, thickness=1)
            start = (i, j)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            leds.draw(img, delay=0.1)
