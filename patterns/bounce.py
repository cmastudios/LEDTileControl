import numpy as np
import random
from helpers import hsl_to_rgb
from math import pi, atan

heights = None
velocities = None
t = 0
def display(board, leds, disturbances=1, height_range=10, omega_d=5, k=30, b=1, m=100, mode="hue"):
    global heights, velocities, t
    if heights is None:
        #heights = (np.random.rand(board.shape[0], board.shape[1])*height_range)-height_range/2
        heights = np.zeros((board.shape[0:2]))
    if velocities is None:
        velocities = np.zeros(board.shape[0:2])
    if t%omega_d == 0:
        for i in range(disturbances):
            row = random.randint(0, board.shape[0]-1)
            col = random.randint(0, board.shape[1]-1)
            heights[row][col] = random.choice((height_range/2, -height_range/2))
    accelerations = np.zeros(board.shape[0:2])
    for i in range(heights.shape[0]):
        for j in range(heights.shape[1]):
            accelerations[i][j] = compute_surroundings(i, j, heights, velocities, k, b, m)
    velocities += accelerations
    heights = heights + velocities
    img = np.zeros((board.shape[0], board.shape[1], 3), dtype=np.uint8)
    for i in range(heights.shape[0]):
        for j in range(heights.shape[1]):
            val = (atan(heights[i][j])*2/pi + 1)/2
            if mode == "hue":
                img[i][j] = hsl_to_rgb(val, 1, 0.5)
            else:
                img[i][j] = hsl_to_rgb(0.5, val, 0.5)
    t += 1
    leds.draw(img)
    
    
    
def compute_surroundings(row, col, heights, velocities, k, b, m):
    """
    Computes the sum of the neighboring cells and normalizes
    it with an arctan function.
    :param row: row of array
    :param col: col of array
    :param array: 2d numpy array representing current board
    """
    total = 0
    to_check = [
        [row-1, col-1],
        [row-1, col],
        [row-1, col+1],
        [row, col+1],
        [row+1, col+1],
        [row+1, col],
        [row+1, col-1],
        [row, col-1]
    ]
    for point in to_check:
        if 0 <= point[0] < heights.shape[0] and 0 <= point[1] < heights.shape[1]:
            total += k*(heights[point[0]][point[1]] - heights[row][col]) + b*(velocities[point[0]][point[1]] - velocities[row][col])
    return total/m
