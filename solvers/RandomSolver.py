import random

POSSIBLE_MOVES = [
    (-1, 0, 'UP'),
    (1, 0, 'DOWN'),
    (0, -1, 'LEFT'),
    (0, 1, 'RIGHT')
]

class RandomSolver:
  def __init__(self, grid, robot_row, robot_col, dest_pos = None):
    self.grid = grid
    self.robot_row = robot_row
    self.robot_col = robot_col

  def solve(self):
    potential_poss = []

    for move in POSSIBLE_MOVES :
        potential_pos = (self.robot_row+move[0], self.robot_col+move[1], move[2])
        
        if potential_pos[0] >= 0 and potential_pos[0]<self.grid.window.rows \
        and potential_pos[1] >= 0 and potential_pos[1]<self.grid.window.cols \
        and self.grid.grid_data[potential_pos[0]][potential_pos[1]] != 'obstacle':
            potential_poss.append(potential_pos)

    output = None
    if len(potential_poss)>0:
      move_row, move_col, direction = random.choice(potential_poss)
      output = (move_row, move_col, direction)

    return output