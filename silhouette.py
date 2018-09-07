import numpy as np
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import tile

WIDTH = 10
HEIGHT = 10

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
fgbg = cv.createBackgroundSubtractorMOG2()

board = tile.TileArray(rows=1, cols=1, width=WIDTH, height=HEIGHT)
leds = tile.LEDStrip(board)

def main():
    global WIDTH, HEIGHT
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        frame = frame[0:frame.shape[1], :, :]
        frame = cv.resize(frame, (WIDTH, HEIGHT))
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        fgmask = fgbg.apply(frame)
        """next_frame = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
        print(frame)
        if frame is not None:
            fgmask = fgbg.apply(frame)
            for w in range(WIDTH):
                for h in range(HEIGHT):
                    pixel = avg_block(w*len(frame)//WIDTH, 
                      h*len(frame)//HEIGHT, fgmask)
                    next_frame[h][w] = pixel
            #cv.imshow('frame', fgmask)
            #cv.imshow('frame2', next_frame)
            leds.draw(next_frame)"""
        next_frame = convert(fgmask)
        leds.draw(next_frame)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        rawCapture.truncate(0)
    #cap.release()
    cv.destroyAllWindows()

def convert(twoDArr):
    next_frame = np.zeros((len(twoDArr), len(twoDArr[0]), 3), np.uint8)
    for i in range(len(twoDArr)):
        for j in range(len(twoDArr[i])):
            for k in range(3):
                next_frame[i][j][k] = twoDArr[i][j]
    return next_frame

def avg_block(b_start_x, b_start_y, frame):
    global WIDTH, HEIGHT
    if frame is not None:
        avg = 0
        for i in range(b_start_y, b_start_y + len(frame)//HEIGHT):
            for j in range(b_start_x, b_start_x + len(frame)//WIDTH):
                avg += frame[i][j]
        avg //= (len(frame)//WIDTH)*(len(frame)//HEIGHT)    
        return avg

if __name__ == "__main__":
    main()
