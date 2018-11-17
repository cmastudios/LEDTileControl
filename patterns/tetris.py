import random

import numpy as np


class Tetromino(object):
    rotations = 0
    x = 0
    y = 0
    color = (0, 0, 0)
    shape = np.array([])

    def __init__(self, x=0, y=0, rotations=0):
        self.x = x
        self.y = y
        self.rotations = rotations

    def bounds_check(self, x, y, rotations, w, h, pieces):
        # render existing pieces to temporary board matrix
        board = np.zeros((h, w), np.uint8)
        for piece in pieces:
            if piece is not self:
                piece.rbinary(board)

        # check that the piece fits entirely within the
        shape = np.rot90(self.shape, k=rotations, axes=(1, 0))
        sw = shape.shape[1]
        sh = shape.shape[0]
        if x < 0 or y < 0 or x > w - sw or y > h - sh:
            return False

        # lastly check that no other piece intersects this one
        bslice = board[y:y + shape.shape[0], x:x + shape.shape[1]]
        return np.sum(np.bitwise_and(bslice, shape)) == 0

    def rbinary(self, board):
        shape = np.rot90(self.shape, k=self.rotations, axes=(1, 0))
        board[self.y:self.y + shape.shape[0], self.x:self.x + shape.shape[1]] = shape
        bslice = board[self.y:self.y + shape.shape[0], self.x:self.x + shape.shape[1]]
        board[self.y:self.y + shape.shape[0], self.x:self.x + shape.shape[1]] = np.bitwise_or(bslice, shape)

    def render(self, board):
        shape = np.rot90(self.shape, k=self.rotations, axes=(1, 0))
        bslice = board[self.y:self.y + shape.shape[0], self.x:self.x + shape.shape[1], :]
        colorshape = np.asarray(shape)[:, :, np.newaxis] * self.color
        # image_region = this OR original
        # OR is important - otherwise it will overwrite nearby tetrominos
        board[self.y:self.y + shape.shape[0], self.x:self.x + shape.shape[1], :] = np.bitwise_or(bslice, colorshape)


class I(Tetromino):
    color = (0, 255, 255)
    shape = np.matrix("1 1 1 1")

class J(Tetromino):
    color = (0, 0, 255)
    shape = np.matrix("1 1 1; 0 0 1")

class L(Tetromino):
    color = (255, 165, 0)
    shape = np.matrix("1 1 1; 1 0 0")

class O(Tetromino):
    color = (255, 255, 0)
    shape = np.matrix("1 1; 1 1")

class S(Tetromino):
    color = (0, 255, 0)
    shape = np.matrix("0 1 1; 1 1 0")

class T(Tetromino):
    color = (128, 0, 128)
    shape = np.matrix("1 1 1; 0 1 0")

class Z(Tetromino):
    color = (255, 0, 0)
    shape = np.matrix("1 1 0; 0 1 1")

pieces = (I, J, L, O, S, T, Z)
p = None
placed = []
stuckc = 0
iteration = 0

def display(board, leds, delay=0.01, skip=1):
    global p, placed, stuckc, iteration
    delay = float(delay)
    skip = int(skip)
    image = np.tile([0, 0, 0], board.shape).astype(np.uint8)

    # reset when full
    if stuckc > 20:
        stuckc = 0
        placed = []
        p = None

    # generate a new piece
    if p is None:
        p = random.choice(pieces)(random.randint(0, board.shape[1]), 3, random.randint(0, 3))
        if p.bounds_check(p.x, p.y, p.rotations, board.shape[1], board.shape[0], placed):
            # it fits
            placed.append(p)
            stuckc = 0
        else:
            # it doesn't fit
            stuckc += 1
            return

    # try to move it downwards
    if p.bounds_check(p.x, p.y + 1, p.rotations, board.shape[1], board.shape[0], placed):
        # actually move it down
        p.y += 1
    else:
        # generate a new piece the next iteration
        p = None

    # draw all tetrominos
    for pi in placed:
        pi.render(image)

    iteration += 1
    if iteration % skip == 0:
        leds.draw(image, delay)

