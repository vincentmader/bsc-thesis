
import os
import warnings

import IPython.core.ultratb
import matplotlib.pyplot as plt
import numpy as np

import analysis
import config
from config import FARGO_DIR
from config import FIGURE_DIR
import plotting
import setup
import sim_params


def create_collage(sim_group):
    # loop over all simulation ids
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        # skip bullshit files
        if sim_id == '.DS_Store':
            continue
        if sim_id in ['1mj_e.05']:
            continue
        setup.dir_structure.create_sim_id_dir(sim_group, sim_id)

        # create collage png files for all gas density output files
        plotting.collage.create_pngs(sim_group, sim_id)
        # create gif from png files
        plotting.collage.create_gif(sim_group, sim_id)


def main(sim_groups):
    for sim_group in sim_groups:
        print(sim_group)
        setup.dir_structure.create_sim_group_dir(sim_group)
#        create_collage(sim_group)
        # create plots for gap evolution over time
#        for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
#            plotting.gap.over_time.create_pngs(sim_group, sim_id)
#            plotting.gap.over_time.create_gif(sim_group, sim_id)
        plotting.gap.eccentricity.vs_planet_ecc(sim_group)
        # create plots showing accretion vs time for different values
        # of initial planet mass and orbit eccentricity
        plotting.accretion.vs_time(sim_group)
        # create plots showing accretion vs eccentricity for different values
        # of initial planet mass
        plotting.accretion.vs_eccentricity(sim_group, 50)
        # create plot showing accretion vs viscosity
        plotting.accretion.vs_viscosity(sim_group)
        # plot 2D gas density vs radial distance (and ecc/m0)
        out_file_idx = 50
        plotting.gas_density.compare_log_1D(sim_group, out_file_idx)
        # plot 2D gas density in polar coordinates after initialization
        #plotting.gas_density.initial_state(sim_group)
        # plot 2D gas density in polar coordinates for 3 different times
        plotting.gas_density.comparison_for_3_different_times(sim_group)


def custom():
    for sim_group in ['frame_rotation']:
        print(sim_group)
        # create plots for gap evolution over time
        for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
            if sim_id in ['.DS_Store']:
                continue
            #plotting.gap_over_time.create_pngs(sim_group, sim_id)
            #plotting.gap_over_time.create_gif(sim_group, sim_id)
            #plotting.gap_eccentricity.vs_planet_ecc(sim_group)
        plotting.gas_density.comparison_for_3_different_times(sim_group)


if __name__ == '__main__':
    sim_groups = [
        '50000_orbits',
        '10000_orbits', 'testing_visc', 'frame_rotation',
        'testing_cells_per_rH', 'testing_visc'
    ]
    #main(sim_groups)
    custom()

