
import numpy as np
import matplotlib.pyplot as plt

import setup
import sim_params


def main(ax, sim_group, sim_id, out_file_idx, r_min=None, r_max=None):

    if not r_min:
        r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
    if not r_max:
        r_max = 5  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

    # load 1D data as numpy array
    λ = setup.load_gas_density.sigma_1D_ascii(sim_group, sim_id, out_file_idx)

    x = np.array([float(row.split(' ')[0]) for row in λ])
    y = [float(row.split(' ')[1]) for row in λ]

    plt.plot(x, y)

    plt.xlim(r_min, r_max)
    plt.ylim(0, 3.5e-4)
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'surface density $\sigma$ [code units]')

