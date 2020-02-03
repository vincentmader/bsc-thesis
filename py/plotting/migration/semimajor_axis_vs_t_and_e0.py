import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group, acc_is_on):
    if sim_group not in ['migration']:
        return
    print('  plotting migration.semimajor_axis_vs_t_and_e0')

    plt.figure(figsize=(4, 4))

    sim_ids = []
    sim_group_dir = os.path.join(FARGO_DIR, sim_group)
    for sim_id in sorted(os.listdir(sim_group_dir)):
        if sim_id in ['.DS_Store']:
            continue
        mass0 = sim_params.planets.initial_mass(sim_group, sim_id)
        alpha_visc = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
        acc_on = sim_id.split('_')[-1] == 'acc'
        if not (mass0 == 1e-3 and alpha_visc == 1e-2 and acc_on == acc_is_on):
            continue
        sim_ids.append(sim_id)

    for sim_id in sim_ids:
        ecc0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)

        semimajor_axes = [
            sim_params.planets.current_semimajor_axis(
                sim_group, sim_id, outfile_idx
            ) for outfile_idx in range(
                sim_params.general.nr_of_iterations(sim_group, sim_id)
            )
        ]

        plt.plot(semimajor_axes, label=ecc0)

    plt.legend()
    plt.xlabel('time in orbits')
    plt.ylabel('semimajor axis')
    plt.xlim(0, len(semimajor_axes))
    plt.ylim(0.5, 1)

    filename = 'semimajor_axis_vs_t_and_e0'
    if acc_is_on:
        filename += '_acc'
    save_loc = os.path.join(
        FIGURE_DIR, sim_group, f'{filename}.pdf'
    )
    plt.savefig(save_loc)


