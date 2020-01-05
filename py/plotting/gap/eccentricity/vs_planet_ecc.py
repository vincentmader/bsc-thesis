
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

    sim_ids = []
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if initial_mass == 1e-3:  # TODO: small variations should also be ok
            sim_ids.append(sim_id)

    planet_eccs = []
    gap_eccs_inner = []
    gap_eccs_outer = []

    plt.figure(figsize=(8, 4))

    for sim_id in sim_ids:
        # get initial planet eccentricity
        planet_ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        # get gap eccentricity for last output file
        nr_of_outputs = sim_params.general.nr_of_outputs(sim_group, sim_id)
        gap_ecc_inner, gap_ecc_outer = analysis.gap.eccentricity(sim_group, sim_id, nr_of_outputs)

        planet_eccs.append(planet_ecc)
        gap_eccs_inner.append(gap_ecc_inner)
        gap_eccs_outer.append(gap_ecc_outer)

    plt.scatter(planet_eccs, gap_eccs_inner, label='inner')
    plt.scatter(planet_eccs, gap_eccs_outer, label='outer')
    plt.legend()
    plt.grid(True)

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_ecc_vs_planet_ecc.pdf')
    plt.savefig(save_loc)
    plt.close()

