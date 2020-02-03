
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import plotting
import sim_params


def main(sim_group):

    if sim_group not in ['frame_rotation']:
        return
    print('  comparison_for_3_different_times')

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        plt.figure(figsize=(16, 7))

        subplot_idx = 1
        for outfile_idx in [1, 10, 50]:

            ax = plt.subplot(1, 3, subplot_idx, projection='polar')
            plotting.gas_density.polar_2D(
                ax, sim_group, sim_id, outfile_idx,
                r_min_crop=0.2, r_max_crop=2.5
            )
            nr_of_orbits = sim_params.general.nr_of_iterations_per_output(sim_group, sim_id) * outfile_idx
            #plt.title(f'after {nr_of_orbits} orbits', size=24)
            subplot_idx += 1

        # plt.colorbar()
        if sim_id not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
            os.mkdir(os.path.join(FIGURE_DIR, sim_group, sim_id))
        plt.savefig(os.path.join(FIGURE_DIR, sim_group, sim_id, 'sigma_for_various_times.png'))
        plt.close()

