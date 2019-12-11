#!/usr/local/bin/python3
# -*- coding: utf8 -*-

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from get_hill_radius import main as get_hill_radius


def main(iteration_step):
    """save a figure displaying the radial density for different resolutions

    Parameters
    ----------
    int iteration_step: determines which files shall be loaded
    """

    rH = get_hill_radius(M=1, m=1e-3, a=1, e=0)

    fig = plt.figure(figsize=(10, 10))

    xs, ys = {}, {}

    for simulation_id in os.listdir('../fargo2d1d/testing_cells_per_rH/'):
        eccentricity = float(simulation_id.split('e')[-1])
        if eccentricity != 0:
            continue
        cells_per_rH = float(simulation_id.split('c')[0])
        if cells_per_rH == 7.5:
            continue

        out_dir = f'../fargo2d1d/testing_cells_per_rH/{simulation_id}/out/'
        λ_file = out_dir + f'gasdens.ascii_rad.{iteration_step}.dat'
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        xs[cells_per_rH] = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        ys[cells_per_rH] = [float(row.split(' ')[1]) for row in content]

    # define plot formats
    fmts = {2.5: 'k-', 5: 'k--', 10: 'k-.'}
    fmts = {2.5: '-', 5: '-', 10: '-'}
    # linear plot
    plt.subplot(311)
    plt.title(r'radial densities after 500 orbits for different resolutions')
    for cells_per_rH in sorted(xs.keys()):
        x, y = xs[cells_per_rH], ys[cells_per_rH]
        fmt = fmts[cells_per_rH]
        plt.plot(x, y, fmt, label=f'{cells_per_rH} cells per Hill radius')
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radial density $\lambda$ [code units]')
    plt.xlim(0.03, 50)
    plt.legend(loc='upper right')
    # linear plot with different xlims
    plt.subplot(312)
    for cells_per_rH in sorted(xs.keys()):
        fmt = fmts[cells_per_rH]
        x, y = xs[cells_per_rH], ys[cells_per_rH]
        plt.plot(x, y, fmt, label=f'{cells_per_rH} cells per Hill radius')
    plt.xlabel(r'radial distance $r$ [code units]')
    plt.ylabel(r'radial density $\lambda$ [code units]')
    plt.xlim(0.03, 2)
    plt.legend(loc='upper right')
    # semilogx plot
    plt.subplot(313)
    for cells_per_rH in sorted(xs.keys()):
        fmt = fmts[cells_per_rH]
        x, y = xs[cells_per_rH], ys[cells_per_rH]
        plt.semilogx(x, y, fmt, label=f'{cells_per_rH} cells per Hill radius')
    plt.xlabel(r'logarithmic radial distance $log(r)$ [code units]')
    plt.ylabel(r'radial density $\lambda$ [code units]')
    plt.xlim(0.03, 50)
    plt.legend(loc='upper right')

    plt.savefig(
        '../figures/testing_cells_per_rH/radial_densities_by_resolution.pdf'
    )
    plt.cla()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        iteration_step = sys.argv[1]
    else:
        iteration_step = 10

    main(iteration_step)

