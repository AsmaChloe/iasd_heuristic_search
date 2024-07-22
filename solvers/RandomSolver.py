from solvers.parents.SAPFSolver import SAPFSolver
from solvers.parents.Solver import POSSIBLE_MOVES, Solver
import random


class RandomSolver(SAPFSolver):

  def __init__(self, environment, robot_pos, dest_pos):
    SAPFSolver.__init__(self, environment, robot_pos, dest_pos)

  def solve(self):
    potential_poss = []

    for move in POSSIBLE_MOVES:
      potential_pos = (self.robot_pos[0] + move[0],
                       self.robot_pos[1] + move[1], move[2])

      if self.is_valid(potential_pos):
        potential_poss.append(potential_pos)

    output = None
    if len(potential_poss) > 0:
      move_row, move_col, direction = random.choice(potential_poss)
      output = (move_row, move_col, direction)

    return output
