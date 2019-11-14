import numpy as np
import matplotlib.pyplot as plt
import threading
import queue
from threading import Thread
import random
import time

# todo da li mogu da procitam prvo stanje iz matrice? - moze
# todo svaka celija ima svoj queue za poruke
# todo susedima javljam svoje stanje(nije blokirajuce)
# todo celija je blokirana nad queue-om dok svaka celija ne javi stanje(8 puta radim wait nad queue)
# todo svaka celija ceka da joj svi susedi kazu svoja stanja
# todo prodjem kroz queue i update svoje stanje na osnovu njih
# todo da li je dozvoljeno upisati stanje u matricu kad zavrsim update?


N = 20
ON = 255
OFF = 0
vals = [ON, OFF]
# randomGrid
grid = np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)
listaMatrica = []

plt.imshow(grid, interpolation='nearest')
plt.show()

cellsFinished = 0
numOfCellsFinished = threading.Condition()


class Celija(Thread):

    def __init__(self, row, column, state):
        super().__init__()
        self.currentIteration = 0
        self.row = row
        self.column = column
        self.state = state
        self.neighborsQueue = queue.Queue()

    def signalNeighbors(self):
        for t in threads:
            if t.row == self.row and t.column == (self.column - 1) % N:
                t.neighborsQueue.put(self.state)
            if t.row == self.row and t.column == (self.column + 1) % N:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row - 1) % N and t.column == self.column:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row + 1) % N and t.column == self.column:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row - 1) % N and t.column == (self.column - 1) % N:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row - 1) % N and t.column == (self.column + 1) % N:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row + 1) % N and t.column == (self.column - 1) % N:
                t.neighborsQueue.put(self.state)
            if t.row == (self.row + 1) % N and t.column == (self.column + 1) % N:
                t.neighborsQueue.put(self.state)

    def update(self, total):
        global cellsFinished
        global grid

        if self.state == ON:

            if (total < 2) or (total > 3):
                self.state = OFF
                grid[self.row, self.column] = OFF
        else:
            if total == 3:
                self.state = ON
                grid[self.row, self.column] = ON

        # zakljucavanje pre povecanja broja celija koje su zavrsile za iteracijom
        numOfCellsFinished.acquire()
        cellsFinished += 1
        numOfCellsFinished.release()

        self.currentIteration += 1

    def run(self):
        global cellsFinished
        # TODO read value from neighbors
        for o in range(0, 5):
            self.signalNeighbors()

            total = 0
            for i in range(0, 8):
                total += self.neighborsQueue.get()

            timeOfSleep = random.random()

            time.sleep(timeOfSleep)

            self.update(total / 255)

            numOfCellsFinished.acquire()
            if cellsFinished == N * N:
                # print("skrt")
                cellsFinished = 0
                numOfCellsFinished.notifyAll()
                numOfCellsFinished.release()
                listaMatrica.append(grid.copy())
            else:
                numOfCellsFinished.wait()
                numOfCellsFinished.release()


threads = []
# Starting threads
for i in range(0, N):
    for j in range(0, N):
        # print("Starting thread: " + i.__str__() + j.__str__())
        thread = Celija(i, j, grid[i][j])
        threads.append(thread)

for t in threads:
    t.start()

for t in threads:
    t.join()

for g in listaMatrica:
    plt.imshow(g, interpolation='nearest')
    plt.show()
