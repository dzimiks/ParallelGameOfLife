import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Process, Value

# todo da li mogu da procitam prvo stanje iz matrice? - moze
# todo svaka celija ima svoj queue za poruke
# todo susedima javljam svoje stanje(nije blokirajuce)
# todo celija je blokirana nad queue-om dok svaka celija ne javi stanje(8 puta radim wait nad queue)
# todo svaka celija ceka da joj svi susedi kazu svoja stanja
# todo prodjem kroz queue i update svoje stanje na osnovu njih
# todo da li je dozvoljeno upisati stanje u matricu kad zavrsim update?


N = 5
ON = 255
OFF = 0
vals = [ON, OFF]
# randomGrid
grid = np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)

plt.imshow(grid, interpolation='nearest')
plt.show()

cellsFinished = Value('i', 0)
numOfCellsFinished = multiprocessing.Condition()


class Celija(Process):
    def __init__(self, row, column, state, gridSize, serviceQueue, matrixQueueCell, numOfCellsFinished,cellsFinished,valueOn,valueOff):
        super().__init__()
        self.currentIteration = 0
        self.row = row
        self.column = column
        self.state = state
        self.gridSize = gridSize
        self.serviceQueue = serviceQueue
        self.matrixQueueCell = matrixQueueCell
        self.numOfCellsFinished = numOfCellsFinished
        self.cellsFinished = cellsFinished
        self.valueOn = valueOn
        self.valueOff = valueOff

    def signalNeighbors(self):

        self.matrixQueueCell[self.row][(self.column - 1) % self.gridSize].put(self.state)

        self.matrixQueueCell[self.row][(self.column + 1) % self.gridSize].put(self.state)

        self.matrixQueueCell[(self.row - 1) % self.gridSize][self.column].put(self.state)

        self.matrixQueueCell[(self.row + 1) % self.gridSize][self.column].put(self.state)

        self.matrixQueueCell[(self.row - 1) % self.gridSize][(self.column - 1) % self.gridSize].put(self.state)

        self.matrixQueueCell[(self.row - 1) % self.gridSize][(self.column + 1) % self.gridSize].put(self.state)

        self.matrixQueueCell[(self.row + 1) % self.gridSize][(self.column - 1) % self.gridSize].put(self.state)

        self.matrixQueueCell[(self.row + 1) % self.gridSize][(self.column + 1) % self.gridSize].put(self.state)

    def update(self, total):
        if self.state == self.valueOn:
            if (total < 2) or (total > 3):
                self.state = self.valueOff
        else:
            if total == 3:
                self.state = self.valueOn


        with self.cellsFinished.get_lock():
            # print("Cell finished ",cellsFinished.value)
            self.cellsFinished.value += 1

        self.currentIteration += 1
        cellInfo = (self.row, self.column, self.currentIteration, self.state)
        # print('cellsFinished:', cellsFinished.value)
        self.serviceQueue.put(cellInfo)
        # todo spakuj koordinate, broj iteracije i novo stanje u tuple i onda odradi put u queue

    def run(self):

        for i in range(0,5):

            self.signalNeighbors()
            total = 0

            for i in range(0, 8):
                total += self.matrixQueueCell[self.row][self.column].get()

            # print("Total",total // 255)
            self.update(total // 255)
            self.numOfCellsFinished.acquire()

            if self.cellsFinished.value == self.gridSize * self.gridSize:
                with self.cellsFinished.get_lock():
                    self.cellsFinished.value = 0
                # print("clear cells finished:", cellsFinished.value)
                    self.numOfCellsFinished.notify_all()

                self.numOfCellsFinished.release()
            else:
                print("Celija", self.row, self.column, "ceka")
                self.numOfCellsFinished.wait()
                self.numOfCellsFinished.release()


class ServiceProces(Process):
    def __init__(self, grid, gridSize, serviceQueue):
        super().__init__()
        self.grid = grid
        self.gridSize = gridSize
        self.serviceQueue = serviceQueue

    def run(self):
        listaMatrica = []

        for i in range(0,5):

            for i in range(0, self.gridSize * self.gridSize):
                cellsInfo = self.serviceQueue.get()
                # print(i, '- Cells info:', cellsInfo)
                self.grid[cellsInfo[0]][cellsInfo[1]] = cellsInfo[3]

            listaMatrica.append(self.grid.copy())

        for g in listaMatrica:
            plt.imshow(g, interpolation='nearest')
            plt.show()


serviceQueue = multiprocessing.Queue()



matrixQueueCell = [[multiprocessing.Queue() for i in range(N)] for j in range(N)]

listaCelija = []

serviceProcess = ServiceProces(grid, N, serviceQueue)
serviceProcess.start()

# Starting threads
# for i in range(0, N):
#     for j in range(0, N):
# print("Starting thread: " + i.__str__() + j.__str__())
# process = Celija(i, j, grid[i][j], N, serviceQueue, matrixQueueCell, numOfCellsFinished, lock)
process = [[Celija(i, j, grid[i][j], N, serviceQueue, matrixQueueCell, numOfCellsFinished, cellsFinished,ON,OFF) for i in range(N)] for j in
           range(N)]

for t in process:
    for op in t:
        op.start()

for t in process:
    for op in t:
        op.join()

serviceProcess.join()

# for g in listaMatrica:
#     plt.imshow(g, interpolation='nearest')
#     plt.show()

# todo queue-ve,lock,condition,broj itracija,velicina matrice,
# todo pracenje koliko je celija zavrsilo, za to koristiti value
# todo kontrol procesu se salje broj iteracija,matricu,velicini grida,service queue(celije komuniciraju sa service procesom),
# todo retrun queue(ne mora) ali da bi napravio animaciju mora da se pozove anime iz main-a
# todo mogu da mu prosledim matricu na pocetku i on ce nju da menja
