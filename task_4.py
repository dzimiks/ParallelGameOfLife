# TODO: Task 4
# TODO: =============================================
# TODO: recimo imam 5x5 matricu i pravim 5 procesa za svaki red u matrici
# TODO: glavni program spawnuje procese koji rade analizu rada
# TODO: glavni program ima celu matricu i dace procesu sve potrebne vrednosti svih suseda
# TODO: funkcija je zapravo podproces koja ce da vrati nazad glavnom programu
# TODO: Process Pool -> map() i apply()
# TODO: damo matricu i on nam vrati nazad
# TODO: funkc koju prosledim poolu da vrati i, j i novu vrednost
# TODO: =============================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Pool, Process
from time import sleep
import json

row_counter = 0
N = 3
ALIVE = 255
DEAD = 0
values = [ALIVE, DEAD]
grid = np.random.choice(values, N ** 2).reshape(N, N)


class Cell(Process):
    def __init__(self, x, y, state):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state

    def fun(self, grid):
        print(f'x: {self.x}, y: {self.y}, state: {self.state}')
        print(grid)


def game(grid_row):
    # global row_counter
    column = 0
    sleep(0.5)

    print(grid_row)
    print()

    # for cell in grid:
    print('N:', N)
    print('row_counter:', row_counter)
    print('column:', column)
    print()

    for _ in grid_row:
        result = {
            'upper_left': grid[(row_counter - 1) % N, (column - 1) % N],
            'upper': grid[(row_counter - 1) % N, column],
            'upper_right': grid[(row_counter - 1) % N, (column + 1) % N],
            'left': grid[row_counter, (column - 1) % N],
            'center': grid[row_counter, column],
            'right': grid[row_counter, (column + 1) % N],
            'lower_left': grid[(row_counter + 1) % N, (column - 1) % N],
            'lower': grid[(row_counter + 1) % N, column],
            'lower_right': grid[(row_counter + 1) % N, (column + 1) % N]
        }

        column += 1
        print(json.dumps(result, default=str, indent=4))


def program():
    global row_counter

    print(grid)

    pool = Pool(N)
    print('Pool kreiran')

    for i in range(N):
        pool.map(game, grid[i:i + 1, :])
        print('map() pozvan')
        row_counter += 1

    pool.close()


if __name__ == '__main__':
    program()
