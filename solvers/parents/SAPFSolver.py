from abc import abstractmethod

from solvers.parents.Solver import Solver

class SAPFSolver(Solver):
    def __init__(self, environment, robot_pos : tuple[int, int], dest_pos : tuple[int, int], constraints=None) -> None:
        Solver.__init__(self, environment, constraints)
        self.dest_pos = dest_pos
        self.robot_pos = robot_pos


    @abstractmethod
    def solve(self):
        pass