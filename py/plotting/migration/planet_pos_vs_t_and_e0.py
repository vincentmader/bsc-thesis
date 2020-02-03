import os, sys

import matplotlib.pyplot as plt
import numpy as np

import config, setup, sim_params
from config import FARGO_DIR, FIGURE_DIR


def main(sim_group):

    if sim_group not in ['migration']:
        return
    print('  plotting.migration.planet_pos_vs_t_and_e0')

    initial_eccs, initial_eccs_with_acc, sigmas = [], [], []

    fig = plt.figure(figsize=(8, 4))

    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        # get initial eccentricity, initial mass and gas disk viscosity
        ecc_0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        m_0 = sim_params.planets.initial_mass(sim_group, sim_id)
        α = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
        if not (m_0 == 1e-3 and α == 1e-2):
            continue

        rs = []
        for outfile_idx in range(0, 1000):
            try:
                r, φ = sim_params.planets.current_position_rφ(
                    sim_group, sim_id, outfile_idx
                )
                rs.append(r)
            except IndexError:
                continue

        plt.plot(rs, label='$e_0=' + str(ecc_0) + '$')



    plt.legend()

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'planet_pos_vs_t_and_e0.pdf')
    plt.savefig(save_loc)

