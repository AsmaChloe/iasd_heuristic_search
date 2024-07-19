from abc import abstractmethod

POSSIBLE_MOVES = [
    (-1, 0, 'UP'),
    (1, 0, 'DOWN'),
    (0, -1, 'LEFT'),
    (0, 1, 'RIGHT')
]

class Solver:
  def __init__(self, environment, robot_pos : tuple[int, int], dest_pos : tuple[int, int]) -> None:
    self.environment = environment
    self.dest_pos = dest_pos
    self.robot_pos = robot_pos
    self.compute_time = None

  @abstractmethod
  def solve(self):
    pass