
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FIGURE_DIR
import plotting
import sim_params


def main(sim_group, sim_id, output_idx=None):
    if sim_group == '.DS_Store' or sim_id == '.DS_Store':
        return
    print('\n', sim_id, ' ', end='')

    # check whether save directory exists
    if not sim_id in os.path.join(FIGURE_DIR, sim_group):
        os.mkdir(os.path.join(FIGURE_DIR, sim_group, sim_id))
    path_to_sim_id_dir = os.path.join(FIGURE_DIR, sim_group, sim_id)
    if not 'all_gap_plots' in os.listdir(path_to_sim_id_dir):
        os.mkdir(os.path.join(path_to_sim_id_dir, 'all_gap_plots'))

    # setup pyplot figure
    fig = plt.figure(figsize=(8, 4))
    # plt.ylim()

    # loop over all output files, create png for each file
    nr_of_outputs = sim_params.general.nr_of_outputs(sim_group, sim_id)
    for iteration_step in range(nr_of_outputs + 1):
        # skip to output_idx, if specified
        if output_idx and iteration_step != output_idx:
            continue
        # plot some dots to better visualize progress
        sys.stdout.write('.')
        sys.stdout.flush()

        # plot 1D gas density for different eccentricities and initial masses (zoomed onto gap)
        ax = plt.gca()
        plotting.gas_density.linear_1D(
            ax, sim_group, sim_id, iteration_step,
            r_min=0.5, r_max=1.5
        )

        # save png
        png_save_path = os.path.join(FIGURE_DIR, sim_group, sim_id, 'all_gap_plots', f'{iteration_step}.png')
        plt.savefig(png_save_path)
        plt.clf()

    plt.close()


