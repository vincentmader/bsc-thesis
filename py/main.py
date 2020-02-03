""""""
import os
import warnings

import IPython.core.ultratb
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import analysis
import config
from config import FARGO_DIR, FIGURE_DIR
import plotting
import setup
import sim_params


def create_collage(sim_group):
    if sim_group not in ['migration', '50000_orbits']:
        return
    # loop over all simulation ids
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        # skip bullshit files
        if sim_id == '.DS_Store':
            continue
        setup.dir_structure.create_sim_id_dir(sim_group, sim_id)

        # create collage png files for all gas density output files
        plotting.collage.create_pngs(sim_group, sim_id)
        # create gif from png files
        plotting.collage.create_gif(sim_group, sim_id)


def create_polar_plot(sim_group, sim_id, outfile_idx, r_min=0.2, r_max=5.0, tick_step_size=0.2):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot(polar=True)
    plotting.gas_density.polar_2D(
        ax, sim_group, sim_id, outfile_idx, r_max_crop=1.4
    )
    save_loc = os.path.join(
        FIGURE_DIR, sim_group, sim_id, f'polar_{outfile_idx}.png'
    )
    plt.grid(True, color='black')
#    ticks = np.arange(r_min, r_max, tick_step_size)
    ticks = list(np.arange(0.5, 5.5, 1))
    plt.yticks(ticks, size=20)
    plt.rgrids(ticks)
    plt.plot(np.linspace(0, 2 * np.pi, 100), [0.2] * 100, color='black', linewidth=1)
    ax.set_rlabel_position(90)
    if sim_id.startswith('10') or outfile_idx == 50:
        cb = plt.colorbar(fraction=0.046, pad=0.04)
        cb.ax.tick_params(labelsize=20)
    if sim_id not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
        os.mkdir(os.path.join(FIGURE_DIR, sim_group, sim_id))
    plt.savefig(save_loc)


def main(sim_groups):

    for sim_group in sim_groups:
        setup.dir_structure.create_sim_group_dir(sim_group)

#    plotting.various.flaring_disk()
#    plotting.hill_sphere.kley(cells_per_rH=5)
#    plotting.hill_sphere.grid_cells_in_hill_sphere()

    outfile_idx = 50
    plotting.gas_density.sigma_vs_r_and_aspect_ratio(outfile_idx)
    plotting.gas_density.sigma_vs_r_and_machida(outfile_idx)
    plotting.gas_density.sigma_vs_r_and_flaring_idx(outfile_idx)
    plotting.gas_density.sigma_vs_r_and_resolution(10)
    plotting.gas_density.sigma_vs_r_and_sigma_slope(10)
    plotting.gas_density.sigma_vs_r_and_viscosity(outfile_idx)

    # create polar plots for first runs and resolution testing
    create_polar_plot('frame_rotation', '1.0mj_e.000', 1, r_min=0.2, r_max=5)
    create_polar_plot('frame_rotation', '1.0mj_e.000', 10, r_min=0.2, r_max=5)
    create_polar_plot('frame_rotation', '1.0mj_e.000', 50, r_min=0.2, r_max=5)

    create_polar_plot('frame_rotation', '1.0mj_e.300', 1, r_min=0.2, r_max=5)
    create_polar_plot('frame_rotation', '1.0mj_e.300', 10, r_min=0.2, r_max=5)
    create_polar_plot('frame_rotation', '1.0mj_e.300', 50, r_min=0.2, r_max=5)

#    for sim_id in os.listdir(os.path.join(FARGO_DIR, 'testing_cells_per_rH')):
#        if sim_id in ['.DS_Store']:
#            continue
#        print(sim_id)
#        create_polar_plot('testing_cells_per_rH', sim_id, 10, r_min=0.2, r_max=1.4)

    for sim_group in sim_groups:
        print(sim_group)

        #create_collage(sim_group)
