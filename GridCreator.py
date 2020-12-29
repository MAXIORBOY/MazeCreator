import numpy as np
from Main import GridMaster


class GridCreator(GridMaster):
    def __init__(self, rows, columns):
        GridMaster.__init__(self)
        self.rows = rows
        self.columns = columns
        self.grid = self.create_grid()
        self.create_borders()

    def create_grid(self):
        grid = np.zeros((self.rows, self.columns), dtype=int)
        grid[:, :] = self.path_value

        return grid

    def create_borders(self):
        self.grid[0, :] = self.obstacle_value
        self.grid[-1, :] = self.obstacle_value
        self.grid[:, 0] = self.obstacle_value
        self.grid[:, -1] = self.obstacle_value
