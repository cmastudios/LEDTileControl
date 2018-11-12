import numpy as np
import time

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

    def size(self):
        return self.width * self.height


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
        return self.rows * self.height * self.cols * self.width

    @property
    def shape(self):
        """
        Gets the shape of the dancefloor. This is calculated from the --rows, --cols, --width, --height
        options.
        Examples:
        1 tile, 10x10 LEDs => board.shape == (10, 10, 1)
        5x6 tiles, 10x10 LEDs => board.shape == (50, 60, 1)
        :return: 3-tuple containing dimensions of tile matrix (height, width, channels)
        """
        return self.rows * self.height, self.cols * self.width, 1

    def tileindex(self, x, y):
        return x // self.width, y // self.height

    def index(self, x, y):
        tilex, tiley = self.tileindex(x, y)
        x, y = x % self.width, y % self.height
        tile = self.tiles[tiley][tilex]
        return tile.index(x, y) + tile.size() * tiley + tile.size() * self.rows * tilex


class LEDStrip(object):
    def __init__(self, array: TileArray):
        #from neopixel import Adafruit_NeoPixel
        # Create NeoPixel object with appropriate configuration.
        #self.strip = Adafruit_NeoPixel(array.size(), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                       #LED_CHANNEL)
        import io
        import fcntl
        self.write_stream = io.open("/dev/i2c-1", "wb", buffering=0)
        fcntl.ioctl(self.write_stream, 0x703, 0x66)
        # Intialize the library (must be called once before other functions).
        #self.strip.begin()
        self.array = array

    def draw(self, image: np.ndarray, delay: float = 0.001):
        """
        Draws a matrix of color values to the dancefloor tiles. Handles the math of calculating what pixels
        correspond to which LEDs in the chain of LED strips. The input image should have a shape of
        (height, width, 3) where height is the LEDs in the vertical direction and width is the total LEDs in
        the horizontal direction.
        :param image: Matrix of colors to display on the dancefloor
        :param delay: Seconds to wait after finishing writing to the LED strips
        """
        #from neopixel import Color
        packet_len = 225
        data = [0] * image.shape[0] * image.shape[1] * 3
        start = time.time()
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                idx = self.array.index(x, y)
                r = int(image[y][x][0])
                g = int(image[y][x][1])
                b = int(image[y][x][2])
                # 0 is an invalid code (for error checking)
                if r == 0:
                    r = 1
                if g == 0:
                    g = 1
                if b == 0:
                    b = 1
                data[3*idx] = r
                data[3*idx+1] = g
                data[3*idx+2] = b
                #color = Color(g, r, b)
                #self.strip.setPixelColor(idx, color)
        #self.strip.show()
        beg = 0
        end = packet_len
        while beg < len(data) - 1:
            try:
                self.write_stream.write(bytes(data[beg:end]))
            except Exception:
                self.write_stream.write(bytes(data[beg:]))
            beg += packet_len
            end += packet_len
        end = time.time()
        delta = end - start
        if delay > delta:
            time.sleep(delay - delta)


def has_been_closed(ax):
    import matplotlib.pyplot as plt
    fig = ax.figure.canvas.manager
    active_fig_managers = plt._pylab_helpers.Gcf.figs.values()
    return fig not in active_fig_managers


class LEDSimulatorCV(object):
    def __init__(self, array: TileArray):
        import cv2
        print("Opening LED Simulator (the window may appear minimized, check your taskbar)")

        self.cv = cv2
        self.cv.namedWindow("LEDs")

    def draw(self, image: np.ndarray, delay: float = 0.001):
        image = image.astype(np.uint8)
        image = self.cv.resize(image, (image.shape[1] * 10, image.shape[0] * 10))
        image = self.cv.cvtColor(image, self.cv.COLOR_RGB2BGR)
        self.cv.imshow("LEDs", image)
        key = self.cv.waitKey(int(delay * 1000))
        if key == 27:
            raise KeyboardInterrupt()


class LEDSimulatorMatplotlib(object):
    def __init__(self, array: TileArray):
        import matplotlib.pyplot as plt
        print("Opening LED Simulator/Matplotlib (the window may appear minimized, check your taskbar)")

        self.plt = plt
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(111)

    def draw(self, image: np.ndarray, delay: float = 0.001):
        self.axis.imshow(image)
        self.plt.pause(delay)
        if has_been_closed(self.axis):
            raise KeyboardInterrupt()
