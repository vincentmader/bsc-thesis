
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import plotting
import setup
import sim_params


def sigma_vs_r_and_e(sim_group, out_file_idx):

    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    sim_ids = [
        f for f in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group)))
        if f != '.DS_Store' and 'unp' not in f
        and sim_params.planets.initial_mass(sim_group, f) == 1e-3
        and sim_params.planets.initial_eccentricity(sim_group, f) < 0.25
        # and (sim_params.planets.initial_mass(sim_group, f) - 1e-3) / 1e-3 < 1e-5
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
    colors = mpl.pylab.cm.jet(np.linspace(0.1, 0.9, len(sim_ids)))
    for idx, sim_id in enumerate(sim_ids):
        # only files with e=0
        initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        #print(initial_eccentricity, initial_eccentricity % 0.05)
        if initial_eccentricity not in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
            continue

        label = f'$e={initial_eccentricity:.2f}$'
        # plot
        plotting.gas_density.logarithmic_1D(
            ax, sim_group, sim_id, out_file_idx, label=label, color=colors[idx]
        )

        r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
        r_max = 3  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

    # plt.xlabel(r'radial distance $r$ [code units]')
    plt.xlabel(r'distance from disk center $r$', size=16)
    plt.xticks(np.arange(0.5, r_max + 1, 0.5), size=12)
    plt.ylabel('azimuthally averaged surface density $\Sigma$ [code units]')
    plt.xlim(0.2, r_max - 0.3)
    if sim_group == 'frame_rotation':
        plt.ylabel('surface density $\Sigma/\Sigma_{unp}$', size=16)
        # plt.ylim(5e-6, 1e-3)
        plt.ylim(1e-2, 2)
        plt.yticks([1e-2, 1e-1, 1], size=12)
        # plt.gcf().subplots_adjust(left=0.2)
    #plt.title('radial gas density after mass taper for planet with $m_0=1\ M_{jupiter}$')
    plt.legend(loc='lower right', fontsize=14)

    orbits = out_file_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    plt.title(f'{"$t=$"}{orbits} orbits', size=16)

    def foo(num):
        string = str(num)
        if num < 1000:
            string = f'0{string}'
        if num < 100:
            string = f'0{string}'
        return string

    save_loc = os.path.join(
        FIGURE_DIR, sim_group, 'gap_depth_vs_e',
        f'sigma_vs_r_and_e0_{foo(orbits)}.png'
    )
    plt.savefig(save_loc)
    # save_loc = os.path.join(
    #     FIGURE_DIR, sim_group, 'gap_depth_vs_e',
    #     f'sigma_vs_r_and_e0_{foo(orbits + 25)}.png'
    # )
    # plt.savefig(save_loc)
    plt.close()


def main(sim_group, out_file_idx):

    print('  plotting gas_density.sigma_vs_r_and_e')

    if sim_group not in ['frame_rotation', '10000_orbits', '50000_orbits']:
        return
    sigma_vs_r_and_e(sim_group, out_file_idx)


if __name__ == '__main__':
    sim_group, out_file_idx = sys.argv[1], sys.argv[2]
    main(sim_group, out_file_idx)

