import random as rnd
from Main import GridMaster


class InternalWallsCreator(GridMaster):
    def __init__(self, grid, solution_path, max_number_of_walls_to_insert_in_2x2_matrix=2):
        GridMaster.__init__(self)
        self.grid = grid
        self.solution_path = solution_path
        self.max_number_of_walls_to_insert_in_2x2_matrix = max_number_of_walls_to_insert_in_2x2_matrix
        self.add_internal_walls()

    def add_internal_walls(self):
        for i in range(1, len(self.grid) - 2):
            for j in range(1, len(self.grid[i]) - 2):
                current_square_indexes = [(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)]
                if all([self.grid[index] == self.path_value for index in current_square_indexes]):
                    current_square_indexes_that_can_be_changed = [index for index in current_square_indexes if index not in self.solution_path]
                    for _ in range(self.max_number_of_walls_to_insert_in_2x2_matrix):
                        chosen_coords = rnd.choice(current_square_indexes_that_can_be_changed)
                        self.grid[chosen_coords] = self.obstacle_value
                        current_square_indexes_that_can_be_changed.remove(chosen_coords)
                        if not len(current_square_indexes_that_can_be_changed):
                            break
