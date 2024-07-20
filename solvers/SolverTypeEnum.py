
from enum import Enum

from solvers.CBSSolver import CBS
from solvers.AStarSolver import AStarSolver
from solvers.BFSSolver import BFSSolver
from solvers.DijkstraSolver import DijkstraSolver
from solvers.RandomSolver import RandomSolver
from solvers.GreedyBFSSolver import GreedyBFSSolver
from solvers.PriorityBasedSolver import PriorityBasedSolver

class SolverTypeEnum(Enum):
    RANDOM = RandomSolver
    DIJKSTRA = DijkstraSolver
    ASTAR = AStarSolver
    BFS = BFSSolver
    GreedyBFSSolver = GreedyBFSSolver
    PriorityBased = PriorityBasedSolver
    ConflictBaseSolver = CBS
