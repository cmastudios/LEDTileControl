import numpy as np
from helpers import hsl_to_rgb
from math import sin, cos

last_time = 0

def display(board, leds, omega_t=0.05, omega_s=0.5, omega_c=0.5):
    global last_time
    img = np.zeros((board.shape[0], board.shape[1], 3), np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = hsl_to_rgb(
                0.5,
                (sin(-((omega_s * (i-board.shape[0]/2))**2 + (omega_c * (j-board.shape[1]/2))**2 ) **0.5 + omega_t * last_time)
                + 1)/2,
                0.5
            )
             
    last_time += 1
    leds.draw(img)
            
