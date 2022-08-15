import os

import matplotlib.pyplot as plt
import numpy as np

from config import FIGURE_DIR


def main():

    f = lambda r: min(0.14, 0.83 * r ** (4.5))

    x = np.linspace(0, 1, 100)
    y = [f(r) for r in x]

    plt.plot(x, y)

    save_loc = os.path.join(FIGURE_DIR, 'machida.pdf')
    plt.savefig(save_loc)
