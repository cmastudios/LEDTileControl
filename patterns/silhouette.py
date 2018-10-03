import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
fgbg = cv2.createBackgroundSubtractorMOG2()
time.sleep(0.1)


def display(board, leds):
    # take picture
    camera.capture(rawCapture, format="rgb", use_video_port=True)
    image = rawCapture.array
    # make the picture a square
    crop = image[0:image.shape[1], :, :]
    # fit picture to tile
    resize = cv2.resize(crop, board.shape[0:2])
    # use patrick's algorithm
    fgmask = fgbg.apply(resize)
    next_frame = convert(fgmask)
    # display
    leds.draw(next_frame)
    rawCapture.truncate(0)


def convert(twoDArr):
    next_frame = np.zeros((len(twoDArr), len(twoDArr[0]), 3), np.uint8)
    for i in range(len(twoDArr)):
        for j in range(len(twoDArr[i])):
            for k in range(3):
                next_frame[i][j][k] = twoDArr[i][j]
    return next_frame
