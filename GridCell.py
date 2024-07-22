class GridCell:
    def __init__(self):
        self.type = 'empty'
        self.original_type = 'empty'

        self.blocked_state = False #True if the cell is blocked : like an agent has found its destination