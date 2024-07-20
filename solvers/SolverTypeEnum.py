
from enum import Enum
from solvers.AStarSolver import AStarSolver
from solvers.BFSSolver import BFSSolver
from solvers.DijkstraSolver import DijkstraSolver
from solvers.RandomSolver import RandomSolver
from solvers.GreedyBFSSolver import GreedyBFSSolver

class SolverTypeEnum(Enum):
    RANDOM = RandomSolver
    DIJKSTRA = DijkstraSolver
    ASTAR = AStarSolver
    BFS = BFSSolver
    GreedyBFSSolver = GreedyBFSSolver
