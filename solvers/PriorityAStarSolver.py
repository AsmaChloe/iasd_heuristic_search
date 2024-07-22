from solvers.parents.Solver import POSSIBLE_MOVES
import time
from solvers.parents.SAPFSolver import SAPFSolver
import heapq

class PriorityAStarSolver(SAPFSolver):
    def __init__(self, environment, agents, constraints=None):
        super().__init__(environment, None, None, constraints)
        self.agents = agents
        self.time_step_map = {}  # Shared time step map for conflicts

    def heuristic(self, pos, dest_pos):
        return abs(pos[0] - dest_pos[0]) + abs(pos[1] - dest_pos[1])

    def is_valid(self, pos, time_step, agent_priority):
        if not super().is_valid(pos):
            return False

        # Check constraints for priority and time step
        if self.constraints is not None:
            for (t, p, priority) in self.constraints:
                if t == time_step and p == pos and priority <= agent_priority:
                    return False

        # Check shared time step map for conflicts
        if (pos, time_step) in self.time_step_map and self.time_step_map[(pos, time_step)] >= agent_priority:
            print(f"Conflict at {pos} at time step {time_step}. ")
            return False

        return True

    def solve(self):
        optimal_paths = []

        # Sort agents by priority in descending order (highest priority first)
        self.agents.sort(key=lambda agent: agent.priority, reverse=True)

        for agent in self.agents:
            path, compute_time = self.find_path(agent)
            if path:
                optimal_paths.append(path)
                for t, pos in enumerate(path):
                    self.time_step_map[(pos, t)] = agent.priority
            else:
                print(f"Agent with priority {agent.priority} could not find a path.")
                optimal_paths.append([])  # Append an empty path if no path is found

        return optimal_paths

    def find_path(self, agent):
        queue = []
        heapq.heappush(queue, (self.heuristic(agent.pos, agent.dest), 0, agent.pos))
        start_time = time.time_ns()

        self.parent = {}
        self.g_cost = {agent.pos: 0}
        self.visited = [[False for _ in range(self.environment.window.cols)] for _ in range(self.environment.window.rows)]

        while queue:
            _, current_time_step, current_pos = heapq.heappop(queue)

            if current_pos == agent.dest:
                compute_time = time.time_ns() - start_time
                path = [agent.dest]
                while current_pos is not None:
                    path.append(current_pos)
                    current_pos = self.parent.get(current_pos)
                return list(reversed(path)), compute_time

            self.visited[current_pos[0]][current_pos[1]] = True

            for move in POSSIBLE_MOVES:
                potential_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                next_time_step = current_time_step + 1

                if self.is_valid(potential_pos, next_time_step, agent.priority):
                    if not self.visited[potential_pos[0]][potential_pos[1]] or (potential_pos, next_time_step) not in self.time_step_map:
                        tentative_g_cost = self.g_cost[current_pos] + 1
                        if potential_pos not in self.g_cost or tentative_g_cost < self.g_cost[potential_pos]:
                            self.g_cost[potential_pos] = tentative_g_cost
                            f_cost = tentative_g_cost + self.heuristic(potential_pos, agent.dest)
                            heapq.heappush(queue, (f_cost, next_time_step, potential_pos))
                            self.parent[potential_pos] = current_pos

        return None, None
