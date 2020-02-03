import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi as π

import analysis
import config
from config import FIGURE_DIR


def colorplot_fred(r_H, cells_per_rH):

    arr = [
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
        [0] * 12
    ]

    for jdx, row in enumerate(arr):
        for idx, col in enumerate(row):
            dy = (jdx - 5.5) * r_H / cells_per_rH
            dx = (idx - 5.5) * r_H / cells_per_rH
            d = np.sqrt(dx**2 + dy**2)

            arr[jdx][idx] = analysis.accretion.kley.f_red(d, r_H)

    plt.figure(figsize=(4, 4))
    plt.imshow(arr, cmap='coolwarm', vmin=0, vmax=2./3)
    cb = plt.colorbar(fraction=0.046, pad=0.04)
    #cb.set_label('$f_{red}$')
    #plt.gcf().subplots_adjust(right=1.5)
    plt.xlim(-.5, 11.5)
    plt.ylim(-.5, 11.5)

    plt.xticks([0.5, 5.5, 10.5], ['$-r_H$', 0, '$r_H$'])
    plt.yticks([0.5, 5.5, 10.5], ['$-r_H$', 0, '$r_H$'])
#    plt.xticks(np.arange(-0.5, 2 * cells_per_rH + 2, 1), '')
#    plt.yticks(np.arange(-0.5, 2 * cells_per_rH + 2, 1), '')
#    plt.gca().grid(color='black', linewidth=1.5)
#    for tick in plt.gca().xaxis.get_major_ticks():
#        tick.tick1line.set_visible(False)
#        tick.tick2line.set_visible(False)
#    for tick in plt.gca().yaxis.get_major_ticks():
#        tick.tick1line.set_visible(False)
#        tick.tick2line.set_visible(False)

    for i in np.arange(-0.5, 12, 1):
        plt.plot([i]*2, [-2, 13], color='black', linewidth=1)
        plt.plot([-2, 13], [i]*2, color='black', linewidth=1)

    # add circle
    radius = cells_per_rH
    plt.gca().add_artist(
        plt.Circle(
            (5.5, 5.5, radius, radius),
            color='red', fill=False, linewidth=2, zorder=10
        )
    )

    # save
    save_loc = os.path.join(FIGURE_DIR, 'hill_sphere_kley_fred_1.pdf')
    plt.savefig(save_loc)
    plt.close()


def lineplot_fred():

    r = np.linspace(0, 2, 1000)
    r_H = 1

    f_red = [analysis.accretion.kley.f_red(i, r_H) for i in r]

    plt.figure(figsize=(4, 4))
    plt.plot(r, f_red)
    plt.xticks([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5])
    plt.yticks([0, 0.25, 0.5, 0.75])
    plt.xlim(0, 1)
    plt.ylim(-0.05, .7505)
    plt.xlabel('distance from planet center in $r_H$')
    plt.ylabel('$f_{red}$')
    plt.gcf().subplots_adjust(left=.2)
    plt.gcf().subplots_adjust(bottom=.175)

    save_loc = os.path.join(FIGURE_DIR, 'hill_sphere_kley_fred_2.pdf')
    plt.savefig(save_loc)
    plt.close()


def main(cells_per_rH=5):

    print('  plotting hill_sphere.kley')


    M, m = 1, 1e-3
    a, e = 1, 0
    r_H = analysis.hill_radius(M, m, a, e)

    colorplot_fred(r_H, cells_per_rH)
    lineplot_fred()

