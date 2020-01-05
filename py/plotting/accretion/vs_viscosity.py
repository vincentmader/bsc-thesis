
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    if sim_group not in ['testing_visc']:
        return

    initial_masses, current_masses, viscosities = [], [], []

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        iteration_step = sim_params.general.nr_of_outputs(sim_group, sim_id)

        viscosity = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, iteration_step)

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)
        viscosities.append(viscosity)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    viscosities = np.array(viscosities)

    # plot setup
    plt.figure(figsize=(8, 4))
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(1e-5, 1e-1)
    #plt.ylim(1, 10)
    #plt.grid(True)
    plt.title(f'mass accretion vs. viscosity after {iteration_step} orbits')
    plt.xlabel(r'viscosity parameter $\alpha_v$')
    plt.ylabel(r'$m/m_0$')

    mpm0 = current_masses / initial_masses
    plt.scatter(viscosities, mpm0)

    # saving
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_visc.pdf')
    plt.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    sim_group = sys.argv[1]
    main(sim_group)

