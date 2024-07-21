from abc import abstractmethod

from solvers.parents.Solver import Solver


class MAPFSolver(Solver):
    def __init__(self, environment, agents, constraints=None):
        Solver.__init__(self, environment, constraints)
        self.agents = agents

    @abstractmethod
    def solve(self):
        pass