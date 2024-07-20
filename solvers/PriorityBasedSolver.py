from solvers.AStarSolver import AStarSolver

class PriorityBasedSolver:

    def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents  # List of tuples (start_pos, dest_pos, priority)
        self.agent_paths = []
        self.max_steps = 0

    def compute_paths(self):
        # Calculate paths for all agents
        sorted(self.agents, key=lambda x: x[2])
        for start_pos, dest_pos, _ in self.agents:
            solver = AStarSolver(self.environment, start_pos, dest_pos)
            path, _ = solver.solve()
            if path is not None:
                self.agent_paths.append(path)
                self.max_steps = max(self.max_steps, len(path))
            else:
                print("A path could not be found for one of the agents.")

        # Sort agent paths based on priority (lower priority value is higher priority)
        # self.agent_paths = [path for _, _, _ in sorted(self.agents, key=lambda x: x[2])]
        self.agent_paths = self.agent_paths[:len(self.agents)]

    def solve(self):
        self.compute_paths()
        # print(f"before checking conflicts: {self.agent_paths=}")

        # Create a list to hold the final positions of agents
        final_positions = [[] for _ in range(len(self.agent_paths))]

        for step in range(self.max_steps):
            # print(f"Step {step}")
            previous_positions = [agent_path[min(step-1, len(agent_path) - 1)] if step >= 1  else None for agent_path in self.agent_paths]
            current_positions = [agent_path[min(step, len(agent_path) - 1)] for agent_path in self.agent_paths]
            # Check for conflicts
            position_to_agent = {}
            for agent_id, pos in enumerate(current_positions):
                if pos in position_to_agent:
                    # Conflict: Multiple agents want to move to the same position
                    priority = self.agents[agent_id][2]
                    conflict_agent_id = position_to_agent[pos]
                    conflict_priority = self.agents[conflict_agent_id][2]
                    # print(f"Conflict between agents {agent_id} and {conflict_agent_id} at position {pos} ")

                    if priority > conflict_priority:
                        # print(f"\tAgent {agent_id} has lower priority and will stay at previous position")
                        # The agent with lower priority will stay in its previous position
                        # print(f"\t\tAvant : {current_positions=}")
                        current_positions[agent_id] = previous_positions[agent_id]
                        # print(f"\t\tApres : {current_positions=}")
                position_to_agent[pos] = agent_id

            # Store the final positions for this step
            for agent_id, pos in enumerate(current_positions):
                final_positions[agent_id].append(pos)

        return final_positions
