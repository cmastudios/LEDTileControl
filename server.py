import multiprocessing
from flask import Flask, request, redirect, render_template
import run_pattern
import tile
import pkgutil

app = Flask("LEDServer")

rows = 1
cols = 1
width = 10
height = 10
shuffle = False
pattern = "patrickstar"
extra_args = ""
process = None
board = None
leds = None


def run():
    global board, leds
    board = tile.TileArray(rows=rows, cols=cols, height=height, width=width)
    leds = tile.LEDStripTeensyUART(board)
    if shuffle:
        run_pattern.shuffle(board, leds)
    else:
        run_pattern.run_pattern(board, leds, pattern, extra_args.split())


def start_proc():
    global process
    if process is not None:
        process.terminate()
        process.join()
    process = multiprocessing.Process(target=run)
    process.start()


@app.route('/')
def hello_world():
    patterns = [name for _, name, _ in pkgutil.iter_modules(['patterns'])]
    return render_template("index.html", rows=rows, cols=cols, width=width, height=height, shuffle=shuffle,
                           pattern=pattern, patterns=patterns, extra=extra_args)


@app.route('/save-settings', methods=['POST'])
def handle_data():
    global rows, cols, width, height
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    width = int(request.form['width'])
    height = int(request.form['height'])
    return redirect("/")


@app.route('/save-pattern', methods=['POST'])
def save_pattern():
    global shuffle, pattern, extra_args
    shuffle = False
    pattern = request.form['pattern']
    extra_args = request.form['extra']
    start_proc()
    return redirect("/")


@app.route('/save-shuffle', methods=['POST'])
def save_shuffle():
    global shuffle, pattern, extra_args
    shuffle = True
    pattern = ""
    extra_args = ""
    start_proc()
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, host="0")
