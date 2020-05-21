import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


COLORS = {1: 'red', 2: 'green', 5: 'blue'}


def main(sim_group, outfile_idx):
    if sim_group not in ['frame_rotation']:
        return
    print('  plotting accretion.vs_e0_and_m0')

    plt.figure(figsize=(8, 4))

    eccs = [0., 0.05, 0.1, 0.15, 0.2, 0.25]
    for mass_in_mJ in [1, 2, 5]:
        mpm0s = []
        for ecc in eccs:

            sim_id = f'{mass_in_mJ:.1f}mj_e{f"{ecc:.3f}"[1:]}'

            m = sim_params.planets.current_mass(
                sim_group, sim_id, outfile_idx
            )
            mpm0s.append(m / mass_in_mJ * 1000)

        plt.scatter(
            eccs, mpm0s, color=COLORS[mass_in_mJ],
            label='$m_0=' + str(mass_in_mJ) + '\ m_{jupiter}$'
        )

    plt.xlim(min(eccs) - 0.025, max(eccs) + 0.025)
    plt.ylim(0.9, 2.8)
    plt.xlabel('eccentricity $e_{planet}$')
    plt.ylabel('mass $m/m_0$')
    plt.legend(loc='upper left')
    # plt.gcf().subplots_adjust(left=.15)

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_e0_and_m0.pdf')
    plt.savefig(save_loc)



