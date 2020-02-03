
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    if sim_group not in ['sigma_slope']:
        return

    print('  plotting accretion.sigma_slope')

    initial_masses, current_masses, slopes = [], [], []

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        outfile_idx = sim_params.general.nr_of_outputs(sim_group, sim_id)

        slope = sim_params.general.sigma_slope(sim_group, sim_id)
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)
        slopes.append(slope)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    mass_increase = current_masses / initial_masses
    slopes = np.array(slopes)

    # plot setup
    plt.figure(figsize=(4, 4))
    plt.xlim(0 - 0.05, max(slopes) + 0.05)
    plt.ylim(1.4, 1.9)
    nr_of_orbits = outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    #plt.title(f'mass accretion vs. flaring index (after {nr_of_orbits} orbits)')
    plt.xlabel(r'sigma slope')
    plt.ylabel(r'relative mass increase $m/m_0$')

    mpm0 = mass_increase
    plt.scatter(slopes, mpm0)

    # saving
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_flaring_idx.pdf')
    plt.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    sim_group = sys.argv[1]
    main(sim_group)

