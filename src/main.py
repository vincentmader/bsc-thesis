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


def polar_plots(sim_group):
    sim_group_dir = os.path.join(FARGO_DIR, sim_group)
    for sim_id in sorted(os.listdir(sim_group_dir)):
        if sim_id in ['.DS_Store']:
            continue
        # if sim_id not in ['1.0mj_e.000', '1.0mj_e.100', '1.0mj_e.200']:
        # if sim_id not in ['5.0mj_e.000', '3.0mj_e.000']:
            # continue
        # ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        # if ecc not in [0.1]:
        #     continue
        nr_of_outfiles = sim_params.general.nr_of_outputs(
            sim_group, sim_id
        )
        fig = plt.figure(figsize=(8, 8))
        save_loc = os.path.join(FIGURE_DIR, sim_group, sim_id)
        if 'polar' not in os.listdir(save_loc):
            os.mkdir(os.path.join(save_loc, 'polar'))
        for outfile_idx in range(nr_of_outfiles + 1):
            # if outfile_idx > 0:
            #     continue
            print(sim_id, outfile_idx)
            ax = plt.subplot(111, projection='polar')
            plotting.gas_density.polar_2D(
                ax, sim_group, sim_id, outfile_idx
            )
            # plt.title(f'{outfile_idx * 10} orbits', size=20)
            cbar = plt.colorbar(fraction=0.046, pad=0.04)
            plt.text(0, 7.5, '$log(\Sigma)$', fontsize=20)
            plt.text(np.pi * 3 / 2, 6, f'$t=${outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)} orbits', size=20, fontsize=20)
            plt.gcf().subplots_adjust(right=0.8)

            plt.grid(True, color='black')
            # ticks = np.arange(r_min, r_max, tick_step_size)
            ticks = [0.2, 1.0, 2.0, 3.0, 4.0, 5.0]
            plt.yticks(ticks, size=12)
            plt.rgrids(ticks)
            plt.plot(np.linspace(0, 2 * np.pi, 100), [0.2] * 100, color='black', linewidth=1)
            ax.set_rlabel_position(90)

            orbits = outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
            filename = str(orbits)
            if orbits < 10000 and sim_group in ['10000_orbits', '50000_orbits']:
                filename = f'0{filename}'
            if orbits < 1000:
                filename = f'0{filename}'
                if orbits < 100:
                    filename = f'0{filename}'
                    if orbits < 10:
                        filename = f'0{filename}'
            filename2 = str(orbits + 25)
            # if orbits + 25 < 1000:
            #     filename2 = f'0{filename2}'
            #     if orbits + 25 < 100:
            #         filename2 = f'0{filename2}'
            #         if orbits + 25 < 10:
            #             filename2 = f'0{filename2}'

            plt.savefig(os.path.join(save_loc, f'polar/{filename}.png'))
            # plt.savefig(os.path.join(save_loc, f'polar/{filename2}.png'))
            plt.clf()

        save_loc = os.path.join(save_loc, 'polar')
        all_pngs = ' '.join([
            f'"{os.path.join(save_loc, i)}"' for i in sorted(os.listdir(save_loc))
        ])
        gif_loc = os.path.join(save_loc, 'evolution.gif')
        os.system(f'convert {all_pngs} "{gif_loc}"')

        mp4_loc = os.path.join(save_loc, 'evolution.mp4')
        os.system(f'gif2vid {gif_loc} {mp4_loc}')

def gap_profile_plots(sim_group):
    sim_group_dir = os.path.join(FARGO_DIR, sim_group)
    for sim_id in sorted(os.listdir(sim_group_dir)):
        if sim_id in ['.DS_Store']:
            continue
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if ecc not in [0.1]:
            continue
        nr_of_outfiles = sim_params.general.nr_of_outputs(
            sim_group, sim_id
        )
        fig = plt.figure(figsize=(8, 8))
        save_loc = os.path.join(FIGURE_DIR, sim_group, sim_id)
        if 'gap_profile' not in os.listdir(save_loc):
            os.mkdir(os.path.join(save_loc, 'gap_profile'))
        for outfile_idx in range(nr_of_outfiles + 1):
            # if outfile_idx > 0:
            #     continue
            print(sim_id, outfile_idx)
            ax = plt.subplot(111)
            plotting.gas_density.logarithmic_1D(ax, sim_group, sim_id, outfile_idx)
            plt.xlim(0.5, 1.5)
            plt.ylim(0.1, 2.0)
