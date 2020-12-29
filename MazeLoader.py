from LoadData import LoadData
from GridDisplay import GridDisplay


class MazeLoader:
    def __init__(self, filename, display_maze=True):
        self.filename = filename
        self.display_maze = display_maze

        self.grid = None
        self.entry_coords = None
        self.exit_coords = None
        self.solution_path = None
        self.path_value = None
        self.obstacle_value = None

    def set_filename(self, new_filename):
        self.filename = new_filename

    def show_maze(self):
        GridDisplay(self.grid).show_grid()

    def load_grid_from_csv(self):
        self.grid = LoadData(self.filename).load_grid_from_csv()
        if self.display_maze:
            self.show_maze()

    def load_data_from_pickle_file(self):
        self.grid, self.entry_coords, self.exit_coords, self.solution_path, self.path_value, self.obstacle_value = LoadData(self.filename).load_data_from_pickle_file()
        if self.display_maze:
            self.show_maze()
