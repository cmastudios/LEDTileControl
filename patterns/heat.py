import numpy as np
import random


heat = None

frame = 0

def display(board, leds, extra):
    global heat, frame

    w = board.shape[1]
    h = board.shape[0]

    if heat is None:
        heat = np.zeros((h, w, 3))
        for x in range(w):
            for y in range(h):
                for c in range(3):
                    heat[y][x][c] = random.randint(128, 255)

    nextHeat = np.zeros((h, w, 3))

    if frame % 20 == 0:
        newX = random.randint(0, w-1)
        newY = random.randint(0, h-1)

        color = [random.randint(0, 255) for _ in range(3)]

        alpha = 0.6

        r = 15
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx * dx + dy * dy < r * r:
                    for c in range(3):
                        heat[(newY + dy) % h][(newX + dx) % w][c] = (int)(color[c] * alpha + (1 - alpha)*heat[(newY + dy) % h][(newX + dx) % w][c])

        nextHeat[newY][newX][1] = 255

    factor = 0.8

    for x in range(w):
        for y in range(h):
            for c in range(3):
                newVal = 0
                for dy in (-1, 1):
                    for dx in (-1, 1):
                        newVal += heat[(y + dy) % h][(x + dx) % w][c]

                nextHeat[y][x][c] = (int)((1-factor) * heat[y][x][c] + factor * newVal/4)



    heat = nextHeat

    leds.draw(heat, 0.03)

    frame += 1
    return



