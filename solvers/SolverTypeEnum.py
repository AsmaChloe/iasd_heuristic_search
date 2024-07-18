
from enum import Enum
from solvers.DijkstraSolver import DijkstraSolver
from solvers.RandomSolver import RandomSolver


class SolverTypeEnum(Enum):
    RANDOM = RandomSolver
    DIJKSTRA = DijkstraSolver
