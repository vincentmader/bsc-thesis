
import math
import os

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi as π

from config import FARGO_DIR
import sim_params, setup


def main(ax, sim_group, sim_id, iteration_step, r_min_crop=None, r_max_crop=None):

    CMAP = 'coolwarm'

    # get resolution
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    # get inner and outer boundary for radius
    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)

    # define path to 2D gas density file
    path_to_2D_data = os.path.join(
        FARGO_DIR, sim_group, sim_id, f'out/gasdens{iteration_step}.dat'
        # f'../fargo2d1d/{sim_group}/{sim_id}/out/gasdens{iteration_step}.dat'
    )
    # load gas density 2D array
    # Σ = np.fromfile(f'{path_to_2D_data}').reshape(res_r, res_φ)
    Σ = setup.load_gas_density.sigma_2D(sim_group, sim_id, iteration_step)
    # unp = setup.sigma_unp(sim_group, sim_id, iteration_step)
    # for row_idx, row in enumerate(Σ):
    #     print(Σ.shape)
    #     print(unp.shape)
    #     Σ[row_idx] /= unp

    if not 'unp' in sim_id:
        # get position of planet in disk
        r_planet, φ_planet = sim_params.planets.current_position_rφ(
            sim_group, sim_id, iteration_step
        )
        # convert position to indices of rows and columns in 2D array
        planet_col_idx = int(math.floor(φ_planet / (2*π) * res_φ))
        planet_row_idx = int(math.floor((1 - r_min) * res_r / (r_max - r_min)))
        # rearange 2D array so that planet sits at the same spot in each image
        for row_idx, row in enumerate(Σ):
            first_half = list(row)[:int(planet_col_idx)]
            second_half = list(row)[int(planet_col_idx):]
            Σ[row_idx] = np.array(second_half + first_half)
        # rearange 2D array so that planet sits in the center of plot
        for row_idx, row in enumerate(Σ):
            first_half = list(row)[:int(res_φ / 2)]
            second_half = list(row)[int(res_φ / 2):]
            Σ[row_idx] = np.array(second_half + first_half)

    # plot Σ against r and φ
    r = np.linspace(r_min, r_max, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)
    plt.pcolormesh(φ, r, np.log10(Σ), cmap=CMAP, vmin=-4.5, vmax=-2.5)

    # various
    plt.title('')
    plt.xticks([])
    plt.yticks([])

    plt.ylim(r_min_crop, r_max_crop)
