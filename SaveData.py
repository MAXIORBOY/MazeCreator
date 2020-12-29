import pandas as pd
import pickle
from Main import GridMaster


class SaveData(GridMaster):
    def __init__(self, grid, entry_coords, exit_coords, solution_path):
        GridMaster.__init__(self)
        self.grid = grid
        self.entry_coords = entry_coords
        self.exit_coords = exit_coords
        self.solution_path = solution_path

    def save_grid_to_csv(self):
        pd.DataFrame(self.grid).to_csv('maze_grid.csv', index=False, header=False)

    def save_data_to_pickle_file(self):
        with open('maze_data.pickle', 'wb') as file:
            pickle.dump((self.grid, self.entry_coords, self.exit_coords, self.solution_path, self.path_value, self.obstacle_value), file)
