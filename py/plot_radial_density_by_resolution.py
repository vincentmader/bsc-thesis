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

    for simulation_dir in os.listdir('../fargo2d1d/testing_cells_per_rH/'):
        eccentricity = float(simulation_dir.split('e')[-1])
        if eccentricity != 0:
            continue
        cells_per_rH = float(simulation_dir.split('c')[0])

        out_dir = f'../fargo2d1d/testing_cells_per_rH/{simulation_dir}/out/'
        λ_file = out_dir + f'gasdens.ascii_rad.{iteration_step}.dat'
        try:
            with open(λ_file) as fp:
                content = fp.readlines()
        except FileNotFoundError:
            continue

        x = np.array([float(row.split(' ')[0]) for row in content]) #/ len(content) #* cells_per_rH * rH
        y = [float(row.split(' ')[1]) for row in content]

        # linear plot
        plt.subplot(311)
        plt.title(r'radial densities for different resolutions')
        plt.plot(x, y, label=f'{cells_per_rH} cells per Hill radius')
        plt.xlabel(r'radial distance $r$ [code units]')
        plt.ylabel(r'radial density $\lambda$ [code units]')
        plt.xlim(0.03, 50)
        plt.legend(loc='upper right')
        # linear plot with different xlims
        plt.subplot(312)
        plt.plot(x, y, label=f'{cells_per_rH} cells per Hill radius')
        plt.xlabel(r'radial distance $r$ [code units]')
        plt.ylabel(r'radial density $\lambda$ [code units]')
        plt.xlim(0.03, 2)
        plt.legend(loc='upper right')
        # semilogx plot
        plt.subplot(313)
        plt.semilogx(x, y, label=f'{cells_per_rH} cells per Hill radius')
        plt.xlabel(r'logarithmic radial distance $log(r)$ [code units]')
        plt.ylabel(r'radial density $\lambda$ [code units]')
        plt.xlim(0.03, 50)
        plt.legend(loc='upper right')

    plt.savefig('radial_densities_by_resolution.pdf')
    plt.clf()


if __name__ == '__main__':

    iteration_step = sys.argv[1]

    main(iteration_step)

