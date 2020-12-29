import pandas as pd
import numpy as np
import pickle


class LoadData:
    def __init__(self, filename):
        self.filename = filename

    def load_grid_from_csv(self):
        return np.array(pd.read_csv(self.filename, header=None))

    def load_data_from_pickle_file(self):
        with open(self.filename, 'rb') as file:
            return pickle.load(file)
