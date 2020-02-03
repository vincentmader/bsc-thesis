import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FIGURE_DIR


def main():

    r = np.linspace(-5, 5, 100)
    Σ = lambda r, β: r**β

    fig = plt.figure(figsize=(4, 2))
    plt.plot(r, Σ(r, 1), color='black')
    plt.plot(r, -Σ(r, 1), color='black')
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    save_loc = os.path.join(FIGURE_DIR, 'flat_disk.pdf')
    plt.savefig(save_loc)
    plt.close()

    fig = plt.figure(figsize=(4, 2))
    plt.plot(r, Σ(r, 2), color='black')
    plt.plot(r, -Σ(r, 2), color='black')
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    save_loc = os.path.join(FIGURE_DIR, 'flaring_disk.pdf')
    plt.savefig(save_loc)
    plt.close()
