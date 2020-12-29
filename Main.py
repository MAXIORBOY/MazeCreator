class FieldCalculation:
    def __init__(self, field_coords=None, second_field_coords=None):
        self.field_coords = field_coords
        self.second_field_coords = second_field_coords

    def set_field_coords(self, new_field_coords):
        self.field_coords = new_field_coords

    def set_both_field_coords(self, first_new_field_coords, second_new_field_coords):
        self.field_coords = first_new_field_coords
        self.second_field_coords = second_new_field_coords

    def check_if_coords_are_inside_the_grid(self, grid):
        if 0 <= self.field_coords[0] < len(grid) and 0 <= self.field_coords[1] < len(grid[0]):
            return True
        else:
            return False

    def calculate_euclidean_distance_between_two_coords(self):
        return ((self.field_coords[0] - self.second_field_coords[0]) ** 2 + (self.field_coords[1] - self.second_field_coords[1]) ** 2) ** (1 / 2)

    def calculate_manhattan_distance_between_two_coords(self):
        return abs(self.field_coords[0] - self.second_field_coords[0]) + abs(self.field_coords[1] - self.second_field_coords[1])

    def get_non_corner_adjacent_fields_coords(self):
        return [(self.field_coords[0] - 1, self.field_coords[1]), (self.field_coords[0], self.field_coords[1] - 1),
                (self.field_coords[0] + 1, self.field_coords[1]), (self.field_coords[0], self.field_coords[1] + 1)]

    def get_corner_adjacent_neighbours_of_field_coords(self):
        return [(self.field_coords[0] - 1, self.field_coords[1] - 1), (self.field_coords[0] - 1, self.field_coords[1] + 1),
                (self.field_coords[0] + 1, self.field_coords[1] - 1), (self.field_coords[0] + 1, self.field_coords[1] + 1)]

    def get_fields_coords_from_n_zones_around(self, n_zones):
        return [(self.field_coords[0] + i, self.field_coords[1] + j) for j in range(-n_zones, n_zones + 1) for i in range(-n_zones, n_zones + 1) if any([i, j])]

    def get_all_2x2_coords_matrices_which_contain_field_coords(self):
        return [[(self.field_coords[0], self.field_coords[1] + 1), (self.field_coords[0] + 1, self.field_coords[1] + 1), (self.field_coords[0] + 1, self.field_coords[1])],
                [(self.field_coords[0] + 1, self.field_coords[1]), (self.field_coords[0] + 1, self.field_coords[1] - 1), (self.field_coords[0], self.field_coords[1] - 1)],
                [(self.field_coords[0], self.field_coords[1] - 1), (self.field_coords[0] - 1, self.field_coords[1] - 1), (self.field_coords[0] - 1, self.field_coords[1])],
                [(self.field_coords[0] - 1, self.field_coords[1]), (self.field_coords[0] - 1, self.field_coords[1] + 1), (self.field_coords[0], self.field_coords[1] + 1)]]

    def check_2x2_matrices(self, grid, object_value):
        for matrices_coords in self.get_all_2x2_coords_matrices_which_contain_field_coords():
            matrices_test = []
            for coords in matrices_coords:
                self.set_field_coords(coords)
                if self.check_if_coords_are_inside_the_grid(grid):
                    matrices_test.append(grid[coords] == object_value)
            if all(matrices_test) and len(matrices_test) == 3:
                return False

        return True

    def calculate_vertical_distance_between_fields(self):
        return self.field_coords[0] - self.second_field_coords[0]

    def calculate_horizontal_distance_between_fields(self):
        return self.second_field_coords[1] - self.field_coords[1]

    def check_if_next_move_does_not_intersect_with_current_path(self, grid, object_value):
        non_corner_border_fields = self.get_coords_of_non_corner_border_fields(grid)
        corner_border_fields = self.get_coords_of_corner_border_fields(grid)
        test_list = []
        for coords in self.get_non_corner_adjacent_fields_coords():
            self.set_field_coords(coords)
            if self.check_if_coords_are_inside_the_grid(grid) and coords not in non_corner_border_fields and coords not in corner_border_fields:
                test_list.append(int(grid[coords] == object_value))

        return not(sum(test_list) >= 2)

    @staticmethod
    def get_coords_of_non_corner_border_fields(grid):
        non_corner_border_fields = []

        non_corner_border_fields.extend([(0, j) for j in range(1, len(grid[0]) - 1)])
        non_corner_border_fields.extend([(i, len(grid[0]) - 1) for i in range(1, len(grid) - 1)])

        non_corner_border_fields.extend([(len(grid) - 1, j) for j in range(1, len(grid[0]) - 1)])
        non_corner_border_fields.extend([(i, 0) for i in range(1, len(grid) - 1)])

        return non_corner_border_fields

    @staticmethod
    def get_coords_of_corner_border_fields(grid):
        return [(0, 0), (0, len(grid[0]) - 1), (len(grid) - 1, 0), (len(grid) - 1, len(grid[0]) - 1)]

    @staticmethod
    def get_internal_fields_coords(grid):
        return [(i, j) for i in range(1, len(grid) - 1) for j in range(1, len(grid[i]) - 1)]


class GridMaster:
    def __init__(self):
        self.path_value = 0
        self.obstacle_value = 1
