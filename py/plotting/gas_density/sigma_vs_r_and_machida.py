
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis
import sim_params


def main(outfile_idx):
    """save a figure displaying the radial density for different resolutions

    Parameters
    ----------
    int outfile_idx: determines which files shall be loaded
    """

    sim_group = 'machida'

    fig = plt.figure(figsize=(8, 4))  # 10, 10))

    xs, ys = {}, {}
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        machida = sim_params.planets.machida(sim_group, sim_id)
        if machida % 0.5 != 0:
            continue

        out_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')
        λ_file = os.path.join(out_dir, f'gasdens.ascii_rad.{outfile_idx}.dat')
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[machida] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[machida] = [float(row.split(' ')[1]) for row in content]

    # define plot formats and colors
    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(xs))))

    # linear plot with different xlims
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    for idx, machida in enumerate(sorted(xs.keys())):
        x, y = xs[machida], ys[machida]
        plt.semilogy(
            x, y, label=f'Machida factor {machida}',
            color=colors[idx]
        )
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radially averaged gas density $\Sigma$ [code units]')
    plt.xlim(0.5, 2)
    # plt.ylim(0, 1.1 * max(y))
    plt.legend(loc='best')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_machida.pdf')
    plt.savefig(save_loc)
    plt.cla()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        outfile_idx = sys.argv[1]
    else:
        outfile_idx = 10

    main(outfile_idx)

