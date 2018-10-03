#!/usr/bin/env python3
import argparse
import importlib

import numpy as np

import tile


def run_pattern(board, leds, pattern, extra_args):
    pattern = importlib.import_module("patterns." + pattern)

    try:
        while True:
            pattern.display(board, leds, *extra_args)
    except KeyboardInterrupt:
        # black the display
        black = np.tile([0, 0, 0], board.shape).astype(np.uint8)
        try:
            leds.draw(black)
            del leds
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display a pattern on the dancefloor')
    parser.add_argument('pattern', help='Name of pattern file')
    parser.add_argument('extra_args', help='Arguments for the pattern', nargs='*')
    parser.add_argument('--rows', help='Number of tile rows', type=int, default=1)
    parser.add_argument('--cols', help='Number of tile columns', type=int, default=1)
    parser.add_argument('--height', help='LEDs per tile row', type=int, default=10)
    parser.add_argument('--width', help='LEDs per tile column', type=int, default=10)
    parser.add_argument('--sim', help='Simulation strategy', choices=('OpenCV', 'Matplotlib'))

    args = parser.parse_args()

    board = tile.TileArray(rows=args.rows, cols=args.cols, height=args.height, width=args.width)
    if args.sim == 'OpenCV':
        leds = tile.LEDSimulatorCV(board)
    elif args.sim == 'Matplotlib':
        leds = tile.LEDSimulatorMatplotlib(board)
    else:
        leds = tile.LEDStrip(board)

    run_pattern(board, leds, args.pattern, args.extra_args)
