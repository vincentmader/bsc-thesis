import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(acc_is_on=True):

    sim_group = 'migration'
    print(f'  plotting.migration.planet_ecc_vs_t(acc={acc_is_on})')
    for vs in ['e0', 'm0', 'visc']:

        fig, ax = plt.subplots(figsize=(4, 4))

        sim_ids = []
        sim_group_dir = os.path.join(FARGO_DIR, sim_group)
        for sim_id in os.listdir(sim_group_dir):
            if sim_id in ['.DS_Store', 'unp']:
                continue

            e0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
            if e0 != 0.2 and vs != 'e0':
                continue
            m0 = sim_params.planets.initial_mass(sim_group, sim_id)
            if m0 != 1e-3 and vs != 'm0':
                continue
            visc = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
            if visc != 1e-2 and vs != 'visc':
                continue
            # print(False == sim_id.split('_')[-1] == 'acc')
            if acc_is_on != ('acc' == sim_id.split('_')[-1]):
                continue
            sim_ids.append(sim_id)

        colors = list(pl.cm.jet(np.linspace(0.3, 0.9, len(sim_ids))))

        # print(vs, sim_ids)
        for idx, sim_id in enumerate(sorted(sim_ids)):

            e0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
            m0 = sim_params.planets.initial_mass(sim_group, sim_id)
            visc = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)

            # load file containing info about orbit
            orbit_file = os.path.join(
                FARGO_DIR, sim_group, sim_id, 'out', 'orbit1.dat'
            )
            with open(orbit_file) as fp:
                orbit = fp.readlines()

            # time parameter in orbits
            t = np.arange(0, len(orbit), 1)
            # eccentricity at time t
            ecc = [float(row.split('\t')[1]) for row in orbit]
            # print(ecc)

            if vs == 'e0':
                label = '$e_0=' + str(e0) + '$'
            if vs == 'm0':
                label = '$m_0=' + str(m0) + '$'
            if vs == 'visc':
                label = '$\\alpha_v=' + str(visc) + '$'

            # plot
            plt.plot(
                t, ecc, label=label, color=colors[idx]
            )
            plt.legend()
            plt.xlim(0, len(t))
            plt.yticks([0, 0.05, 0.1, 0.15, 0.2])
            plt.xlabel('time $t$ [orbits]')
            plt.ylabel('eccentricity $e$')
            # plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
            plt.gcf().subplots_adjust(left=.15)

        # save
        filename = f'ecc_vs_t_and_{vs}'
        if acc_is_on:
            filename += '_acc'
        save_loc = os.path.join(FIGURE_DIR, sim_group, f'{filename}.pdf')
        plt.savefig(save_loc)
        plt.close()
