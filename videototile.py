import cv2
import tile

board = tile.TileArray(rows=1, cols=1, height=10, width=10)
leds = tile.LEDStrip(board)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    cap.grab()
    _, image = cap.retrieve()

    crop = image[0:image.shape[1], :, :]
    resize = cv2.resize(crop, (10, 10))
    leds.draw(resize)

    cv2.imshow('Output', resize)
    key = cv2.waitKey(1)
    if key == 27:
        break


cv2.destroyAllWindows()
