from solvers.Solver import POSSIBLE_MOVES, Solver
import random


class RandomSolver(Solver):

  def __init__(self, environment, robot_pos, dest_pos):
    Solver.__init__(self, environment, robot_pos, dest_pos)

  def solve(self):
    potential_poss = []

    for move in POSSIBLE_MOVES:
      potential_pos = (self.robot_pos[0] + move[0],
                       self.robot_pos[1] + move[1], move[2])

      if potential_pos[0] >= 0 and potential_pos[0] < self.environment.window.rows \
      and potential_pos[1] >= 0 and potential_pos[1] < self.environment.window.cols \
      and self.environment.grid_data[potential_pos[0]][potential_pos[1]] != 'obstacle':
        potential_poss.append(potential_pos)

    output = None
    if len(potential_poss) > 0:
      move_row, move_col, direction = random.choice(potential_poss)
      output = (move_row, move_col, direction)

    return output
