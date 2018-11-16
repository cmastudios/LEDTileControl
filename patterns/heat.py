import numpy as np
import random


heat = None

frame = 0

def display(board, leds, radius=10, period=10, smooth=0.2):
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

    try:
        mod = int(period)
    except:
        mod = 10

    if frame % mod == 0:
        newX = random.randint(0, w-1)
        newY = random.randint(0, h-1)

        color = [random.randint(0, 255) for _ in range(3)]

        alpha = 0.6

        try:
            r = int(radius)
        except:
            r = 10

        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx * dx + dy * dy < r * r:
                    for c in range(3):
                        heat[(newY + dy) % h][(newX + dx) % w][c] = (int)(color[c] * alpha + (1 - alpha)*heat[(newY + dy) % h][(newX + dx) % w][c])

        nextHeat[newY][newX][1] = 255

    try:
        s = float(smooth)
        if 0 <= s <= 1:
            factor = 1 - s
        else:
            raise Exception()
    except:
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

    leds.draw(heat, 0.001)

    frame += 1
    return



