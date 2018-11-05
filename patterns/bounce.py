import numpy as np
from math import pi

heights = None
velocities = None
def display(board, leds):
    if heights is None:
        heights = (np.rand(board.shape[0:1])*2)-1
    if velocities is None:
        velocities = np.zeros(board.shape[0:1])
    accelerations = np.zeros(board.shape[0:1])
    for i in range(heights.shape[0]):
        for j in range(heights.shape[1]):
            velocities[i][j] += compute_surroundings(i, j, heights)
    
    
    
def compute_surroundings(row, col, array):
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
        if 0 <= point[0] < array.shape[0] and 0 <= point[1] < array.shape[1]:
            total += array[point[0]][point[1]]
    return total
