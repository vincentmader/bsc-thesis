
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis
import sim_params


def main(outfile_idx):

    sim_group = 'aspect_ratio'

    fig = plt.figure(figsize=(4, 4))  # 10, 10))

    xs, ys = {}, {}
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id in ['.DS_Store']:
            continue

        hr = sim_params.general.aspect_ratio(sim_group, sim_id)
        if hr > 0.1:
            continue
        if hr not in np.array(range(1, 11)) / 100:
            continue

        out_dir = os.path.join(FARGO_DIR, sim_group, sim_id, 'out')
        λ_file = os.path.join(out_dir, f'gasdens.ascii_rad.{outfile_idx}.dat')
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[hr] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[hr] = [float(row.split(' ')[1]) for row in content]

    # define plot formats and colors
    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(xs))))

    # linear plot with different xlims
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    for idx, hr in enumerate(sorted(xs.keys())):
        x, y = xs[hr], ys[hr]
        hr_tex = r'$H/R$'
        plt.semilogy(
            x, y, label=f'{hr_tex}={hr}',
            color=colors[idx]
        )
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel('azimuthally averaged surface density $\Sigma$ [code units]')
    plt.gcf().subplots_adjust(left=.2)
    plt.xlim(0.05, 2)
    # plt.ylim(0, 1.1 * max(y))
    plt.legend(loc='lower right')

    save_loc = os.path.join(FIGURE_DIR, sim_group, 'sigma_vs_r_and_hr.pdf')
    plt.savefig(save_loc)
    plt.cla()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        outfile_idx = sys.argv[1]
    else:
        outfile_idx = 10

    main(outfile_idx)


