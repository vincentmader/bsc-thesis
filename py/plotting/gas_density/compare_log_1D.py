
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import plotting
import setup
import sim_params


def sigma_vs_t_and_e(sim_group, out_file_idx):

    plt.figure(figsize=(8, 4))
    ax = plt.gca()

    sim_ids = [
        f for f in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group)))
        if f != '.DS_Store'
        and sim_params.planets.initial_mass(sim_group, f) == 1e-3
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
    colors = pl.cm.jet(np.linspace(0.1, 0.9, len(sim_ids)))
    for idx, sim_id in enumerate(sim_ids):
        # only files with e=0
        initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)

        label = f'$e_0={initial_eccentricity:.2f}$'
        # plot
        plotting.gas_density.logarithmic_1D(
            ax, sim_group, sim_id, out_file_idx, label=label, color=colors[idx]
        )

        r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
        r_max = 3  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

    plt.xlabel(r'radial distance $r$ [code units]')
    plt.xticks(np.arange(0, r_max + 1, 1))
    plt.ylabel(r'surface density $\Sigma$ [code units]')
    plt.xlim(r_min + 0.1, r_max)
    plt.legend(loc='upper right')
    plt.title('radial gas density after mass taper for planet with $m_0=1\ M_{jupiter}$')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_e0.pdf')
    plt.savefig(save_loc)
    plt.close()


def sigma_vs_t_and_m0(sim_group, out_file_idx):

    plt.figure(figsize=(8, 4))
    ax = plt.gca()

    sim_ids = [
        f for f in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group)))
        if f != '.DS_Store'
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

    for idx, sim_id in enumerate(sim_ids):
        # only files with e=0
        initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if initial_eccentricity != 0:
            continue

        label = f'$m_0={initial_mass:.3f}$'
        # plot
        plotting.gas_density.logarithmic_1D(
            ax, sim_group, sim_id, out_file_idx, label=label, color=colors[idx]
        )

        r_min = sim_params.radial_boundaries.r_min_1D(sim_group, sim_id)
        r_max = 3  # sim_params.radial_boundaries.r_max_1D(sim_group, sim_id)

    plt.xlabel(r'radial distance $r$ [code units]')
    plt.xticks(np.arange(0, r_max + 1, 1))
    plt.ylabel('surface density $\Sigma$ [code units]')
    plt.xlim(r_min + 0.1, r_max)
    plt.legend(loc='upper right')
    plt.title('radial gas density after mass taper for planet with $e=0$')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_m0.pdf')
    plt.savefig(save_loc)
    plt.close()


def main(sim_group, out_file_idx):
    if sim_group in ['testing_cells_per_rH', 'testing_visc']:
        return
    sigma_vs_t_and_e(sim_group, out_file_idx)
    sigma_vs_t_and_m0(sim_group, out_file_idx)


if __name__ == '__main__':
    sim_group, out_file_idx = sys.argv[1], sys.argv[2]
    main(sim_group, out_file_idx)

