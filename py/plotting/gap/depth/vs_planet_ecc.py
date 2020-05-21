import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import setup
import sim_params


def plot(sim_group, outfile_idx):

    plt.figure(figsize=(4, 4))

    eccs, depths = [], []
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store'] or 'unp' in sim_id:
            continue

        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        mass = sim_params.planets.initial_mass(sim_group, sim_id)

        if mass != 1e-3 or ecc >= 0.2:
            continue

        content = setup.load_gas_density.sigma_1D_ascii(sim_group, sim_id, outfile_idx)
        rs = np.array([float(i.split(' ')[0]) for i in content])
        Σs = np.array([float(i.split(' ')[1]) for i in content])

        planet_idx = np.argmin(abs(rs - 1))
        depth = Σs[planet_idx]

        if sim_group in ['frame_rotation']:
            depth /= setup.sigma_unp(sim_group, sim_id, outfile_idx)[planet_idx]

        eccs.append(ecc)
        depths.append(depth)

    plt.scatter(eccs, depths)
    plt.xlim(-0.025, max(eccs) + 0.025)
    if outfile_idx == 10:
        plt.ylim(0, 1e-4)
    elif outfile_idx == 50:
        plt.ylim(0, 0.25e-4)
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    plt.xlabel('eccentricity of planet orbit')
    plt.ylabel('azimuthally averaged gas density at $r=1$')
    if sim_group in ['frame_rotation']:
        plt.ylabel('$\Sigma/\Sigma_{unp}$')
        if outfile_idx == 10:
            plt.ylim(0, 0.4)
        elif outfile_idx == 50:
            plt.ylim(0, 0.1)
    plt.gcf().subplots_adjust(left=.15)

    save_loc = os.path.join(
        FIGURE_DIR, sim_group, f'gap_depth_vs_e0_{outfile_idx}.pdf'
    )
    plt.savefig(save_loc)


def main(sim_group):
    for outfile_idx in [10, 50]:
        plot(sim_group, outfile_idx)
