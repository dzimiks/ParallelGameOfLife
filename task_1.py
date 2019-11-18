import numpy as np
import matplotlib.pyplot as plt
import threading
from threading import Thread
import random
import time

N = 20
ON = 255
OFF = 0
vals = [ON,OFF]
#randomGrid
grid = np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)
listaMatrica = []

plt.imshow(grid, interpolation='nearest')
plt.show()

cellsFinished = 0
numOfCellsFinished = threading.Lock()
accessListiBrojaca = threading.Lock()
nextIteration = threading.Condition()

class Celija(Thread):

    def __init__(self, row, column, state):
        super().__init__()
        self.currentIteration = 0
        self.row = row
        self.column = column
        self.state = state
        self.listaBrojacaSuseda = [0, 0, 0, 0, 0, 0, 0, 0]
        self.semaphore = threading.Semaphore(0)

    def checkNeighbors(self):

        total = 0
        for i in range(0, 8):
            if (i == 0):
                # 1
                # levi sused
                # posecen od strane desnog
                total += grid[self.row, (self.column - 1) % N]

                # zakljucava pristup listi brojaca suseda kako bi promenio vrednost

                for t in threads:
                    if t.row == self.row and t.column == (self.column - 1) % N:
                        t.listaBrojacaSuseda[i] += 1
                        # TODO proveri koja je vrednost u listi nakon ovoga


                    # print("Uvecam brojac za levi sused")

                    t.semaphore.release()

            if (i == 1):
                # 2
                # desni sused
                # posecen od strane levog
                total += grid[self.row, (self.column + 1) % N]


                for t in threads:
                    if t.row == self.row and t.column == (self.column + 1) % N:
                        t.listaBrojacaSuseda[i] += 1

                    # print("Uvecam brojac za desni sused")

                    t.semaphore.release()

            if (i == 2):
                # 3
                # gornji sused
                # posecen od strane donjeg
                total += grid[(self.row - 1) % N, self.column]


                for t in threads:
                    if (t.row == (self.row - 1) % N and t.column == self.column):
                        t.listaBrojacaSuseda[i] += 1

                    # print("Uvecam brojac za gornji sused")

                    t.semaphore.release()


            if (i == 3):
                # 4
                # donji sused
                # posecen od strane gornjeg
                total += grid[(self.row + 1) % N, self.column]


                for t in threads:
                    if (t.row == (self.row + 1) % N and t.column == self.column):
                        t.listaBrojacaSuseda[i] += 1
                    # print("Uvecam brojac za donji sused")

                    t.semaphore.release()


            if (i == 4):
                # 5
                # gornji levi sused
                # posecen od stranje donjeg desnog
                total += grid[(self.row - 1) % N, (self.column - 1) % N]


                for t in threads:
                    if (t.row == (self.row - 1) % N and t.column == (self.column - 1) % N):
                        t.listaBrojacaSuseda[i] += 1

                    # print("Uvecam brojac za gornji levi sused")

                    t.semaphore.release()


            if (i == 5):
                # 6
                # gornji desni sused
                # posecen od strane donjeg levog
                total += grid[(self.row - 1) % N, (self.column + 1) % N]


                for t in threads:
                    if (t.row == (self.row - 1) % N and t.column == (self.column + 1) % N):
                        t.listaBrojacaSuseda[i] += 1
                    # print("Uvecam brojac za gornji desni sused")

                    t.semaphore.release()


            if (i == 6):
                # 7
                # donji levi sused
                # posecen od strane gornjeg desnog
                total += grid[(self.row + 1) % N, (self.column - 1) % N]


                for t in threads:
                    if (t.row == (self.row + 1) % N and t.column == (self.column - 1) % N):
                        t.listaBrojacaSuseda[i] += 1
                    # print("Uvecam brojac za donji levi sused")

                    t.semaphore.release()


            if (i == 7):
                # 8
                # donji desni sused
                # posecen od strane gornjeg levog
                total += grid[(self.row + 1) % N, (self.column + 1) % N]


                for t in threads:
                    if (t.row == (self.row + 1) % N and t.column == (self.column + 1) % N):
                        t.listaBrojacaSuseda[i] += 1
                    # print("Uvecam brojac za donji desni sused")

                    t.semaphore.release()

        return total / 255

    def update(self, total):
        global cellsFinished
        global grid

        if grid[self.row, self.column] == ON:

            if (total < 2) or (total > 3):
                grid[self.row, self.column] = OFF
        else:
            if total == 3:
                grid[self.row, self.column] = ON

        # zakljucavanje pre povecanja broja celija koje su zavrsile za iteracijom
        numOfCellsFinished.acquire()
        # print("Menjam vrednost jer sam zavrsio")
        # print("Broj celija koje su zavrsile1:" + str(cellsFinished))
        cellsFinished += 1
        numOfCellsFinished.release()

        self.currentIteration += 1

    def run(self):
        global cellsFinished
        # TODO read value from neighbors
        for o in range(0,5):
            total = self.checkNeighbors()

            # print("Total " + str(self.row) + " " + str(self.column) + " : " + str(total))
            # waiting for everyone to read(waiting for semaphore to have value 1)
            # print("Brojac za semafor: "+ str(self.brojacZaSemafor))
            # print("Vrednost brojaca: "+str(brojac))
            while True:
                self.semaphore.acquire()

                # print("Celija "+str(self.row)+str(self.column))
                accessListiBrojaca.acquire()
                if self.listaBrojacaSuseda[0] == 1 and self.listaBrojacaSuseda[1] == 1 and self.listaBrojacaSuseda[1] == 1 and self.listaBrojacaSuseda[3] == 1 and self.listaBrojacaSuseda[4] == 1  and self.listaBrojacaSuseda[5] == 1 and self.listaBrojacaSuseda[6] == 1 and self.listaBrojacaSuseda[7] == 1:
                    for i in range(0,8):
                        self.listaBrojacaSuseda[i] = 0
                    accessListiBrojaca.release()
                    break
                accessListiBrojaca.release()

            timeOfSleep = random.random()
            # print("Vreme spavanja :" + str(timeOfSleep))
            time.sleep(timeOfSleep)
            # TODO write value based on neighbors
            self.update(total)
            numOfCellsFinished.acquire()
            if(cellsFinished == N*N):
                # print("Celija " + str(self.row) + str(self.column)+" radi notifyAll")
                # print("RADIM NotifyAll")
                cellsFinished = 0
                numOfCellsFinished.release()
                nextIteration.acquire()
                nextIteration.notifyAll()
                nextIteration.release()
                print("Crtam grid",self.currentIteration,o)

                listaMatrica.append(grid.copy())

            else:
                numOfCellsFinished.release()
                nextIteration.acquire()
                nextIteration.wait()
                nextIteration.release()




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
