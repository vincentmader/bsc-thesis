import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def plot(acc=False):
    sim_group = 'migration'

    plt.figure(figsize=(4, 4))

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store'] or 'unp' in sim_id:
            continue

        if sim_id.endswith('acc') and not acc:
            continue
        if not sim_id.endswith('acc') and acc:
            continue

        ecc0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if mass != 1e-3:
            continue

        eccs = []
        for outfile_idx in range(sim_params.general.nr_of_outputs(sim_group, sim_id) + 1):
            ecc = sim_params.planets.current_eccentricity(sim_group, sim_id, outfile_idx)
            eccs.append(ecc)

        plt.plot(eccs)
        plt.xlabel('time in orbits')
        plt.ylabel('eccentricity of planet orbit')
        plt.xlim(0, len(eccs))
        plt.gcf().subplots_adjust(left=.175)

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'final_ecc_vs_t_and_e0')
    save_loc += '_acc.pdf' if acc else '.pdf'
    plt.savefig(save_loc)



def main(sim_group):

    if sim_group not in ['migration']:
        return

    plot(acc=True)
    plot(acc=False)


