from AStar import AStar
from Main import GridMaster


class IsolatedPathsRemover(GridMaster):
    def __init__(self, grid, entry_coords, exit_coords):
        GridMaster.__init__(self)
        self.grid = grid
        self.entry_coords = entry_coords
        self.exit_coords = exit_coords

        self.remove_isolated_paths()

    def remove_isolated_paths(self):
        for path_coords in [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i])) if self.grid[i, j] == self.path_value]:
            if path_coords not in [self.entry_coords, self.exit_coords]:
                if AStar(self.grid, path_coords, self.entry_coords, use_euclidean_distance=False).get_shortest_path() is None:
                    self.grid[path_coords] = self.obstacle_value
