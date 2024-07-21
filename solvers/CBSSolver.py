from solvers.AStarSolver import AStarSolver
from solvers.parents.MAPFSolver import MAPFSolver
import heapq

class CBSSolver(MAPFSolver):
    def __init__(self, environment, agents):
        MAPFSolver.__init__(self, environment, agents)

        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def generate_paths(self):
        all_paths = []
        for agent_id, (start_pos, dest_pos, _) in enumerate(self.agents):
            solver = AStarSolver(self.environment, start_pos, dest_pos, constraints=self.constraints)
            path, _ = solver.solve()
            if path:
                all_paths.append(path)
            else:
                return None
        return all_paths

    def solve(self):
        agent_paths = None
        open_list = []
        closed_list = set()

        initial_cost = sum(len(self.generate_paths()[i]) for i in range(len(self.agents)))
        open_list.append((initial_cost, []))
        best_cost = float('inf')

        while open_list:
            current_cost, current_constraints = heapq.heappop(open_list)
            # Converting back to list to then merge
            current_constraints = list(current_constraints)
            if current_cost >= best_cost:
                continue

            self.constraints = current_constraints
            paths = self.generate_paths()
            if paths is None:
                continue

            # Check for conflicts
            conflicts = self.check_conflicts(paths)
            if not conflicts:
                print("No conflict detected")
                best_cost = current_cost
                agent_paths = paths
            else:
                print("Conflict detected")
                for conflict in conflicts:
                    # Converting to tuple to hash
                    new_constraints = tuple(current_constraints + [conflict])
                    new_cost = current_cost + 1
                    if (new_cost, new_constraints) not in closed_list:
                        heapq.heappush(open_list, (new_cost, new_constraints))
                        closed_list.add((new_cost, new_constraints))
        return agent_paths

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
                        if self.agents[agent_id][2] > self.agents[other_agent_id][2]:
                            conflicts.append((time_step, pos, agent_id))
                        else:
                            conflicts.append((time_step, pos, other_agent_id))
                    position_to_agent[pos] = agent_id
            time_step += 1
        return conflicts
