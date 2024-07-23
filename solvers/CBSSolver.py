import heapq
import time

from solvers.parents.SAPFSolver import SAPFSolver
from solvers.parents.Solver import POSSIBLE_MOVES


class AStarSolver(SAPFSolver):
    def __init__(self, environment, robot_pos, dest_pos, constraints=None):
        SAPFSolver.__init__(self, environment, robot_pos, dest_pos, constraints=None)
        self.constraints = constraints or set()  # Set of constraints (time, pos, agent_id)
        self.parent = {}
        self.g_cost = {self.robot_pos: 0}
        self.visited = [[False for _ in range(self.environment.window.cols)]
                        for _ in range(self.environment.window.rows)]

    def heuristic(self, pos):
        return abs(pos[0] - self.dest_pos[0]) + abs(pos[1] - self.dest_pos[1])

    def solve(self):
        queue = []
        heapq.heappush(queue, (self.heuristic(self.robot_pos), self.robot_pos, 0))
        start_time = time.time_ns()

        while queue:
            _, current_pos, current_time = heapq.heappop(queue)

            # End - Retracing path
            if current_pos == self.dest_pos:
                self.compute_time = time.time_ns() - start_time
                path = [self.dest_pos]
                while current_pos is not None:
                    path.append(current_pos)
                    current_pos = self.parent.get(current_pos)
                return list(reversed(path)), self.compute_time

            self.visited[current_pos[0]][current_pos[1]] = True

            for move in POSSIBLE_MOVES:
                potential_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                next_time = current_time + 1

                if self.is_valid(potential_pos, next_time) and not self.visited[potential_pos[0]][potential_pos[1]]:
                    tentative_g_cost = self.g_cost[current_pos] + 1
                    if potential_pos not in self.g_cost or tentative_g_cost < self.g_cost[potential_pos]:
                        self.g_cost[potential_pos] = tentative_g_cost
                        f_cost = tentative_g_cost + self.heuristic(potential_pos)
                        heapq.heappush(queue, (f_cost, potential_pos, next_time))
                        self.parent[potential_pos] = current_pos

        return None, None

class CBSSolver:

    def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents
        self.agent_paths = []
        self.constraints = []
        self.open_list = []
        self.closed_list = set()
        self.best_cost = float('inf')

    def add_constraint(self, constraint):
        self.constraints.append(constraint)
        self.constraints.append(constraint)

    def generate_paths(self):
        all_paths = []
        for agent_id, agent in enumerate(self.agents) :
            start_pos = agent.pos
            dest_pos = agent.dest

            solver = AStarSolver(self.environment, start_pos, dest_pos, constraints=self.constraints)
            path, _ = solver.solve()
            if path is None :
                all_paths.append([])
                agent.found_destination = True
                print(f"No path found for agent {agent_id}")
            else :
                all_paths.append(path)

        return all_paths

    def solve(self):
        start_time = time.time_ns()
        initial_cost = sum(len(self.generate_paths()[i]) for i in range(len(self.agents)))
        self.open_list.append((initial_cost, []))
        self.best_cost = float('inf')

        while self.open_list:
            current_cost, current_constraints = heapq.heappop(self.open_list)
            if current_cost >= self.best_cost:
                continue

            self.constraints = current_constraints
            paths = self.generate_paths()
            if paths is None:
                continue

            # Check for conflicts
            conflicts = self.check_conflicts(paths)
            if not conflicts:
                print(f"No conflicts")
                self.best_cost = current_cost
                self.agent_paths = paths
            else:
                print(f"Solving conflicts...")
                for conflict in conflicts:
                    new_constraints = current_constraints + [conflict]
                    new_constraints_str = str(new_constraints)
                    new_cost = current_cost + 1
                    if (new_cost, new_constraints_str) not in self.closed_list:
                        heapq.heappush(self.open_list, (new_cost, new_constraints))
                        self.closed_list.add((new_cost, new_constraints_str))

        self.compute_time = time.time_ns() - start_time
        return self.agent_paths, self.compute_time

    def check_conflicts(self, paths):
        conflicts = []
        time_step = 0
        max_length = max(len(path) for path in paths)
        while time_step < max_length:
            position_to_agent = {}
            for agent_id, path in enumerate(paths):
                if time_step < len(path):
                    pos = path[time_step]
                    if pos in position_to_agent:
                        # Conflict detected
                        other_agent_id = position_to_agent[pos]
                        if self.agents[agent_id].priority > self.agents[other_agent_id].priority:
                            conflicts.append((time_step, pos, agent_id))
                        else:
                            conflicts.append((time_step, pos, other_agent_id))
                    position_to_agent[pos] = agent_id
            time_step += 1
        return conflicts