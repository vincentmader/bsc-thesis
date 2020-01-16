
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis
import sim_params


def main(outfile_idx):

    sim_group = 'testing_visc'

    fig = plt.figure(figsize=(8, 4))  # 10, 10))

    xs, ys = {}, {}
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        viscosity = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)

        out_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')
        λ_file = os.path.join(out_dir, f'gasdens.ascii_rad.{outfile_idx}.dat')
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[viscosity] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[viscosity] = [float(row.split(' ')[1]) for row in content]

    # define plot formats and colors
    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(xs))))

    # linear plot with different xlims
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    for idx, viscosity in enumerate(sorted(xs.keys())):
        x, y = xs[viscosity], ys[viscosity]
        alpha_v = r'$\alpha_v$'
        plt.semilogy(
            x, y, label=f'{alpha_v}={viscosity:.0E}',
            color=colors[idx]
        )
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radially averaged gas density $\Sigma$ [code units]')
    plt.xlim(0.5, 2)
    # plt.ylim(0, 1.1 * max(y))
    plt.legend(loc='best')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_viscosity.pdf')
    plt.savefig(save_loc)
    plt.cla()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        outfile_idx = sys.argv[1]
    else:
        outfile_idx = 10

    main(outfile_idx)


