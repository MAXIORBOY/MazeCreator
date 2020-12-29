import random as rnd
from Main import GridMaster
from AStar import AStar


class SolutionPathOptimalMaker(GridMaster):
    def __init__(self, grid, entry_coords, exit_coords, solution_path):
        GridMaster.__init__(self)
        self.grid = grid
        self.entry_cords = entry_coords
        self.exit_coords = exit_coords
        self.solution_path = solution_path
        self.optimal_path = self.get_optimal_path()

        self.make_solution_path_optimal()

    def get_optimal_path(self):
        return AStar(self.grid, self.entry_cords, self.exit_coords, use_euclidean_distance=False).get_shortest_path()

    def make_solution_path_optimal(self):
        while self.solution_path != self.optimal_path:
            optimal_path_coords_which_are_not_in_solution_path = [coords for coords in self.optimal_path if coords not in self.solution_path]
            self.grid[rnd.choice(optimal_path_coords_which_are_not_in_solution_path)] = self.obstacle_value

            self.optimal_path = self.get_optimal_path()
