
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    if sim_group not in ['machida']:
        return

    print('  plotting accretion.vs_machida')

    initial_masses, current_masses, machidas = [], [], []

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        iteration_step = sim_params.general.nr_of_outputs(sim_group, sim_id)

        machida = sim_params.planets.machida(sim_group, sim_id)
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, iteration_step)

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)
        machidas.append(machida)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    machida = np.array(machida)

    # plot setup
    plt.figure(figsize=(4, 4))
    plt.xlim(min(machidas) - 0.25, max(machidas) + 0.25)
    plt.ylim(1.2, 2.2)
    plt.xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    if sim_group in ['testing_visc']:
        # TODO: generalize
        plt.ylim(0.8, 2.2)
    #plt.title(f'mass accretion vs. Machida accretion factor after {iteration_step} orbits')
    plt.xlabel(r'accretion factor')
    plt.ylabel(r'relative mass increase $m/m_0$')

    mpm0 = current_masses / initial_masses
    plt.scatter(machidas, mpm0)

    # saving
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_machida.pdf')
    plt.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    sim_group = sys.argv[1]
    main(sim_group)

