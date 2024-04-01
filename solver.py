from game import GameBoard
import numpy as np
import constants

class Node() :
    parent = None
    children = None
    state = None

    def __init__(self, parent, state) :
        self.parent = parent
        self.state = state


class Solver() :
    
    gameboard : GameBoard = None
    placed_flags : int = None

    def __init__(self, gameboard : GameBoard) :
        self.gameboard = gameboard
        self.gameboard.table = [
                                [-1, 2, 1, 1, 0, 0, 2, -1, 3, 1],
                                [1, 2, -1, 1, 0, 1, 3, -1, -1, 2],
                                [1, 2, 2, 1, 0, 1, -1, 5, -1, 3],
                                [1, -1, 1, 0, 1, 2, 3, -1, 3, -1],
                                [2, 2, 2, 0, 1, -1, 2, 2, 4, 3],
                                [1, -1, 1, 0, 1, 2, 2, 2, -1, -1],
                                [2, 2, 1, 0, 0, 1, -1, 3, 3, 2],
                                [-1, 2, 0, 0, 1, 2, 3, -1, 1, 0],
                                [-1, 2, 0, 1, 2, -1, 2, 1, 1, 0],
                                [1, 1, 0, 1, -1, 2, 1, 0, 0, 0]
                                ]
        self.placed_flags = 0
        self.gameboard.updateSecretBoard(self.gameboard.getStartCoordinates())

        while self.gameboard.bomb - self.placed_flags != 0 :
            res = self.directResolution(10)
            if not res : break

        print(f"{self.gameboard.secret_gb}")
    
    def directResolution(self, depth = 1) :
        if depth == 0 :
            return False
        for x in range(self.gameboard.dim) :
            for y in range(self.gameboard.dim) : 
                if self.gameboard.secret_gb[x][y] != constants.HIDDEN : # Faire toutes les cases découvertes du démineur 
                    hidden_adj = 0
                    flag_adj = 0
                    for cell in self.gameboard.getAdjacent((x,y)) :
                        if self.gameboard.secret_gb[cell[0]][cell[1]] == constants.HIDDEN :
                            hidden_adj += 1
                        if self.gameboard.secret_gb[cell[0]][cell[1]] == constants.FLAG :
                            flag_adj += 1
                    if hidden_adj + flag_adj == self.gameboard.secret_gb[x][y] : # Si il y a autant de cases adjacentes pas découvertes que de bombes autour de la case
                        for cell in self.gameboard.getAdjacent((x,y)) :
                            if self.gameboard.placeFlag((cell[0],cell[1])) :
                                self.placed_flags += 1
                    
                    if flag_adj == self.gameboard.secret_gb[x][y] : # Si tous les flags ont déjà étés posés autour de la case
                        for cell in self.gameboard.getAdjacent((x,y)) :
                            if self.gameboard.secret_gb[cell[0]][cell[1]] == constants.HIDDEN :
                                self.gameboard.updateSecretBoard(cell)  # On clique sur toutes les cases pas découvertes autour
        return self.directResolution(depth-1)
    
    def deepResolution(self, depth : int) :
        pass
    

if __name__ == "__main__" :
    gm = GameBoard(10)
    solver = Solver(gm)
    print(gm.bomb - solver.placed_flags)