#            ax = plt.subplot(111, projection='polar')
#            plotting.gas_density.polar_2D(
#                ax, sim_group, sim_id, outfile_idx
#            )
#            # plt.title(f'{outfile_idx * 10} orbits', size=20)
#            cbar = plt.colorbar(fraction=0.046, pad=0.04)
#            plt.text(0, 7.5, '$log(\Sigma)$', fontsize=20)
#            plt.text(np.pi * 3 / 2, 6, f'$t=${outfile_idx * 10} orbits', size=20, fontsize=20)
#            plt.gcf().subplots_adjust(right=0.8)
            filename = outfile_idx
            if outfile_idx < 100:
                filename = f'0{filename}'
                if outfile_idx < 10:
                    filename = f'0{filename}'

            plt.savefig(os.path.join(save_loc, f'gap_profile/{filename}.png'))
            plt.clf()

        save_loc = os.path.join(save_loc, 'gap_profile')
        all_pngs = ' '.join([
            f'"{os.path.join(save_loc, i)}"' for i in sorted(os.listdir(save_loc))
        ])
        gif_loc = os.path.join(save_loc, 'evolution.gif')
        os.system(f'convert {all_pngs} "{gif_loc}"')


def main(sim_groups):

    for sim_group in sim_groups:
        setup.dir_structure.create_sim_group_dir(sim_group)

#    plotting.various.flaring_disk()
    # plotting.hill_sphere.kley(cells_per_rH=5)
   # plotting.hill_sphere.grid_cells_in_hill_sphere()

    # outfile_idx = 50
    # plotting.gas_density.sigma_vs_r_and_aspect_ratio(outfile_idx)
    # plotting.gas_density.sigma_vs_r_and_machida(outfile_idx)
    # plotting.gas_density.sigma_vs_r_and_flaring_idx(outfile_idx)
    # plotting.gas_density.sigma_vs_r_and_resolution(10)
    # plotting.gas_density.sigma_vs_r_and_sigma_slope(10)
    # plotting.gas_density.sigma_vs_r_and_viscosity(outfile_idx)

    # # create polar plots for first runs and resolution testing
    # create_polar_plot('frame_rotation', '1.0mj_e.000', 1, r_min=0.2, r_max=5)
    # create_polar_plot('frame_rotation', '1.0mj_e.000', 10, r_min=0.2, r_max=5)
    # create_polar_plot('frame_rotation', '1.0mj_e.000', 50, r_min=0.2, r_max=5)

    # create_polar_plot('frame_rotation', '1.0mj_e.300', 1, r_min=0.2, r_max=5)
    # create_polar_plot('frame_rotation', '1.0mj_e.300', 10, r_min=0.2, r_max=5)
    # create_polar_plot('frame_rotation', '1.0mj_e.300', 50, r_min=0.2, r_max=5)

#    for sim_id in os.listdir(os.path.join(FARGO_DIR, 'testing_cells_per_rH')):
#        if sim_id in ['.DS_Store']:
#            continue
#        print(sim_id)
#        create_polar_plot('testing_cells_per_rH', sim_id, 10, r_min=0.2, r_max=1.4)

    for sim_group in sim_groups:
        print(sim_group)

        # create_collage(sim_group)
        # # create plots for gap evolution over time
        # for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        #     plotting.gap.over_time.create_pngs(sim_group, sim_id)
        #     plotting.gap.over_time.create_gif(sim_group, sim_id)

        if sim_group in ['frame_rotation', '10000_orbits', '50000_orbits']:
            # plot 2D gas density vs radial distance (and ecc/m0)
            plotting.gas_density.sigma_vs_r_and_m0(sim_group, outfile_idx)
            plotting.gas_density.sigma_vs_r_and_e(sim_group, outfile_idx)
            if sim_group in ['frame_rotation']:
                plotting.gas_density.sigma_vs_r_and_e(sim_group, 10)
                plotting.gap.depth.vs_planet_ecc(sim_group)
                plotting.gap.eccentricity.vs_planet_ecc(sim_group)
                plotting.gap.eccentricity.vs_initial_mass(sim_group)
                plotting.gap.depth.vs_planet_ecc(sim_group)

        # create plots showing accretion vs time for different values
        # of initial planet mass and orbit eccentricity
        plotting.accretion.vs_time(sim_group)

        # create plots showing accretion vs eccentricity for different values
        # of initial planet mass
        if sim_group in ['frame_rotation']:
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
        ## plotting.gas_density.initial_state(sim_group)
        # plot 2D gas density in polar coordinates for 3 different times
        ## plotting.gas_density.comparison_for_3_different_times(sim_group)
        if sim_group in ['migration']:
            plotting.migration.planet_ecc_vs_e0(sim_group)
            plotting.migration.planet_ecc_vs_m0(sim_group)
            plotting.migration.planet_ecc_vs_visc(sim_group)
        # plotting.migration.planet_ecc_vs_t_and_e0()
        # plotting.migration.planet_ecc_vs_t_and_m0()
        # plotting.migration.planet_ecc_vs_t_and_visc()

        # plotting.migration.planet_pos_vs_t_and_e0(sim_group)
        # plotting.migration.planet_pos_vs_t_and_m0(sim_group)
        # plotting.migration.planet_pos_vs_t_and_visc(sim_group)
        for acc_is_on in [True, False]:
            plotting.migration.semimajor_axis_vs_t(acc_is_on)
            plotting.migration.planet_ecc_vs_t(acc_is_on)


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
        # 'migration',
        # 'testing_cells_per_rH',
        'testing_visc',
        # 'frame_rotation',
        # '10000_orbits',
        # 'aspect_ratio',
        # 'machida',
        # 'presentation_5000_orbits',
        # 'presentation_500_orbits',
        # 'sigma_slope',     # not working yet, TODO: rerun sims?
        # 'flaring_idx',
        # '50000_orbits',
    ]

    # plot 2D gas density in polar coordinates for 3 different times
    # plotting.gas_density.comparison_for_3_different_times('migration')

    # fig = plt.figure(figsize=(8, 8))
    # ax = plt.subplot(111, projection='polar')
    # for sim_group in sim_groups:
    #     sim_group_dir = os.path.join(FARGO_DIR, sim_group)
    #     for sim_id in sorted(os.listdir(sim_group_dir)):
    #         if sim_id in ['.DS_Store']:
    #             continue
    #         nr_of_outputs = sim_params.general.nr_of_outputs(sim_group, sim_id)
    #         for outfile_idx in range(nr_of_outputs):
    #             plotting.gas_density.polar_2D(ax, sim_group, sim_id, outfile_idx)
    #             filename = f'{outfile_idx}.png'
    #             if outfile_idx < 100:
    #                 filename = f'0{filename}'
    #                 if outfile_idx < 10:
    #                     filename = f'0{filename}'
    #             save_loc = os.path.join(FIGURE_DIR, sim_group, sim_id, 'polar', filename)
    #             plt.savefig(save_loc)
    #             plt.cla()

