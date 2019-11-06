
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import sys


# setup
SIMULATION_ID = sys.argv[1]

RES_r, RES_φ = 300, 600
r = np.linspace(0, RES_r - 1, RES_r)
φ = np.linspace(0, RES_φ - 1, RES_φ)

FIGURES_DIR = f'../figures/testing/{SIMULATION_ID}/'
if SIMULATION_ID not in os.listdir('../figures/testing/'):
    os.mkdir(FIGURES_DIR)

SIMULATION_DIR = '../fargo2d1d/first_tests/{SIMULATION_ID}/'

fig = plt.figure()
gs = GridSpec(2, 2, figure=fig)

# loop over all files in simulation output directory
for i in range(1000):

    # define file paths for 2d and 1d data, then load them in
    file_path_2d = f'{SIMULATION_DIR}out/gasdens{i}.dat'
    file_path_1d = f'{SIMULATION_DIR}out/gasdens1D{i}.dat'
    try:
        σ = np.log10(np.fromfile(f'{file_path_2d}').reshape(RES_r, RES_φ))
        λ = np.fromfile(f'{file_path_1d}')
    except FileNotFoundError:
        continue

    print(f'plotting data for file {i}')
    # rearange 2d array so that planet sits in the center of plot
    for row_idx, row in enumerate(σ):
        first_half = list(row)[:int(RES_φ / 2)]
        second_half = list(row)[int(RES_φ / 2):]
        σ[row_idx] = np.array(second_half + first_half)

    # plot 2d data in rectangular grid
    ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=2))
    plt.title('')
    plt.imshow(σ, origin='lower', aspect='auto')
    plt.xticks([])
    plt.yticks([])
    # plt.colorbar()

    # plot 2d data in polar coords
    ax2 = plt.subplot(gs.new_subplotspec((1, 0), colspan=1), projection='polar')
    plt.pcolormesh(σ)
    plt.xticks([])
    plt.yticks([])

    # plot 1d data
    ax2 = plt.subplot(gs.new_subplotspec((1, 1), colspan=1))
    plt.plot(λ)
    plt.xlim(0, 50)
    #plt.xticks([])
    #plt.yticks([])

    # save and reset figure
    plt.savefig(f'{FIGURES_DIR}plot{i}.png')
    plt.clf()

# create gif of all images that where created
#os.system(f'convert {FIGURES_DIR}*.png {FIGURES_DIR}evolution.gif')

