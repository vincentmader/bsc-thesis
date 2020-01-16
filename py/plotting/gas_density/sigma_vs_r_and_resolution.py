
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis
import sim_params


def main(iteration_step):
    """save a figure displaying the radial density for different resolutions

    Parameters
    ----------
    int iteration_step: determines which files shall be loaded
    """

    sim_group = 'testing_cells_per_rH'

    rH = analysis.accretion.hill_radius(M=1, m=1e-3, a=1, e=0)
    xs, ys = {}, {}

    for sim_id in os.listdir(os.path.join(FARGO_DIR, 'testing_cells_per_rH')):
        if sim_id in ['.DS_Store']:
            continue
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)  #float(sim_id.split('e')[-1])
        if ecc != 0:
            continue
        cells_per_rH = float(sim_id.split('c')[0])
        if cells_per_rH == 7.5:
            continue

        out_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')
        λ_file = os.path.join(out_dir, f'gasdens.ascii_rad.{iteration_step}.dat')
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[cells_per_rH] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[cells_per_rH] = [float(row.split(' ')[1]) for row in content]

    # define plot formats and colors
    fmts = {2.5: 'k-', 5: 'k--', 10: 'k-.'}
    fmts = {2.5: '-', 5: '-', 10: '-'}
    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(xs))))

    # linear plot
    fig = plt.figure(figsize=(8, 4))
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    #plt.title(r'radial densities after 500 orbits for different resolutions')
    for idx, cells_per_rH in enumerate(sorted(xs.keys())):
        x, y = xs[cells_per_rH], ys[cells_per_rH]
        fmt = fmts[cells_per_rH]
        plt.plot(
            x, y, fmt, label=f'{cells_per_rH} cells per Hill radius',
            color=colors[idx]
        )
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radially averaged gas density $\Sigma$ [code units]')
    plt.xlim(0, 50)
    plt.ylim(0, 1.2e-3)
    plt.legend(loc='upper right')
    plt.grid(True)
    save_loc = os.path.join(FIGURE_DIR, sim_group, 'radial_densities_by_resolution.pdf')
    plt.savefig(save_loc)
    plt.close()

    # linear plot with different xlims
    fig = plt.figure(figsize=(8, 4))
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    for idx, cells_per_rH in enumerate(sorted(xs.keys())):
        fmt = fmts[cells_per_rH]
        x, y = xs[cells_per_rH], ys[cells_per_rH]
        plt.plot(
            x, y, fmt, label=f'{cells_per_rH} cells per Hill radius',
            color=colors[idx]
        )
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radially averaged gas density $\Sigma$ [code units]')
    plt.xlim(0, 2)
    plt.ylim(0, 1.2e-3)
    plt.grid(True)
    plt.legend(loc='upper right')
#    # semilogx plot
#    plt.subplot(313)
#    for idx, cells_per_rH in enumerate(sorted(xs.keys())):
#        fmt = fmts[cells_per_rH]
#        x, y = xs[cells_per_rH], ys[cells_per_rH]
#        plt.semilogx(
#            x, y, fmt, label=f'{cells_per_rH} cells per Hill radius',
#            color=colors[idx]
#        )
#    plt.xlabel(r'logarithmic radial distance $log(r)$ [code units]')
#    plt.ylabel(r'radial density $\lambda$ [code units]')
#    plt.xlim(0.03, 50)
#    plt.legend(loc='upper right)

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'radial_densities_by_resolution_zoom.pdf')
    plt.savefig(save_loc)
    plt.close()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        iteration_step = sys.argv[1]
    else:
        iteration_step = 10

    main(iteration_step)

