
import numpy as np
import matplotlib.pyplot as plt

import setup
import sim_params


def main(ax, sim_group, sim_id, out_file_idx, label='', color='black'):

    # load 1D data as numpy array
    λ = setup.load_gas_density.sigma_1D_ascii(sim_group, sim_id, out_file_idx)

    x = np.array([float(row.split(' ')[0]) for row in λ])
    y = [float(row.split(' ')[1]) for row in λ]

    plt.semilogy(x, y, label=label, color=color)

