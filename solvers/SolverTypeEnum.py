
from enum import Enum

from solvers.CBSSolver import CBSSolver
from solvers.AStarSolver import AStarSolver
from solvers.BFSSolver import BFSSolver
from solvers.DijkstraSolver import DijkstraSolver
from solvers.PriorityAStarSolver import PriorityAStarSolver
from solvers.RandomSolver import RandomSolver
from solvers.GreedyBFSSolver import GreedyBFSSolver

class SolverTypeEnum(Enum):

    def __new__(cls, *args, **kwargs):
          value = len(cls.__members__) + 1
          obj = object.__new__(cls)
          obj._value_ = value
          return obj

    def __init__(self, solver_class, agent_limit):
        self.solver_class = solver_class
        self.agent_limit = agent_limit

    RANDOM = RandomSolver, "single"
    DIJKSTRA = DijkstraSolver, "single"
    ASTAR = AStarSolver, "single"
    BFS = BFSSolver, "single"
    GREEDY_BFS = GreedyBFSSolver, "single"
    PRIORITY_BASED = PriorityAStarSolver, "multiple"
    CONFLICT_BASED = CBSSolver, "multiple"
