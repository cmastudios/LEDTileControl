import cv2


def display(board, leds, filename):
    # read in image
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # make the picture a square
    crop = image[0:image.shape[1], :, :]
    # fit picture to tile
    resize = cv2.resize(crop, board.shape[0:2])
    # display image
    leds.draw(resize, delay=10)
