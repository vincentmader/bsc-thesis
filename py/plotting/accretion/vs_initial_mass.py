
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import config
from config import FARGO_DIR
from config import FIGURE_DIR
import sim_params


WANTED_ECCENTRICITY = 0.


def main(sim_group, outfile_idx):

    # TODO: also allow for other sim_groups ?
    if sim_group not in ['frame_rotation']:
        return

    print('  plotting accretion.vs_initial_mass')

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')

    initial_masses, current_masses, initial_masses = [], [], []
    # loop over all sim_ids with initial_mass of 1 M_J
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store'] or 'unp' in sim_id:
            continue

        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)
        eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if (eccentricity - WANTED_ECCENTRICITY) / initial_mass > 0.05:
            continue

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    planet_mass_increase = current_masses / initial_masses

    orbit_num = outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)

    # plot setup for mpm0 vs m0
    plt.figure(figsize=(4.5, 4))  # (8, 4))
    #plt.title(f'accretion for 1.0 {"$M_{jupiter}$"} planets after {orbit_num} orbits')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
    plt.xlim(min(initial_masses) - 0.5e-3, max(initial_masses) + 0.5e-3)
    plt.ylim(.9 * min(planet_mass_increase), 2.8)
    plt.xlabel('initial mass $m_0$')
    plt.ylabel(r'relative mass increase $m/m_0$')  # at outfile_idx * nr_of_orbits_between_outputs
    plt.xticks(initial_masses)
    if sim_group == 'frame_rotation':
        plt.gcf().subplots_adjust(left=0.2)
    # plot
    plt.scatter(initial_masses, current_masses / initial_masses)
    # save
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_m0.pdf')
    plt.savefig(save_path)
    plt.close()

    # plot setup for m vs m0
    plt.figure(figsize=(4.5, 4))  # (8, 4))
    #plt.title(f'accretion for 1.0 {"$M_{jupiter}$"} planets after {orbit_num} orbits')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    plt.xlim(min(initial_masses) - 0.5e-3, max(initial_masses) + 0.5e-3)
    plt.ylim(1e-3, 6e-3)
    plt.xlabel('initial mass $m_0$')
    plt.ylabel(r'absolute planet mass')  # at outfile_idx * nr_of_orbits_between_outputs
    plt.xticks(initial_masses)
    if sim_group == 'frame_rotation':
        plt.gcf().subplots_adjust(left=0.2)
    # plot
    plt.scatter(initial_masses, current_masses)
    # save
    save_path = os.path.join(FIGURE_DIR, sim_group, 'm_vs_m0.pdf')
    plt.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    sim_group, outfile_idx = sys.argv[1], sys.argv[2]
    main(sim_group, outfile_idx)

