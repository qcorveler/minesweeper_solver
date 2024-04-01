import random as rd, numpy as np, copy as cp, queue as Q, constants

class GameBoard() :
    
    table : list[list[int]] = None
    dim : int = None
    bomb : int = None
    secret_gb : list[list[int]] = None

    def __init__(self, dim : int) :
        self.table = np.zeros((dim, dim), dtype=int)
        self.dim = dim
        self.bomb = int((20/100)*dim**2)
        self.secret_gb = constants.HIDDEN*np.ones((self.dim, self.dim), dtype=int)

        for i in range (self.bomb) :
            x = rd.randint(0, dim-1)
            y = rd.randint(0, dim-1)
            while self.table[x][y] == constants.BOMB :
                x = rd.randint(0, dim-1)
                y = rd.randint(0, dim-1)
            self.table[x][y] = constants.BOMB

        while not self.isSolvable() :
            self.table = np.zeros((dim, dim), dtype=int)
            for i in range (self.bomb) :
                x = rd.randint(0, dim-1)
                y = rd.randint(0, dim-1)
                while self.table[x][y] == constants.BOMB :
                    x = rd.randint(0, dim-1)
                    y = rd.randint(0, dim-1)
                self.table[x][y] = constants.BOMB
        
        for x in range (dim):
            for y in range(dim):
                if self.table[x][y] == 0 :
                    adj_bombs = 0
                    for cell in self.getAdjacent((x,y)) :
                        if self.table[cell[0]][cell[1]] == constants.BOMB :
                            adj_bombs += 1
                    self.table[x][y] = adj_bombs

    
    def isSolvable(self) -> bool :
        gb_copy = cp.deepcopy(self.table)
        x_start, y_start = 0,0
        found : bool = False
        
        for x in range(self.dim) :
            for y in range(self.dim) :
                if gb_copy[x][y] == 0:
                    x_start, y_start = x, y
                    gb_copy[x][y] = 1
                    found = True
                    break
            if found : break

        fifo = Q.Queue()
        for cell in self.getAdjacent((x_start, y_start)) :
            x,y = cell[0], cell[1]
            if gb_copy[x][y] != constants.BOMB and gb_copy[x][y] != 1 and gb_copy[x][y] != -2 :
                fifo.put(cell)
                gb_copy[x][y] = 1
            elif gb_copy[x][y] == constants.BOMB :
                gb_copy[x][y] = -2

        while not fifo.empty() :
            cell = fifo.get()
            for cell2 in self.getAdjacent((cell[0], cell[1])) :
                x,y = cell2[0], cell2[1]
                if gb_copy[x][y] != constants.BOMB and gb_copy[x][y] != 1  and gb_copy[x][y] != -2 :
                    fifo.put(cell2)
                    gb_copy[x][y] = 1
                elif gb_copy[x][y] == constants.BOMB :
                    gb_copy[x][y] = -2

        for line in gb_copy :
            for i in line :
                if i == 0 or i == constants.BOMB :
                    return False
        return True

    def getAdjacent(self, coordinates) -> list :
        x, y = coordinates
        res = set()
        if x-1 >= 0 :
            res.add((x-1, y))
        if y-1 >= 0 :
            res.add((x, y-1))
        if x-1 >= 0 and y-1 >= 0 :
            res.add((x-1, y-1))
        if x+1 < self.dim :
            res.add((x+1, y))
        if y+1 < self.dim : 
            res.add((x, y+1))
        if x-1 >= 0 and y+1 < self.dim :
            res.add((x-1, y+1))
        if x+1 < self.dim and y-1 >= 0 :
            res.add((x+1, y-1))
        if x+1 < self.dim and y+1 < self.dim :
            res.add((x+1, y+1))

        return res
    
    def getStartCoordinates(self) :
        for x in range(self.dim) :
            for y in range(self.dim) :
                if self.table[x][y] == 0:
                    return (x,y)
    

    def clickOnCell(self, coordinates) :
        discoveredCell = set()
        cellToExplore = set()
        cellToExplore.add(coordinates)

        if self.table[coordinates[0]][coordinates[1]] == constants.BOMB :
            return False

        def explore(discoveredCell, cellToExplore) :
            cellToExplore_res = set()
            for cell in cellToExplore :
                if self.table[cell[0]][cell[1]] == 0 :
                    if not cell in discoveredCell :
                        for adj in self.getAdjacent(cell) :
                            cellToExplore_res.add(adj)
                discoveredCell.add(cell)
            
            return [discoveredCell, cellToExplore_res]


        while len(cellToExplore) > 0 :
            res = explore(discoveredCell, cellToExplore)
            discoveredCell = cp.deepcopy(res[0])
            cellToExplore = cp.deepcopy(res[1])

        return discoveredCell
    
    def updateSecretBoard(self, coordinates) :
        discovered = self.clickOnCell(coordinates)
        
        if not discovered : return False

        for x in range(self.dim) :
            for y in range(self.dim) :
                if (x, y) in discovered :
                    self.secret_gb[x][y] = self.table[x][y]
    
    def placeFlag(self, coordinates) : 
        x, y = coordinates
        if self.secret_gb[x][y] == constants.HIDDEN :
            self.secret_gb[x][y] = constants.FLAG
            return True
        return False


if __name__ == "__main__" :
    gm = GameBoard(10)
    print(f"{gm.table} \n Liste à découvrir pour le début : {gm.clickOnCell(gm.getStartCoordinates())} \n {len(gm.clickOnCell(gm.getStartCoordinates()))}")