
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis
import sim_params


def main(outfile_idx):

    sim_group = 'sigma_slope'

#    print('plotting gas_density.sigma_vs_r_and_flaring_idx')

    fig = plt.figure(figsize=(4, 4))  # 10, 10))

    xs, ys = {}, {}
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        slope = sim_params.general.sigma_slope(sim_group, sim_id)

        out_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')
        λ_file = os.path.join(out_dir, f'gasdens.ascii_rad.{outfile_idx}.dat')
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[slope] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[slope] = [float(row.split(' ')[1]) for row in content]

    # define plot formats and colors
    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(xs))))

    # linear plot with different xlims
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    for idx, slope in enumerate(sorted(xs.keys())):
        x, y = xs[slope], ys[slope]
        plt.semilogy(
            x, y, label=f'sigma slope {slope}',
            color=colors[idx]
        )
    nr_of_orbits = outfile_idx * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    #plt.title(f'gas density for various flaring indices (after {nr_of_orbits} orbits) ')
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel('azimuthally averaged surface density $\Sigma$ [code units]')
    plt.xlim(0.5, 2)
    # plt.ylim(0, 1.1 * max(y))
    plt.legend(loc='best')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_sigma_slope.pdf')
    plt.savefig(save_loc)
    plt.cla()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        iteration_step = sys.argv[1]
    else:
        iteration_step = 10

    main(iteration_step)

