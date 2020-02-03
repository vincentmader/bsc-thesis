
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
    if sim_group not in ['aspect_ratio']:
        return

    print('  plotting accretion.vs_aspect_ratio')

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')

    initial_masses, current_masses, aspect_ratios = [], [], []
    # loop over all sim_ids with initial_mass of 1 M_J
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)
        aspect_ratio = sim_params.general.aspect_ratio(sim_group, sim_id)
        if aspect_ratio > 0.1:
            continue
        if aspect_ratio not in np.array(range(1, 11)) / 100:
            continue

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)
        aspect_ratios.append(aspect_ratio)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    planet_mass_increase = current_masses / initial_masses
    aspect_ratios = np.array(aspect_ratios)

    orbit_num = outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)

    # plot setup
    plt.figure(figsize=(4, 4))
    #plt.title(f'accretion for 1.0 {"$M_{jupiter}$"} planets after {orbit_num} orbits')
    plt.xlim(min(aspect_ratios) - 0.01, max(aspect_ratios) + 0.01)
    plt.ylim(0, 4)
    plt.xlabel('aspect ratio')
    plt.ylabel(r'planet mass increase $m/m_0$')  # at outfile_idx * nr_of_orbits_between_outputs
    plt.xticks(aspect_ratios)

    # plot
    plt.scatter(aspect_ratios, current_masses / initial_masses)

    # save
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_hr.pdf')
    plt.savefig(save_path)


if __name__ == '__main__':
    sim_group, outfile_idx = sys.argv[1], sys.argv[2]
    main(sim_group, outfile_idx)

