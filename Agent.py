class Agent:
    def __init__(self, pos, dest, priority=None):
        self.pos = pos
        self.dest = dest
        self.priority = priority
        self.found_destination = False
        self.optimal_path = []
        self.algorithm_step = 0

    def __str__(self):
        return f"Agent at {self.pos} with destination {self.dest} and priority {self.priority}"