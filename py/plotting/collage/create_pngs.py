
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR
from config import FIGURE_DIR
import sim_params
import plotting


def main(sim_group, sim_id, output_idx=None):

    if sim_group == '.DS_Store' or sim_id == '.DS_Store':
        return

    nr_of_outputs = sim_params.general.nr_of_outputs(sim_group, sim_id)

    print('\npng for', sim_group, sim_id, ' ', end='')

    # define location of simulation output files
    out_file_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')

    # define list with names of all simulation output file names
    all_out_file_names = sorted(os.listdir(out_file_dir))
    # check whether there are any simulation output files, return if not
    if not all_out_file_names:
        return
    # only create png for parameter output_idx (for all outfiles if none given)
    if output_idx:
        all_out_file_names = [all_out_file_names[output_idx]]

    # create figure and initialize grid
    fig = plt.figure(figsize=(15, 10))
    gs = mpl.gridspec.GridSpec(2, 3, figure=fig)

    # loop over all simulation output files
    for iteration_step in range(nr_of_outputs + 1):
        # skip to output_idx, if specified
        if output_idx and iteration_step != output_idx:
            continue
        # plot some dots to better visualize progress
        sys.stdout.write('.')
        sys.stdout.flush()

        # plot 2D gas density in rectangular grid
        ax1 = fig.add_subplot(gs.new_subplotspec((0, 0), colspan=3))
        plotting.gas_density.cartesian_2D(
            ax1, sim_group, sim_id, iteration_step, plot_gap_bounds=True
        )
        # create info box
        ax2 = plt.subplot(gs.new_subplotspec((1, 1), colspan=1))
        plotting.collage.info_box(ax2, sim_group, sim_id, iteration_step)
        # plot 1d data
        ax3 = plt.subplot(gs.new_subplotspec((1, 0), colspan=1))
        plotting.gas_density.linear_1D(ax3, sim_group, sim_id, iteration_step)
        # plot 2D gas density in polar coordinates
        ax4 = plt.subplot(gs.new_subplotspec((1, 2), colspan=1), projection='polar')
        plotting.gas_density.polar_2D(
            ax4, sim_group, sim_id, iteration_step
        )

        # make sure sorting of files will work fine
        if 9 < iteration_step < 100:
            iteration_step = f'0{iteration_step}'
        elif iteration_step < 10:
            iteration_step = f'00{iteration_step}'
        # make sure necessary directories exist for saving collages
        png_save_loc = os.path.join(
            FIGURE_DIR, sim_group, sim_id, f'all_collages/collage_{iteration_step}.png'
        )
        sim_id_fig_dir = os.path.join(FIGURE_DIR, sim_group, sim_id)
        if 'all_collages' not in os.listdir(sim_id_fig_dir):
            all_collages_dir = os.path.join(sim_id_fig_dir, 'all_collages')
            os.system(f'mkdir "{all_collages_dir}"')

        # save
        plt.savefig(png_save_loc)
        # also save collage for last iteration step as high quality pdf
        if iteration_step == nr_of_outputs:
            pdf_save_loc = os.path.join(
                FIGURE_DIR, sim_group, sim_id, f'collage_for_output_{iteration_step}.pdf'
            )
            plt.savefig(pdf_save_loc)

        plt.clf()

    # close figure
    plt.close()

