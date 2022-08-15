
import numpy as np
import matplotlib.pyplot as plt

import setup
import sim_params


def main(ax, sim_group, sim_id, outfile_idx, label='', color='black'):

    # load 1D data as numpy array
    λ = setup.load_gas_density.sigma_1D_ascii(sim_group, sim_id, outfile_idx)

    x = np.array([float(row.split(' ')[0]) for row in λ])
    y = np.array([float(row.split(' ')[1]) for row in λ])

    if sim_group in ['frame_rotation', '50000_orbits']:
        sigma_unp = setup.sigma_unp(sim_group, sim_id, outfile_idx)

        if not y.shape == sigma_unp.shape:
            raise Exception('oh nooo, sigma_unp has different resolution!')

        y /= sigma_unp

    plt.semilogy(x, y, label=label, color=color)

