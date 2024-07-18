import random

POSSIBLE_MOVES = [
    (-1, 0, 'UP'),
    (1, 0, 'DOWN'),
    (0, -1, 'LEFT'),
    (0, 1, 'RIGHT')
]

class Node:
    def __init__(self, g, robot_position, parent=None, move=None):
        self.g = g
        self.robot_position = robot_position
        self.parent = parent
        self.move = move
        self.children = []

    def __repr__(self) -> str:
        return f"Node(g={self.g}, robot_position={self.robot_position}, parent={self.parent}"

class DijkstraSolver:
    def __init__(self, environment, robot_row, robot_col):
        self.environment = environment
        self.start_node = Node(0, (robot_row, robot_col))
        self.destination = environment.destination_positions[environment.robot_positions.index((robot_row, robot_col))]
        self.leaves = []
        self.visited = set()

    def expand(self):
        queue = [self.start_node]
        self.visited.add(self.start_node.robot_position)

        while queue:
            current_node = queue.pop()

            if current_node.robot_position == self.destination:
                print(f"\tFound leaf.")
                self.leaves.append(current_node)
            else:
                print(f"\tExpanding node ...")
                for move_row, move_col, direction in POSSIBLE_MOVES:
                    new_row = current_node.robot_position[0] + move_row
                    new_col = current_node.robot_position[1] + move_col
                    new_position = (new_row, new_col)

                    if 0 <= new_row < self.environment.window.rows \
                            and 0 <= new_col < self.environment.window.cols \
                            and self.environment.grid_data[new_row][new_col] != 'obstacle' \
                            and new_position not in self.visited:
                        child_node = Node(current_node.g + 1,
                                          new_position,
                                          parent=current_node,
                                          move=(move_row, move_col, direction)
                                          )
                        # print(f"\tExpanding node {current_node} with move {child_node.move}")
                        current_node.children.append(child_node)
                        queue.append(child_node)
                        self.visited.add(new_position)
            print(f"\n")

    def solve(self):
        self.expand()
        print(f"{self.leaves}=")

        if not self.leaves:
            return None

        min_g = min(node.g for node in self.leaves)
        print(f"{min_g}")
        candidates_leaves = [node for node in self.leaves if node.g == min_g]
        print(f"{candidates_leaves=}")
        shallowest_leave = random.choice(candidates_leaves)
        path = self.retrace_path(shallowest_leave)
        return path

    def retrace_path(self, node):
        path = []
        while node.parent is not None:
            path.append(node.move)
            node = node.parent
        path.reverse()
        return path
