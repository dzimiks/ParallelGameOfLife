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
import json
from multiprocessing import Pool, cpu_count


ITERATIONS = 20
N = 20
ALIVE = 255
DEAD = 0
values = [ALIVE, DEAD]
grid = np.random.choice(values, N ** 2, p=(0.2, 0.8)).reshape(N, N)


def play_game(task, grid, N):
    coordinates = {}

    for x, y in task:
        result = {
            'upper_left': grid[(x - 1) % N, (y - 1) % N],
            'upper': grid[(x - 1) % N, y],
            'upper_right': grid[(x - 1) % N, (y + 1) % N],
            'left': grid[x, (y - 1) % N],
            # 'center': grid[x, y],
            'right': grid[x, (y + 1) % N],
            'lower_left': grid[(x + 1) % N, (y - 1) % N],
            'lower': grid[(x + 1) % N, y],
            'lower_right': grid[(x + 1) % N, (y + 1) % N]
        }

        # print(json.dumps(result, default=str, indent=4))

        total = 0

        for v in result.values():
            total += v

        total //= 255

        # Conway's rules
        if grid[x, y] == ALIVE:
            if total < 2 or total > 3:
                coordinates[(x, y)] = DEAD
            else:
                coordinates[(x, y)] = ALIVE
        else:
            if total == 3:
                coordinates[(x, y)] = ALIVE
            else:
                coordinates[(x, y)] = DEAD

    return coordinates


if __name__ == '__main__':
    matrix_list = [grid.copy()]
    tasks = []
    results = []

    print(grid)
    print()

    # Add grid rows
    for i in range(N):
        row = []
        for j in range(N):
            row.append((i, j))
        tasks.append(row)

    pool = Pool(cpu_count())

    for i in range(ITERATIONS):
        results = [pool.apply(play_game, args=(task, grid, N,)) for task in tasks]
        # results.append(result)
        # print('results:', results)

        for r in results:
            for k, v in r.items():
                grid[k[0], k[1]] = v

        matrix_list.append(grid.copy())

    pool.close()
    pool.join()

    for matrix in matrix_list:
        plt.imshow(matrix, interpolation='nearest')
        plt.show()
