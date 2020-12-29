from GridCreator import GridCreator
from EntryExitGenerator import EntryExitGenerator
from SolutionPathCreator import SolutionPathGenerator
from InternalWallsCreator import InternalWallsCreator
from PathConnector import PathConnector
from SolutionPathOptimalMaker import SolutionPathOptimalMaker
from IsolatedPathsRemover import IsolatedPathsRemover
from GridDisplay import GridDisplay
from SaveData import SaveData


class MazeCreator:
    def __init__(self, rows, columns, display_maze=True, save_data=True):
        self.rows = rows
        self.columns = columns
        self.display_maze = display_maze
        self.save_data = save_data

    def generate_maze(self):
        grid = GridCreator(self.rows, self.columns).grid
        grid, entry_coords, exit_coords = EntryExitGenerator(grid).get_data()
        solution_path = SolutionPathGenerator(grid, entry_coords, exit_coords).solution_path
        grid = InternalWallsCreator(grid, solution_path).grid
        grid = PathConnector(grid).grid
        grid = SolutionPathOptimalMaker(grid, entry_coords, exit_coords, solution_path).grid
        grid = IsolatedPathsRemover(grid, entry_coords, exit_coords).grid

        if self.display_maze:
            GridDisplay(grid).show_grid()

        if self.save_data:
            save_data_obj = SaveData(grid, entry_coords, exit_coords, solution_path)
            save_data_obj.save_grid_to_csv()
            save_data_obj.save_data_to_pickle_file()
