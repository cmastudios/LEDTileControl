import numpy as np

from config import *


class Tile(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def index(self, x, y):
        # snake order
        if y % 2 == 0:
            # moving to the right
            return self.width * y + x
        else:
            # moving to the left
            return self.width * y + (self.width - x - 1)


class TileArray(object):
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.tiles = []
        for row in range(rows):
            elems = []
            for col in range(cols):
                elems.append(Tile(width, height))
            self.tiles.append(elems)

    def size(self):
        return self.rows * self.height + self.cols * self.width

    def tileindex(self, x, y):
        return x // self.width, y // self.height

    def index(self, x, y):
        tilex, tiley = self.tileindex(x, y)
        tile = self.tiles[tiley][tilex]
        return tile.index(x, y)


class LEDStrip(object):
    def __init__(self, array:TileArray):
        from neopixel import Adafruit_NeoPixel
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(array.size(), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.array = array

    def draw(self, image:np.ndarray):
        from neopixel import Color
        for y in image.shape[0]:
            for x in image.shape[1]:
                idx = self.array.index(x, y)
                color = Color(image[y][x][0], image[y][x][1], image[y][x][2])
                self.strip.setPixelColor(idx, color)
        self.strip.show()