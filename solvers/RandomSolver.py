import random

class RandomSolver:
  def __init__(self, grid, robot_row, robot_col):
    self.grid = grid
    self.robot_row = robot_row
    self.robot_col = robot_col

  def solve(self):
    possible_moves = []
    if self.robot_row > 0 and self.grid.grid_data[self.robot_row - 1][self.robot_col] != 'obstacle':  # Up
        possible_moves.append((-1, 0, 'UP'))
    if self.robot_row < self.grid.rows - 1 and self.grid.grid_data[self.robot_row + 1][self.robot_col] != 'obstacle':  # Down
        possible_moves.append((1, 0, 'DOWN'))
    if self.robot_col > 0 and self.grid.grid_data[self.robot_row][self.robot_col - 1] != 'obstacle':  # Left
        possible_moves.append((0, -1, 'LEFT'))
    if self.robot_col < self.grid.cols - 1 and self.grid.grid_data[self.robot_row][self.robot_col + 1] != 'obstacle':  # Right
        possible_moves.append((0, 1, 'RIGHT'))

    output = None
    if possible_moves:
      move_row, move_col, direction = random.choice(possible_moves)
      output = (move_row, move_col, direction)

    return output