import random as rnd
from Main import GridMaster, FieldCalculation


class EntryExitGenerator(GridMaster, FieldCalculation):
    def __init__(self, grid, width_of_exclusion_strip=5):
        GridMaster.__init__(self)
        FieldCalculation.__init__(self)
        self.grid = grid
        self.width_of_exclusion_strip = width_of_exclusion_strip

        self.entry_coords, self.exit_coords = self.generate_entry_and_exit_coords()
        self.set_entry_and_exit_as_path()

    def generate_entry_and_exit_coords(self):
        available_fields = self.get_coords_of_non_corner_border_fields(self.grid)
        entry_coords = rnd.choice(available_fields)

        available_fields.remove(entry_coords)
        self.set_field_coords(entry_coords)
        excluded_fields = self.get_fields_coords_from_n_zones_around(n_zones=int(max(len(self.grid), len(self.grid[0])) / 2.5))
        available_fields = [available_field for available_field in available_fields if available_field not in excluded_fields and
                            available_field[0] not in [entry_coords[0] - i for i in range(-int(self.width_of_exclusion_strip / 2), int(self.width_of_exclusion_strip / 2) + 1)] and
                            available_field[1] not in [entry_coords[1] - i for i in range(-int(self.width_of_exclusion_strip / 2), int(self.width_of_exclusion_strip / 2) + 1)]]

        exit_coords = rnd.choice(available_fields)

        return entry_coords, exit_coords

    def set_entry_and_exit_as_path(self):
        self.grid[self.entry_coords] = self.path_value
        self.grid[self.exit_coords] = self.path_value

    def get_data(self):
        return self.grid, self.entry_coords, self.exit_coords
