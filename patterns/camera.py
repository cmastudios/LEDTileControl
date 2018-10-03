import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)


def display(board, leds):
    # take picture
    camera.capture(rawCapture, format="rgb", use_video_port=True)
    image = rawCapture.array
    # make the picture a square
    crop = image[0:image.shape[1], :, :]
    # fit picture to tile
    resize = cv2.resize(crop, board.shape[0:2])
    # display
    leds.draw(resize)
    rawCapture.truncate(0)
