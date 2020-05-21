
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import analysis
import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    # make sure naming scheme is similar to '1mj_e.00'
    if sim_group not in ['frame_rotation', '10000_orbits', '50000_orbits']:
        return

    print('  plotting gap_eccentricity.vs_initial_mass')

    sim_ids = []
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store'] or 'unp' in sim_id:
            continue
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if ecc == 0.0 and mass % 1e-3 == 0:
            sim_ids.append(sim_id)

    planet_masses = []
    gap_eccs = []

    plt.figure(figsize=(4, 4))
    for sim_id in sim_ids:
        # get initial planet mass
        planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        # get gap eccentricity for last output file
        nr_of_outputs = sim_params.general.nr_of_outputs(sim_group, sim_id)
        gap_ecc = analysis.gap.eccentricity(sim_group, sim_id, nr_of_outputs)

        planet_masses.append(planet_mass)
        gap_eccs.append(gap_ecc)

    plt.scatter(planet_masses, gap_eccs)
    # plt.legend()
    plt.xlim(5e-4, max(planet_masses) + 5e-4)
    plt.ylim(0.1, 0.2)
    plt.xticks(planet_masses, [1, 2, 3, 4, 5])
    plt.yticks([0.1, 0.125, 0.15, 0.175, 0.2])
    plt.xlabel('mass $m_0/m_{jupiter}$')
    plt.ylabel('gap eccentricity $e_{gap}$')
    plt.gcf().subplots_adjust(left=.175)

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_ecc_vs_planet_mass.pdf')
    plt.savefig(save_loc)
    plt.close()
