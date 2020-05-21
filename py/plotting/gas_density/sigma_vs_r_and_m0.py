

import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

import analysis
import config
from config import FARGO_DIR, FIGURE_DIR
import plotting
import setup
import sim_params


def sigma_vs_r_and_m0(sim_group, out_file_idx):

    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    sim_ids = [
        f for f in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group)))
        if f != '.DS_Store' and 'unp' not in f
        and sim_params.planets.initial_eccentricity(sim_group, f) == 0
        # TODO: generalize for different masses
    ]
    if not sim_ids:
        plt.close()
        return
    # initial_eccentricities = [
    #     sim_params.planets.initial_eccentricity(sim_group, s) for s in sim_ids
    # ]
    # print(sim_group, initial_eccentricities)
    # colors = pl.cm.jet(initial_eccentricities)
    colors = pl.cm.jet(np.linspace(0.1, 0.9, len(sim_ids)))

    for idx, sim_id in enumerate(sorted(sim_ids)):
        # only files with e=0
        initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if initial_eccentricity != 0:
            continue

        m_jupiter = r'm_{jupiter}'
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, out_file_idx)
        label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$, $m(t)={(current_mass * 1e3):.1f}\ {m_jupiter}$'
        label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$, $m/m_0={(current_mass / initial_mass):.2f}$'
        label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$'
        # plot
        plotting.gas_density.logarithmic_1D(
            ax, sim_group, sim_id, out_file_idx, label=label, color=colors[idx]
        )

        r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
        r_max = 3  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

    plt.xlabel(r'distance from disk center $r$', size=16)
    plt.xticks(np.arange(0, r_max + 1, 0.5), fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel('surface density $\Sigma/\Sigma_{unp}$', fontsize=15)
    if sim_group in ['frame_rotation']:
        plt.ylim(10**(-3), 2.5)
    plt.xlim(0.2, r_max -0.3)
    #plt.title('radial gas density after mass taper for planet with $e=0$')
    plt.legend(loc='lower right', fontsize=14)
    # save
    orbits = out_file_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    plt.title(f'{"$t=$"}{orbits} orbits', size=16)
    filename = str(orbits)
    if orbits < 1000:
        filename = f'0{filename}'
        if orbits < 100:
            filename = f'0{filename}'
            if orbits < 10:
                filename = f'0{filename}'
    plt.title(f'{"$t=$"}{orbits} orbits')
    save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_m0', f'{filename}.png')
    plt.savefig(save_loc)

    if out_file_idx == 50:
        sim_ids = [
            '0.5mj_e.000', '1.0mj_e.000', '1.5mj_e.000', '2.0mj_e.000',
            '2.5mj_e.000', '3.0mj_e.000', '3.5mj_e.000', '4.0mj_e.000',
            '4.5mj_e.000', '5.0mj_e.000'
        ]
            # f for f in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group)))
            # if f not in ['unp', '.DS_Store']
            # and sim_params.planets.initial_mass(sim_group, f) in np.arange(0.5, 5.5, 0.5) * 1e-3
            # and sim_params.planets.initial_eccentricity(sim_group, f) == 0
        # ]
        masses = [
            sim_params.planets.current_mass(sim_group, s, out_file_idx) for s in sim_ids
        ]
        hill_sphere_starts = [
            1 - analysis.hill_radius(m=m) for m in masses
        ]
        hill_sphere_stops = [
            1 + analysis.hill_radius(m=m) for m in masses
        ]
        # print(hill_sphere_starts)
        # def grid_idx(sim_id_idx):
        #     sim_id = sim_ids[idx]
        #     r_min= sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
        #     r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)
        #     N_rad, N_sec = sim_params.resolution.get_2D_res(sim_group, sim_id)
        #     foo = [(x - r_min) / (r_max - r_min) * N_sec  for x in hill_sphere_starts]
        #     return int(foo[sim_id_idx])

        # gap_depths = [
        #     np.average(setup.load_gas_density.sigma_2D(
        #         sim_group, sim_id, out_file_idx
        #     )[grid_idx(idx)]) for idx, _ in enumerate(sim_ids)
        # ]
        # plt.gcf()
        # print(gap_depths)

        gap_depths = [6e-2, 4e-2, 2.5e-2, 1.5e-2, 9e-3, 6e-3, 4e-3, 1.7e-3, 2e-3, 1.3e-3]

        plt.plot(hill_sphere_starts, gap_depths, 'k--')
        plt.plot(hill_sphere_stops, gap_depths, 'k--')

        save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_m0', f'{orbits + 25}.png')
        plt.savefig(save_loc)

        plt.clf()
        for idx, sim_id in enumerate(sorted(sim_ids)):
            # only files with e=0
            initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
            initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
            if initial_eccentricity != 0:
                continue

            m_jupiter = r'm_{jupiter}'
            initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
            current_mass = sim_params.planets.current_mass(sim_group, sim_id, out_file_idx)
            label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$, $m(t)={(current_mass * 1e3):.1f}\ {m_jupiter}$'
            label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$, $m/m_0={(current_mass / initial_mass):.2f}$'
            label = f'$m_0={(initial_mass * 1e3):.1f}\ {m_jupiter}$'
            # plot
            plotting.gas_density.logarithmic_1D(
                ax, sim_group, sim_id, out_file_idx, label=label, color=colors[idx]
            )

            r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
            r_max = 3  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

        plt.xlabel(r'distance from disk center $r$', size=16)
        plt.xticks(np.arange(0, r_max + 1, 0.5), fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylabel('surface density $\Sigma/\Sigma_{unp}$', fontsize=15)
        if sim_group in ['frame_rotation']:
            plt.ylim(10**(-3), 2.5)
        plt.xlim(0.2, r_max -0.3)
        #plt.title('radial gas density after mass taper for planet with $e=0$')
        plt.legend(loc='lower right', fontsize=14)
        # save
        orbits = out_file_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
        plt.title(f'{"$t=$"}{orbits} orbits', size=16)
        plt.title(f'{"$t=$"}{orbits} orbits')
        filename = str(orbits + 10)
        save_loc = os.path.join(FIGURE_DIR, sim_group, 'gap_depth_vs_m0', f'{orbits + 30}.png')
        plt.savefig(save_loc)

    plt.close()


def main(sim_group, out_file_idx):

    print('  plotting gas_density.sigma_vs_r_and_m0')

    if sim_group not in ['frame_rotation', '10000_orbits', '50000_orbits']:
        return
    sigma_vs_r_and_m0(sim_group, out_file_idx)


if __name__ == '__main__':
    sim_group, out_file_idx = sys.argv[1], sys.argv[2]
    main(sim_group, out_file_idx)

