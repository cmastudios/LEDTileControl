# LEDTileControl
Controls RxC tiles of HxW WS2812 LEDs from a Raspberry Pi on one PWM pin.

![Imgur](https://i.imgur.com/1FKZu4g.jpg)

## Setting up the development environment

1. Download and install [Python 3](https://www.python.org/downloads/).
2. Optionally download an IDE like [PyCharm](https://www.jetbrains.com/pycharm/).
3. Clone this repo
4. From the cloned folder, run `pip3 install -r requirements.txt`

## Running patterns locally

For basic information, run `python3 run_pattern.py --help`. View a list of patterns by opening the patterns directory.

Running a pattern in the simulator: `python3 run_pattern.py --sim OpenCV patrickstar`   
Patterns with custom text: `python3 run_pattern.py --sim OpenCV text IEEE_is_better_than_DBF`   
Varying number of tiles: `python3 run_pattern.py --sim OpenCV --rows 5 --cols 6 fill`

# Pattern development

Create a new .py file in patterns. The name of the file will be the name of the pattern.
Populate it with the following function:

```python
def display(board, leds):
    pass
```

While your pattern is executing, this function will be called repeatedly.
Do not loop infinitely inside this function, otherwise shuffle playing patterns will not be possible.
Store any state variables as global variables in your pattern file.

The `board` parameter implements the following interface:
```python
class TileArray(object):
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
        pass
```

The `leds` parameter implements the following interface:

```python
class LEDStrip(object):
    def draw(self, image: np.ndarray, delay: float = 0.001):
    """
    Draws a matrix of color values to the dancefloor tiles. Handles the math of calculating what pixels
    correspond to which LEDs in the chain of LED strips. The input image should have a shape of
    (height, width, 3) where height is the LEDs in the vertical direction and width is the total LEDs in 
    the horizontal direction.
    :param image: Matrix of colors to display on the dancefloor
    :param delay: Seconds to wait after finishing writing to the LED strips
    """
    pass
```

Typically, these interfaces are used as following: (this also uses the numpy library)

```python
import numpy as np

def display(board, leds):
    # RGB color (black in this case, range is [0, 255] for each channel)
    color = (0, 0, 0)
    # create a image from the color spanning the entire dancefloor
    image = np.tile(color, board.shape)
    # draw this image and wait for 1/10th of a second
    leds.draw(image, 0.1)
```

## Making fancy patterns with numpy and OpenCV

Your image is just a matrix of color values, and as such it can be iterated across and modified with libraries
such as numpy and OpenCV.

```python
import numpy as np
# ...
image = np.tile((0, 0, 0), board.shape)

# Draw a diagonal white line
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        if y == x:
            image[y][x] = (255, 255, 255)
```

[OpenCV](https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html) has many drawing functions available.

```python
import numpy as np
import cv2
# ...
image = np.tile((0, 0, 0), board.shape)

# Draw a white circle at the center of the image
point = (board.shape[1] // 2, board.shape[0] // 2)  # (x,y) ordering
cv2.circle(image, point, 15, (255, 255, 255))

```

# Project creators

Patrick Naughton, Connor Monahan, Alex Herriott, Michael Greer   
IEEE Student Chapter, Washington University in St. Louis
