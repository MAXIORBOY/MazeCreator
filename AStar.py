import random as rnd
from Main import GridMaster, FieldCalculation


class AStarFieldDetails:
    def __init__(self, distance_from_end_node, parent_field_coords=None):
        self.distance_from_starting_node = None
        self.sum_of_distances = None
        self.distance_from_end_node = distance_from_end_node
        self.parent_field_coords = parent_field_coords

    def set_distance_from_starting_node(self, distance_from_starting_node):
        self.distance_from_starting_node = distance_from_starting_node
        self.update_sum_of_distances()

    def update_sum_of_distances(self):
        if self.distance_from_starting_node is None or self.distance_from_end_node is None:
            self.sum_of_distances = None
        else:
            self.sum_of_distances = self.distance_from_starting_node + self.distance_from_end_node

    def set_new_parent_field_coords(self, new_parent_field_coords):
        self.parent_field_coords = new_parent_field_coords


class AStar(GridMaster, FieldCalculation):
    def __init__(self, grid, start_point_coords, end_point_coords, use_euclidean_distance=True):
        GridMaster.__init__(self)
        FieldCalculation.__init__(self)

        self.grid = grid
        self.start_point_coords = start_point_coords
        self.end_point_coords = end_point_coords
        self.use_euclidean_distance = use_euclidean_distance

        self.algorithm_dictionary = {}

    def get_all_neighbours_of_field_coords(self, field_coords):
        self.set_field_coords(field_coords)
        neighbours = self.get_non_corner_adjacent_fields_coords()
        if self.use_euclidean_distance:
            neighbours.extend(self.get_corner_adjacent_neighbours_of_field_coords())

        return neighbours

    def filter_neighbour_fields(self, neighbours):
        filtered_neighbours = []
        for neighbour_coords in neighbours:
            self.set_field_coords(neighbour_coords)
            if self.check_if_coords_are_inside_the_grid(self.grid):
                if self.grid[neighbour_coords] == self.path_value and neighbour_coords != self.start_point_coords:
                    filtered_neighbours.append(neighbour_coords)

        return filtered_neighbours

    def get_distance_and_path_from_field_to_start(self, field_coords, overridden_first_parent_field_coords=None):
        current_coords = field_coords
        distance = 0
        path = [current_coords]
        used_overridden_coords = False
        while current_coords != self.start_point_coords:
            if overridden_first_parent_field_coords is None or used_overridden_coords:
                current_parent_field_coords = self.algorithm_dictionary[current_coords].parent_field_coords
            else:
                current_parent_field_coords = overridden_first_parent_field_coords
                used_overridden_coords = True
            if sum([abs(current_coords[i] - current_parent_field_coords[i]) for i in range(len(field_coords))]) == 1:
                distance += 1
            else:
                distance += 2 ** (1 / 2)
            current_coords = current_parent_field_coords
            path.append(current_coords)

        return distance, path

    def get_shortest_path(self):
        if self.start_point_coords == self.end_point_coords:
            return [self.start_point_coords]

        explorable, explored = [], []

        self.set_both_field_coords(self.start_point_coords, self.end_point_coords)
        if self.use_euclidean_distance:
            self.algorithm_dictionary[self.start_point_coords] = AStarFieldDetails(self.calculate_euclidean_distance_between_two_coords())
        else:
            self.algorithm_dictionary[self.start_point_coords] = AStarFieldDetails(self.calculate_manhattan_distance_between_two_coords())

        explored.append(self.start_point_coords)
        chosen_coords = self.start_point_coords

        while True:
            current_coords = chosen_coords
            explored.append(current_coords)

            for neighbour_coords in self.filter_neighbour_fields(self.get_all_neighbours_of_field_coords(current_coords)):
                if neighbour_coords not in explorable and neighbour_coords not in explored:
                    self.set_both_field_coords(neighbour_coords, self.end_point_coords)
                    if self.use_euclidean_distance:
                        self.algorithm_dictionary[neighbour_coords] = AStarFieldDetails(distance_from_end_node=self.calculate_euclidean_distance_between_two_coords(),
                                                                                        parent_field_coords=current_coords)
                    else:
                        self.algorithm_dictionary[neighbour_coords] = AStarFieldDetails(distance_from_end_node=self.calculate_manhattan_distance_between_two_coords(),
                                                                                        parent_field_coords=current_coords)
                    path_distance, path = self.get_distance_and_path_from_field_to_start(neighbour_coords)
                    self.algorithm_dictionary[neighbour_coords].set_distance_from_starting_node(path_distance)
                    explorable.append(neighbour_coords)
                elif neighbour_coords in explorable:
                    alternative_path_distance, path = self.get_distance_and_path_from_field_to_start(neighbour_coords, overridden_first_parent_field_coords=current_coords)
                    if self.algorithm_dictionary[neighbour_coords].distance_from_starting_node > alternative_path_distance:
                        self.algorithm_dictionary[neighbour_coords].set_new_parent_field_coords(current_coords)
                        self.algorithm_dictionary[neighbour_coords].set_distance_from_starting_node(alternative_path_distance)

            if len(explorable):
                minimal_sum_of_distances = min([self.algorithm_dictionary[coords].sum_of_distances for coords in explorable])
                chosen_coords = rnd.choice([coords for coords in explorable if self.algorithm_dictionary[coords].sum_of_distances == minimal_sum_of_distances])
            else:
                return None

            explorable.remove(chosen_coords)
            if chosen_coords == self.end_point_coords:
                path_distance, path = self.get_distance_and_path_from_field_to_start(self.end_point_coords)
                return list(reversed(path))