#            # create plots for gap evolution over time
#            for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
#                plotting.gap.over_time.create_pngs(sim_group, sim_id)
#                plotting.gap.over_time.create_gif(sim_group, sim_id)

        if sim_group in ['frame_rotation', '10000_orbits', '50000_orbits']:
            plotting.gap.eccentricity.vs_planet_ecc(sim_group)
            plotting.gap.eccentricity.vs_initial_mass(sim_group)

            # plot 2D gas density vs radial distance (and ecc/m0)
            plotting.gas_density.sigma_vs_r_and_m0(sim_group, outfile_idx)
            plotting.gas_density.sigma_vs_r_and_e(sim_group, outfile_idx)
            if sim_group in ['frame_rotation']:
                plotting.gas_density.sigma_vs_r_and_e(sim_group, 10)
                plotting.gap.depth.vs_planet_ecc(sim_group)

        # create plots showing accretion vs time for different values
        # of initial planet mass and orbit eccentricity
        plotting.accretion.vs_time(sim_group)

        # create plots showing accretion vs eccentricity for different values
        # of initial planet mass
        plotting.accretion.vs_eccentricity(sim_group, 50)
        plotting.accretion.vs_e0_and_m0(sim_group, 50)
        plotting.accretion.vs_initial_mass(sim_group, 50)

        # create plot showing accretion vs Machida factor
        plotting.accretion.vs_machida(sim_group)
        # create plot showing accretion vs viscosity
        plotting.accretion.vs_viscosity(sim_group)
        # create plot showing accretion vs flaring index
        plotting.accretion.vs_flaring_idx(sim_group)
        # create plot showing accretion vs H/R
        plotting.accretion.vs_aspect_ratio(sim_group, 50)
        # create plot showing accretion vs sigma slope
        plotting.accretion.vs_sigma_slope(sim_group)

        # plot 2D gas density in polar coordinates after initialization
        # plotting.gas_density.initial_state(sim_group)
        # plot 2D gas density in polar coordinates for 3 different times
        plotting.gas_density.comparison_for_3_different_times(sim_group)

        plotting.migration.planet_ecc_vs_e0(sim_group)
        plotting.migration.planet_ecc_vs_m0(sim_group)
        plotting.migration.planet_ecc_vs_visc(sim_group)
        plotting.migration.planet_ecc_vs_t(sim_group)
        plotting.migration.planet_pos_vs_t_and_e0(sim_group)
        plotting.migration.planet_pos_vs_t_and_m0(sim_group)
        plotting.migration.planet_pos_vs_t_and_visc(sim_group)
        for acc_is_on in [True, False]:
            plotting.migration.semimajor_axis_vs_t_and_e0(sim_group, acc_is_on)


def custom():
    for sim_group in ['50000_orbits', '10000_orbits', 'frame_rotation']:
        plotting.gap.vs_initial_mass(sim_group)
        plotting.gap.vs_planet_ecc(sim_group)
#    for sim_group in ['frame_rotation']:
#        print(sim_group)
#        # create plots for gap evolution over time
#        for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
#            if sim_id in ['.DS_Store']:
#                continue
#            #plotting.gap_over_time.create_pngs(sim_group, sim_id)
#            #plotting.gap_over_time.create_gif(sim_group, sim_id)
#            #plotting.gap_eccentricity.vs_planet_ecc(sim_group)
#        plotting.gas_density.comparison_for_3_different_times(sim_group)


if __name__ == '__main__':

    sim_groups = [
#        'migration',
#        'testing_cells_per_rH',
#        'testing_visc',
        'frame_rotation',
#        '10000_orbits',
#        'aspect_ratio',
#        'machida',
#        'sigma_slope',     # not working yet, TODO: rerun sims?
#        'flaring_idx',
#        '50000_orbits',
    ]

#    plotting.gap.depth.vs_planet_ecc('frame_rotation')

#    sim_group = 'frame_rotation'
#    plotting.gas_density.sigma_vs_r_and_e(sim_group, 50)
#    plotting.gas_density.sigma_vs_r_and_e(sim_group, 10)

    main(sim_groups)
    #custom()

