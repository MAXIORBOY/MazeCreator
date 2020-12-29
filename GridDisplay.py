import matplotlib.pyplot as plt
from matplotlib import colors
from Main import GridMaster


class GridDisplay(GridMaster):
    def __init__(self, grid, path_rgb_color=(255, 239, 156), obstacle_rgb_color=(99, 190, 123)):
        GridMaster.__init__(self)
        self.grid = grid
        self.path_rgb_color = self.normalize_rgb_colors_values(path_rgb_color)
        self.obstacle_rgb_color = self.normalize_rgb_colors_values(obstacle_rgb_color)

    @staticmethod
    def normalize_rgb_colors_values(rgb_color):
        return tuple([color / 255 for color in rgb_color])

    def show_grid(self):
        def get_colormap():
            return colors.ListedColormap([self.path_rgb_color, self.obstacle_rgb_color])

        def get_norm(colormap):
            return colors.BoundaryNorm([self.path_value, (self.path_value + self.obstacle_value) / 2, self.obstacle_value], colormap.N)

        cmap = get_colormap()
        norm = get_norm(cmap)

        fig, ax = plt.subplots(dpi=100, figsize=(15, 15))
        ax.imshow(self.grid, cmap=cmap, norm=norm)

        fig.tight_layout()
        plt.axis('off')
        plt.show()

        plt.close()
