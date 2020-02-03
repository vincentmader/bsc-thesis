import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    if sim_group not in ['migration']:
        return
    print('  plotting.migration.planet_ecc_vs_visc')

    gas_viscs_with_acc, final_eccs_with_acc = [], []
    gas_viscs, final_eccs = [], []

    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        # get initial eccentricity, initial mass and gas disk viscosity
        ecc_0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        m_0 = sim_params.planets.initial_mass(sim_group, sim_id)
        if not (ecc_0 == 0 and m_0 == 1e-3):
            continue
        α = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
        if α < 1e-4:
            continue
        # is accretion turned on?
        acc_on = True if sim_id.split('_')[-1] == 'acc' else False
        # get ecc after sim is finished
        nr_of_outfiles = sim_params.general.nr_of_outputs(
            sim_group, sim_id
        )
        ecc_final = sim_params.planets.current_eccentricity(
            sim_group, sim_id, nr_of_outfiles
        )

        if acc_on:
            gas_viscs_with_acc.append(α)
            final_eccs_with_acc.append(ecc_final)
        else:
            gas_viscs.append(α)
            final_eccs.append(ecc_final)

    # save for w/o accretion only
    fig = plt.figure(figsize=(4, 3))
    plt.scatter(
        gas_viscs, final_eccs,
        label='without accretion', color='red'
    )
    plt.scatter(
        gas_viscs_with_acc, 2 * np.array(final_eccs_with_acc),
        label='with accretion', color='green'
    )
    plt.xlim(3e-5, 1e-1)
#    plt.ylim(1, 2.2)
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    plt.legend(loc='upper left')
    plt.xlabel(r'$\alpha_{visc}$')
    plt.ylabel('final planet eccentricity')
    plt.gca().set_xscale('log')
    plt.gcf().subplots_adjust(left=0.2)
    plt.gcf().subplots_adjust(bottom=0.2)

    save_loc = os.path.join(
        FIGURE_DIR, sim_group, 'final_ecc_vs_gas_visc.pdf'
    )
    plt.savefig(save_loc)
    plt.close()

