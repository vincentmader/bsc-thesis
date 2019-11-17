
import os
from pprint import pprint

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


RES_r, RES_φ = 300, 600
r = np.linspace(0, RES_r - 1, RES_r)
φ = np.linspace(0, RES_φ - 1, RES_φ)

PLANET_POS_r, PLANET_POS_φ = 100, 0
HILL_RADIUS = 5

# define identifier for simulation
SIMULATION_ID = 'first_tests/ecc0'
# define location of simulation output files
SIM_OUTPUT_DIR = os.path.join('../fargo2d1d', SIMULATION_ID, 'out')
# define location where figures shall be saved to
FIGURE_DIR = os.path.join('../figures', SIMULATION_ID)


def load_data_for_iter_step(iter_step):

    # define file paths for 2D and 1D data
    file_path_1d = os.path.join(SIM_OUTPUT_DIR, f'gasdens1D{iter_step}.dat')
    file_path_2d = os.path.join(SIM_OUTPUT_DIR, f'gasdens{iter_step}.dat')

    # load in 2D density
    σ = np.fromfile(f'{file_path_2d}').reshape(RES_r, RES_φ)
    # load in 1D density
    λ = np.fromfile(f'{file_path_1d}')

    return σ, λ


planet_masses = []
# loop over all iteration steps
for iter_step in range(1000):

    # load in the data
    try:
        σ, λ = load_data_for_iter_step(iter_step)
    except FileNotFoundError:
        continue

    planet_mass = σ[PLANET_POS_r][PLANET_POS_φ]
    planet_masses.append(planet_mass)

    # # rearange 2d array so that planet sits in the center of plot
    # for row_idx, row in enumerate(σ):
    #     first_half = list(row)[:int(RES_φ / 2)]
    #     second_half = list(row)[int(RES_φ / 2):]
    #     σ[row_idx] = np.array(second_half + first_half)

    # # calculate mass in hill sphere
    # hill_sphere = []
    # for row_idx, row in enumerate(σ):
    #     tmp_row = []
    #     if row_idx not in range(PLANET_POS[0] - HILL_RADIUS, PLANET_POS[0] + HILL_RADIUS):
    #         continue
    #     for col_idx, col in enumerate(row):
    #         if col_idx not in range(PLANET_POS[1] - HILL_RADIUS, PLANET_POS[1] + HILL_RADIUS):
    #             continue
    #         tmp_row.append(col)
    #     hill_sphere.append(tmp_row)
    # pprint(hill_sphere)
    # input()
    # mass_in_hill_sphere = sum(np.array(hill_sphere))

fig = plt.figure()
ax = plt.subplot()

ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.2e'))

plt.plot(planet_masses)
plt.xlabel('iteration step')
plt.ylabel(r'planet mass [$M_{\odot}$]')
plt.savefig(os.path.join(FIGURE_DIR, 'mass_evolution.png'))

