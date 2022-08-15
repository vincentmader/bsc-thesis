import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import config
from config import FIGURE_DIR


def main():

    r = np.linspace(2, 20, 100)
    Σ = lambda r, β: 0.25 * r**β

    fig = plt.figure(figsize=(4, 2))
    plt.plot(r, Σ(r, 1) + .5, color='black')
    plt.plot(r, -Σ(r, 1) - .5, color='black')
    plt.plot(-r, Σ(r, 1) + .5, color='black')
    plt.plot(-r, -Σ(r, 1) - .5, color='black')
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-20, 20)
    plt.ylim(-10, 10)
    plt.axis('off')
    circ = plt.Circle((0, 0), 1, color='black')
    plt.gca().add_artist(circ)
    save_loc = os.path.join(FIGURE_DIR, 'flat_disk.pdf')
    plt.savefig(save_loc)
    plt.close()

    fig = plt.figure(figsize=(4, 2))
    plt.plot(r, Σ(r, 2) + 7, color='black')
    plt.plot(r, -Σ(r, 2) - 7, color='black')
    plt.plot(-r, Σ(r, 2) + 7, color='black')
    plt.plot(-r, -Σ(r, 2) - 7, color='black')
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-20, 20)
    plt.ylim(-100, 100)
    plt.axis('off')
    circ = mpl.patches.Ellipse((0, 0), 2, 20, color='black')
    plt.gca().add_artist(circ)
    save_loc = os.path.join(FIGURE_DIR, 'flaring_disk.pdf')
    plt.savefig(save_loc)
    plt.close()
