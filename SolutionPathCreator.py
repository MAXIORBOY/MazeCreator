import random as rnd
import numpy as np
from Main import GridMaster, FieldCalculation
from AStar import AStar


class Move:
    def __init__(self):
        self.up_move_name = 'up'
        self.down_move_name = 'down'
        self.right_move_name = 'right'
        self.left_move_name = 'left'

        self.moves = [self.up_move_name, self.down_move_name, self.right_move_name, self.left_move_name]
        self.move_definitions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.move_definitions_dictionary = dict(zip(self.moves, self.move_definitions))

    def get_opposite_move(self, move):
        if move == self.up_move_name:
            return self.down_move_name
        elif move == self.down_move_name:
            return self.up_move_name
        elif move == self.right_move_name:
            return self.left_move_name
        elif move == self.left_move_name:
            return self.right_move_name

    def get_vertical_direction_based_on_distance_value(self, vertical_distance_value):
        if vertical_distance_value > 0:
            return self.up_move_name

        elif vertical_distance_value < 0:
            return self.down_move_name

        else:
            return None

    def get_horizontal_direction_based_on_distance_value(self, horizontal_distance_value):
        if horizontal_distance_value > 0:
            return self.right_move_name

        elif horizontal_distance_value < 0:
            return self.left_move_name

        else:
            return None

    def get_next_stairs_move_based_on_two_moves(self, first_move, second_move):
        if (first_move == self.right_move_name or first_move == self.left_move_name) and (second_move == self.up_move_name or second_move == self.down_move_name):
            return first_move

        if (first_move == self.up_move_name or first_move == self.down_move_name) and (second_move == self.right_move_name or second_move == self.left_move_name):
            return first_move

        return None


class PreferableFieldsGenerator:
    def __init__(self, grid, chance_for_preferable_field=0.4):
        self.grid = grid
        self.chance_for_preferable_field = chance_for_preferable_field

        self.preferable_fields = self.create_preferable_fields()

    def create_preferable_fields(self):
        preferable_fields = []
        for coords in [(i, j) for i in range(1, len(self.grid) - 1) for j in range(1 + len(self.grid[i]) - 1)]:
            if rnd.random() <= self.chance_for_preferable_field:
                preferable_fields.append(coords)

        return preferable_fields


class SolutionPathGenerator(GridMaster, FieldCalculation, Move, PreferableFieldsGenerator):
    def __init__(self, grid, entry_coords, exit_coords, instruction_move_bias=3, preferable_move_bias=6, anti_stairs_bias=4):
        GridMaster.__init__(self)
        FieldCalculation.__init__(self)
        Move.__init__(self)
        self.grid = grid
        PreferableFieldsGenerator.__init__(self, grid)
        self.entry_coords = entry_coords
        self.exit_coords = exit_coords
        self.instruction_move_bias = instruction_move_bias
        self.preferable_move_bias = preferable_move_bias
        self.anti_stairs_bias = anti_stairs_bias

        self.path_matrix = self.create_path_matrix()
        self.solution_path = self.create_solution_path()

    def create_path_matrix(self):
        path_matrix = np.copy(self.grid)
        for field_coords in self.get_internal_fields_coords(self.grid):
            path_matrix[field_coords] = self.path_value

        return path_matrix

    def create_instructions_how_to_get_from_a_to_b(self, first_field_coords, second_fields_coords):
        directions = {}
        self.set_both_field_coords(first_field_coords, second_fields_coords)

        vertical_distance = self.calculate_vertical_distance_between_fields()
        vertical_direction = self.get_vertical_direction_based_on_distance_value(vertical_distance)
        if vertical_direction is not None:
            directions[vertical_direction] = abs(vertical_distance)

        horizontal_distance = self.calculate_horizontal_distance_between_fields()
        horizontal_direction = self.get_horizontal_direction_based_on_distance_value(horizontal_distance)
        if horizontal_direction is not None:
            directions[horizontal_direction] = abs(horizontal_distance)

        return directions

    def prepare_weighted_list_of_moves_options_for_generator(self, available_moves, instruction_moves, stairs_move=None):
        weighted_move_options = []
        for available_move_direction in list(available_moves.keys()):
            if self.exit_coords == available_moves[available_move_direction]:
                return [available_move_direction]

            weighted_move_options.append(available_move_direction)

            if available_moves[available_move_direction] in self.preferable_fields:
                weighted_move_options.extend([available_move_direction] * self.preferable_move_bias)
            elif available_move_direction in instruction_moves:
                weighted_move_options.extend([available_move_direction] * self.instruction_move_bias)
            if stairs_move is not None and available_move_direction != stairs_move:
                weighted_move_options.extend([available_move_direction] * self.anti_stairs_bias)

        return weighted_move_options

    def update_instructions(self, instructions, new_move_direction):
        if instructions.get(new_move_direction, None) is not None:
            instructions[new_move_direction] -= 1
            if instructions[new_move_direction] == 0:
                del instructions[new_move_direction]
        else:
            if instructions.get(self.get_opposite_move(new_move_direction), None) is not None:
                instructions[self.get_opposite_move(new_move_direction)] += 1
            else:
                instructions[self.get_opposite_move(new_move_direction)] = 1

        return instructions

    def construct_modified_path_matrix_for_pathfinding_algorithm(self):
        modified_path_matrix = np.copy(self.path_matrix)
        non_border_solution_path_fields_coords = [coords for coords in self.get_internal_fields_coords(self.path_matrix) if self.path_matrix[coords] == self.obstacle_value]
        for non_border_solution_path_field_coord in non_border_solution_path_fields_coords:
            self.set_field_coords(non_border_solution_path_field_coord)
            for adjacent_field_coord in self.get_non_corner_adjacent_fields_coords():
                if adjacent_field_coord != self.exit_coords:
                    modified_path_matrix[adjacent_field_coord] = self.obstacle_value

        return modified_path_matrix

    def create_solution_path(self):
        solution_path_dictionary = {self.entry_coords: None}
        current_location = self.entry_coords
        previous_move = None
        prior_move = None

        instructions = self.create_instructions_how_to_get_from_a_to_b(self.entry_coords, self.exit_coords)
        while current_location != self.exit_coords:
            available_moves = {}
            for move_direction in list(self.move_definitions_dictionary.keys()):
                coords_of_move = tuple([current_location[k] + self.move_definitions_dictionary[move_direction][k] for k in range(len(current_location))])
                self.set_field_coords(coords_of_move)
                if self.check_if_coords_are_inside_the_grid(self.grid):
                    if self.grid[coords_of_move] != self.obstacle_value:
                        if coords_of_move not in list(solution_path_dictionary.keys()):
                            if self.check_if_next_move_does_not_intersect_with_current_path(self.path_matrix, self.obstacle_value):
                                if AStar(self.construct_modified_path_matrix_for_pathfinding_algorithm(), coords_of_move, self.exit_coords, use_euclidean_distance=False).get_shortest_path() is not None:
                                    available_moves[move_direction] = coords_of_move

            list_of_choices = self.prepare_weighted_list_of_moves_options_for_generator(available_moves, list(instructions.keys()), stairs_move=self.get_next_stairs_move_based_on_two_moves(prior_move, previous_move))
            chosen_move = rnd.choice(list_of_choices)
            instructions = self.update_instructions(instructions, chosen_move)
            new_path_field_coords = available_moves[chosen_move]
            solution_path_dictionary[new_path_field_coords] = chosen_move
            self.path_matrix[new_path_field_coords] = self.obstacle_value
            current_location = new_path_field_coords

            prior_move = previous_move
            previous_move = chosen_move

        return list(solution_path_dictionary.keys())
