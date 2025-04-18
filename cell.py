class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.visited = False
