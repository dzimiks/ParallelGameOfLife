import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Setting up the values for the grid
ALIVE = 255
DEAD = 0
values = [ALIVE, DEAD]


def random_grid(n):
    """
    Returns a grid of NxN random values.

    :param n: Size of the grid.
    :return: A grid of NxN random values
    """
    return np.random.choice(values, n * n).reshape(n, n)


def update(frame_number, img, grid, n):
    """
    Updates given grid.

    :param frame_number: Current frame.
    :param img: Current image.
    :param grid: Current matrix.
    :param n: Size of the grid.
    :return: Display an image, i.e. data on a 2D regular raster.
    """

    # Copy grid
    new_grid = grid.copy()

    for i in range(n):
        for j in range(n):
            # Compute 8-neighbour sum using toroidal boundary conditions
            total = int((grid[i, (j - 1) % n] + grid[i, (j + 1) % n] +
                         grid[(i - 1) % n, j] + grid[(i + 1) % n, j] +
                         grid[(i - 1) % n, (j - 1) % n] + grid[(i - 1) % n, (j + 1) % n] +
                         grid[(i + 1) % n, (j - 1) % n] + grid[(i + 1) % n, (j + 1) % n]) / 255)

            # Conway's rules
            if grid[i, j] == ALIVE:
                if (total < 2) or total > 3:
                    new_grid[i, j] = DEAD
            else:
                if total == 3:
                    new_grid[i, j] = ALIVE

    # Update grid
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img


def play_game():
    # Grid size
    N = 50
    FRAMES = 10
    UPDATE_INTERVAL = 50
    SAVE_COUNT = 50

    grid = random_grid(N)

    for i in range(N):
        for j in range(N):
            # 3x3 Matrix of 8 neighbours of the current cell
            matrix = [[
                ((i - 1) % N, (j - 1) % N),
                ((i - 1) % N, j),
                ((i - 1) % N, (j + 1) % N)
            ], [
                (i, (j - 1) % N),
                (i, j),
                (i, (j + 1) % N)
            ], [
                ((i + 1) % N, (j - 1) % N),
                ((i + 1) % N, j),
                ((i + 1) % N, (j + 1) % N)
            ]]

            print('\nMatrix for ({},{}):'.format(i, j))

            for k in range(3):
                for v in range(3):
                    print(matrix[k][v], end='')
                print()

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(
        fig,
        update,
        fargs=(img, grid, N,),
        frames=FRAMES,
        interval=UPDATE_INTERVAL,
        save_count=SAVE_COUNT
    )
    plt.show()


if __name__ == '__main__':
    play_game()
