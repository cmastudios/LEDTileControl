import numpy as np

last_img = None
delay = 0

def display(board, leds, filename=None, passed_delay=0.001):
    global last_img, delay
    if delay == 0:
        delay = float(passed_delay)

    if last_img is None:
        last_img = np.zeros((board.shape[0], board.shape[1]), dtype=np.uint8)
        if filename is None:
            if board.shape[0]>10 and board.shape[1] > 37:
                # Initialize Gosper Glider Gun if we have space
                delay = 0.001
                mat = load_file('life/glider.txt')
            elif board.shape[0] > 16 and board.shape[1] > 16:
                #Initialize Pulsar
                delay = 0.5
                mat = load_file('life/pulsar.txt')
            elif board.shape[0] > 4 and board.shape[1] > 4:
                delay = 1
                mat = load_file('life/basic.txt')
            else:
                raise RuntimeError('Board too small for defaults')
        else:
            mat = load_file(filename)

        if mat.shape[0] > board.shape[0] or mat.shape[1] > board.shape[1]:
            raise RuntimeError('Board too small for specified file')

        last_img[0:mat.shape[0], 0:mat.shape[1]] = mat

    next_img = np.zeros(last_img.shape, dtype=np.uint8)
    for i in range(last_img.shape[0]):
        for j in range(last_img.shape[1]):
            if last_img[i][j] == 0:
                if compute_surroundings(i, j, last_img)==3:
                    # Spawn if exactly 3 live neighbors.
                    next_img[i][j] = 1
            else:
                # Remain alive if 2 or three live neighbors
                neighbors = compute_surroundings(i, j, last_img)
                if neighbors == 2 or neighbors == 3:
                    next_img[i][j] = 1
    last_img = next_img
    leds.draw(convert_array_to_img(next_img), delay=delay)
    
    
def compute_surroundings(row, col, array):
    """
    Computes the number of live cells in the up to 8 cells surrounding
    the cell called out by row and col
    :param row: row of array
    :param col: col of array
    :param array: 2d numpy array representing current board
    """
    total = 0
    to_check = [
        [row-1, col-1],
        [row-1, col],
        [row-1, col+1],
        [row, col+1],
        [row+1, col+1],
        [row+1, col],
        [row+1, col-1],
        [row, col-1]
    ]
    for point in to_check:
        if 0 <= point[0] < array.shape[0] and 0 <= point[1] < array.shape[1]:
            total += array[point[0]][point[1]]
    return total


def convert_array_to_img(array):
    """
    Turns an array of cell states into an image (3d np array)
    :return: The new array
    """
    return 255 * np.stack((array,)*3, axis=-1)

def load_file(filename):
    if filename.endswith('.cells'):
        with open(filename, 'r') as f:
            array = []
            for line in f:
                row = []
                if line.startswith('!'):
                    continue
                for c in line:
                    if c == '.':
                        row.append(0)
                    elif c == 'O':
                        row.append(1)
                array.append(row)
        return np.array(array, dtype=np.uint8)
    else:
        return np.loadtxt(filename, dtype=np.uint8)
