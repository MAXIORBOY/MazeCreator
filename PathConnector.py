import numpy as np
import random as rnd
from Main import GridMaster, FieldCalculation


class PathConnector(GridMaster, FieldCalculation):
    def __init__(self, grid, probability_to_turn_obstacle_into_path=0.7):
        GridMaster.__init__(self)
        FieldCalculation.__init__(self)
        self.grid = grid
        self.probability_to_turn_obstacle_into_path = probability_to_turn_obstacle_into_path

        self.paths_fixer_templates, self.paths_fixer_not_none_templates_indexes = self.create_paths_fixer_templates()
        self.paths_fixer()

    def create_paths_fixer_templates(self):
        templates = [np.array([[None, self.path_value, None], [self.path_value, self.obstacle_value, None], [None, None, None]]),
                     np.array([[None, self.path_value, None], [None, self.obstacle_value, self.path_value], [None, None, None]]),
                     np.array([[None, None, None], [None, self.obstacle_value, self.path_value], [None, self.path_value, None]]),
                     np.array([[None, None, None], [self.path_value, self.obstacle_value, None], [None, self.path_value, None]]),
                     np.array([[None, None, None], [self.path_value, self.obstacle_value, self.path_value], [None, None, None]]),
                     np.array([[None, self.path_value, None], [None, self.obstacle_value, None], [None, self.path_value, None]])]

        not_none_templates_indexes = []
        for template in templates:
            not_none_templates_indexes.append([(i, j) for i in range(len(template)) for j in range(len(template[i])) if template[i, j] is not None])

        return templates, not_none_templates_indexes

    def compare_matrix_with_paths_fixer_template(self, matrix):
        template_index = 0
        for template_indexes in self.paths_fixer_not_none_templates_indexes:
            if all([matrix[indexes] == self.paths_fixer_templates[template_index][indexes] for indexes in template_indexes]):
                return True

            template_index += 1

        return False

    def paths_fixer(self):
        for i in range(1, len(self.grid) - 3):
            for j in range(1, len(self.grid[i]) - 3):
                if self.compare_matrix_with_paths_fixer_template(self.grid[i:i + 3, j:j + 3]):
                    self.set_field_coords((i + 1, j + 1))
                    if self.check_2x2_matrices(self.grid, self.path_value):
                        if rnd.random() <= self.probability_to_turn_obstacle_into_path:
                            self.grid[i + 1, j + 1] = self.path_value
