import pyaudio
import struct
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = None

def display(board, leds):
    global stream
    if stream is None:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=board.shape[1])


    b = stream.read(board.shape[1], exception_on_overflow=False)
    s = struct.unpack("h" * board.shape[1], b)

    black = np.tile([0, 0, 0], board.shape).astype(np.uint8)
    for x in range(board.shape[1]):
        y = s[x] / 2**15 * board.shape[0] + board.shape[0] / 2
        y = int(y)
        if board.shape[0] > y >= 0:
            black[y][x] = [255, 255, 255]

    try:
        leds.draw(black, delay=0.003)
    except:
        stream.stop_stream()
        stream.close()