#    plotting.various.flaring_disk()
    # plotting.hill_sphere.machida()

    # plotting.gas_density.sigma_vs_r_and_flaring_idx(50)
    # plotting.gap.polar2D()

#    plotting.gap.depth.vs_planet_ecc('frame_rotation')

#    sim_group = 'frame_rotation'
#    plotting.gas_density.sigma_vs_r_and_e(sim_group, 50)
#    plotting.gas_density.sigma_vs_r_and_e(sim_group, 10)

    # sim_group = 'frame_rotation'
    # plotting.gap.eccentricity.vs_planet_ecc(sim_group)
    # plotting.gap.eccentricity.vs_initial_mass(sim_group)
    # plotting.gap.polar2D()

    # plotting.migration.planet_ecc_vs_t_and_m0()
    # plotting.migration.planet_ecc_vs_t_and_visc()
    # for acc_is_on in [True, False]:
    #     plotting.migration.semimajor_axis_vs_t(acc_is_on)
    #     plotting.migration.planet_ecc_vs_t(acc_is_on)


    # main(sim_groups)
    #custom()

    def gap_profile_plots_vs_e():
        sim_group = 'frame_rotation'
        for outfile_idx in range(51):
            # plotting.gas_density.sigma_vs_r_and_m0(sim_group, outfile_idx)
            plotting.gas_density.sigma_vs_r_and_e(sim_group, outfile_idx)
            pass

        imgs_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_e')
        imgs = ' '.join([
            f'"{os.path.join(imgs_loc, i)}"' for i in sorted(os.listdir(imgs_loc))
        ])
        save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_evolution_vs_e.gif')
        # print(imgs)
        # input()
        os.system(f'convert {imgs} "{save_loc}"')

    def gap_profile_plots_vs_m():
        sim_group = 'frame_rotation'
        for outfile_idx in range(0):
            # plotting.gas_density.sigma_vs_r_and_m0(sim_group, outfile_idx)
            plotting.gas_density.sigma_vs_r_and_m0(sim_group, outfile_idx)
            pass

        if 'gap_depth_vs_m0' not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
            os.mkdir(os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_m0'))
        imgs_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_m0')
        imgs = ' '.join([
            f'"{os.path.join(imgs_loc, i)}"' for i in sorted([i for i in os.listdir(imgs_loc) if i not in ['.DS_Store']]) if int(i.split('.')[0]) <= 2500
        ])
        save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_evolution_vs_m0.gif')
        # print(imgs)
        # input()
        os.system(f'convert {imgs} "{save_loc}"')

    sim_group = 'frame_rotation'
    # plotting.gap.eccentricity.vs_planet_ecc(sim_group)
    # plotting.gap.eccentricity.vs_initial_mass(sim_group)
    # gap_profile_plots_vs_m()
    # gap_profile_plots_vs_e()
    # polar_plots('10000_orbits')
    # plotting.accretion.vs_time(sim_group)
    plotting.accretion.vs_e0_and_m0(sim_group, 50)
    # plotting.hill_sphere.kley()
    # plotting.gas_density.sigma_vs_r_and_m0(sim_group, 50)
    # create_polar_plot(sim_group, '1.0mj_e.000', 10)
    # for i in [True, False]:
    #     plotting.migration.planet_ecc_vs_t(i)
    # plotting.gas_density.sigma_vs_r_and_viscosity(50)
    #     plotting.migration.semimajor_axis_vs_t(i)
