import cv2
cam = cv2.VideoCapture(0)

def display(board, leds):
    global cam
    # take picture
    if cam.isOpened():
        cam.grab()
        _, image = cam.retrieve()
        # fit picture to tile
        resize = cv2.resize(image, (board.shape[1], board.shape[0]))
        resize = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
        # display
        leds.draw(resize)
