import numpy as np
import random
from math import pi, atan

heights = None
velocities = None
def display(board, leds, disturbances=1, height_range=10):
    global heights, velocities
    if heights is None:
        #heights = (np.random.rand(board.shape[0], board.shape[1])*height_range)-height_range/2
        heights = np.zeros((board.shape[0:2]))
    if velocities is None:
        velocities = np.zeros(board.shape[0:2])
    for i in range(disturbances):
        row = random.randint(0, board.shape[0]-1)
        col = random.randint(0, board.shape[1]-1)
        heights[row][col] = random.choice((height_range/2, -height_range/2))
    accelerations = np.zeros(board.shape[0:2])
    for i in range(heights.shape[0]):
        for j in range(heights.shape[1]):
            accelerations[i][j] = compute_surroundings(i, j, heights, velocities, 1, 1, 10)
    velocities += accelerations
    heights = heights + velocities
    img = np.zeros((board.shape[0], board.shape[1], 3), dtype=np.uint8)
    for i in range(heights.shape[0]):
        for j in range(heights.shape[1]):
            val = int(((atan(heights[i][j])*2/pi + 1)/2) * 256)
            img[i][j] = (val, val, val)
    leds.draw(img, delay=0.1)
    
    
    
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
