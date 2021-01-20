import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FIGURE_DIR


ELEGANCE_IS_DIFFERENT = {
    2.5 : [
        [0] * 7,
        [0] * 2 + [1] * 3 + [0] * 2,
        [0] + [1] * 5 + [0],
        [0] + [1] * 5 + [0],
        [0] + [1] * 5 + [0],
        [0] * 2 + [1] * 3 + [0] * 2,
        [0] * 7
    ], 5: [
        [0] * 12,
        [0] * 4 + [1] * 4 + [0] * 4,
        [0] * 2 + [1] * 8 + [0] * 2,
        [0] * 2 + [1] * 8 + [0] * 2,
        [0] + [1] * 10 + [0],
        [0] + [1] * 10 + [0],
        [0] + [1] * 10 + [0],
        [0] + [1] * 10 + [0],
        [0] * 2 + [1] * 8 + [0] * 2,
        [0] * 2 + [1] * 8 + [0] * 2,
        [0] * 4 + [1] * 4 + [0] * 4,
        [0] * 12,
    ], 10: [
        [0] * 22,
        [0] * 8 + [1] * 6 + [0] * 8,
        [0] * 6 + [1] * 10 + [0] * 6,
        [0] * 4 + [1] * 14 + [0] * 4,
        [0] * 3 + [1] * 16 + [0] * 3,
        [0] * 3 + [1] * 16 + [0] * 3,
        [0] * 2 + [1] * 18 + [0] * 2,
        [0] * 2 + [1] * 18 + [0] * 2,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 1 + [1] * 20 + [0] * 1,
        [0] * 2 + [1] * 18 + [0] * 2,
        [0] * 2 + [1] * 18 + [0] * 2,
        [0] * 3 + [1] * 16 + [0] * 3,
        [0] * 3 + [1] * 16 + [0] * 3,
        [0] * 4 + [1] * 14 + [0] * 4,
        [0] * 6 + [1] * 10 + [0] * 6,
        [0] * 8 + [1] * 6 + [0] * 8,
        [0] * 22
    ]
}




def main():

    print('  plotting hill_sphere.grid_cells_in_hill_sphere')

    for cells_per_rH in [2.5, 5, 10]:

        # try loading array
        try:
            arr = ELEGANCE_IS_DIFFERENT[cells_per_rH]
        except KeyError:
            raise KeyError('Oh crap, work ahead...')

        # define diameter of circle and make sure it can be used for shape
        circle_diameter = 2 * cells_per_rH
        if float(int(circle_diameter)) != circle_diameter:
            raise Exception('oh nooo')
        circle_diameter = int(circle_diameter)

        plt.figure(figsize=(4, 4))
        plt.imshow(arr, cmap='Greys', vmin=0, vmax=2)

        plt.gca().add_artist(
            plt.Circle(
                (circle_diameter / 2 + .5, circle_diameter / 2 + .5), cells_per_rH,
                color='red', fill=False, linewidth=2
            )
        )

        # create grid
        plt.xticks(np.arange(-0.5, circle_diameter + 2, 1), '')
        plt.yticks(np.arange(-0.5, circle_diameter + 2, 1), '')
        plt.gca().grid(color='black', linewidth=1.5)
        for tick in plt.gca().xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
        for tick in plt.gca().yaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)

        if cells_per_rH == 2.5:
            cells_per_rH = '2,5'
        save_loc = os.path.join(FIGURE_DIR, f'hill_sphere_{cells_per_rH}_cells.pdf')
        plt.savefig(save_loc)
        plt.close()

