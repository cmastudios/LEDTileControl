import cv2

cap = None

def display(board, leds, filename):
    global cap
    if cap is None:
        cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        raise RuntimeError('Failed to open video file {}'.format(filename))

    # Capture frame-by-frame
    ret, frame = cap.read()

    # fit picture to tile
    resize = cv2.resize(frame, board.shape[0:2])
    resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)

    # display image
    leds.draw(resize, delay=0.04)

