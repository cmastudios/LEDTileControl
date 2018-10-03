import multiprocessing
from flask import Flask, request, redirect
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
    if shuffle:
        pass
    else:
        board = tile.TileArray(rows=rows, cols=cols, height=height, width=width)
        leds = tile.LEDStrip(board)
        run_pattern.run_pattern(board, leds, pattern, extra_args.split())


def start_proc():
    global process
    if process is not None:
        process.terminate()
        process.join()
    process = multiprocessing.Process(target=run)
    process.start()


indextemplate = """
<h1>Current settings:</h1><br>
Rows: {r} Cols: {c}<br>
Width: {w} Height: {h}<br>
Shuffle? {s}<br>
Pattern: {p}<br>
Extra Args: {x}<br><br>
<h1>Change settings</h1>
<form action="/save-settings" method="post">
    <label for="rows">Rows</label>
    <input type="text" id="rows" name="rows" value="{r}"><br>
    <label for="cols">Cols</label>
    <input type="text" id="cols" name="cols" value="{c}"><br>
    <label for="width">Width</label>
    <input type="text" id="width" name="width" value="{w}"><br>
    <label for="height">Height</label>
    <input type="text" id="height" name="height" value="{h}"><br>
    <input type="submit">
</form>
<h1>Run a different pattern</h1>
<form action="/save-pattern" method="post">
    <label for="pattern">Pattern</label>
    <select name="pattern">
        {ps}
    </select>
    <label for="extra">Extra Args</label>
    <input type="text" id="extra" name="extra" value="{x}"><br>
    <input type="submit">
</form>
<h1>Shuffle play</h1>
<form action="/save-shuffle" method="post">
    <input type="submit">
</form>
"""
patternstemplate = """<option value="{p}" {s}>{p}</option>"""


@app.route('/')
def hello_world():
    patterns = "\n".join([patternstemplate.format(p=name, s="selected" if name == pattern else "") for _, name, _ in pkgutil.iter_modules(['patterns'])])
    return indextemplate.format(r=rows, c=cols, w=width, h=height, s=shuffle, p=pattern, ps=patterns, x=extra_args)


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
    app.run(port=80, host="0")
