#!/usr/local/bin/python3
# -*- coding: utf8 -*-

from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np


def plot_hill_sphere(cells_per_rH):
    """

    Parameters
    ----------
    cells_per_rH: number of cells in Hill radius

    Returns
    --------


    """

    dim = int(2 * (cells_per_rH))
    shape = (dim, dim)
    print(cells_per_rH, shape)

    arr = np.zeros(shape=shape)
    for row_idx, row in enumerate(arr):
        Δrow = dim / 2. - (row_idx)
        Δrow -= 0.5 if 2 * cells_per_rH % 2 != 0 else 0
        for col_idx, col in enumerate(row):
            Δcol = dim / 2. - (col_idx)
            Δcol -= 0.5 if 2 * cells_per_rH % 2 != 0 else 0
            if Δcol**2 + Δrow**2 < cells_per_rH**2:
                arr[row_idx][col_idx] = 1

    diameter = 2 * (cells_per_rH)
    shape = diameter, diameter

    pprint(arr)
    # scale cells_per_rH up by factors of 2 until its an integer, remember factor
    # make plot, rescale grid by 1 / factor

    plt.imshow(arr, cmap='Greys', vmin=0, vmax=2)


    if cells_per_rH != int(cells_per_rH):
        plt.xlim(-1.5, dim + .5)
        plt.ylim(-1.5, dim + .5)
        plt.gca().add_artist(plt.Circle((dim / 2 - .5, dim / 2 - .5), cells_per_rH, color='red', fill=False))
    else:
        plt.xlim(-.5, dim + .5)
        plt.ylim(-.5, dim + .5)
        plt.gca().add_artist(plt.Circle((dim / 2, dim / 2), cells_per_rH, color='red', fill=False))
    plt.xticks(np.arange(-1, dim, 1) + .5, '')
    plt.yticks(np.arange(-1, dim, 1) + .5, '')
    plt.grid(color='black')

    for tick in plt.gca().xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
    for tick in plt.gca().yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)


if __name__ == '__main__':
    plt.figure(figsize=(6, 2))

    cells_per_rH = [2.5, 5, 10]
    for idx, cprH in enumerate(cells_per_rH):
        plt.subplot(1, len(cells_per_rH), idx + 1)
        plot_hill_sphere(cprH)
    plt.savefig('../figures/hill_sphere.pdf')

