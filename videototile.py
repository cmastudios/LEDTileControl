import cv2
import tile
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    crop = image[0:image.shape[1], :, :]
    resize = cv2.resize(crop, (10, 10))

    resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)

#    gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
#    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#    resize = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


    leds.draw(resize)

    rawCapture.truncate(0)

    cv2.imshow('Output', resize)
    key = cv2.waitKey(1)
    if key == 27:
        break

print("Quitting application")
cv2.destroyAllWindows()
