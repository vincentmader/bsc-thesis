
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from plot_collage import get_total_nr_of_steps, get_nr_of_orbits_between_outputs
from plot_collage import get_initial_planet_mass


SIMULATION_DIR = sys.argv[1]


def create_plot_for_rel_mass_vs_t(simulation_id, color):

    with open(f'../fargo2d1d/{SIMULATION_DIR}/{simulation_id}/out/planet1.dat') as fp:
        content = fp.readlines()

    initial_planet_mass = get_initial_planet_mass(SIMULATION_DIR, simulation_id)
    nr_of_orbits_between_outputs = get_nr_of_orbits_between_outputs(SIMULATION_DIR)
    total_nr_of_steps = get_total_nr_of_steps(SIMULATION_DIR, simulation_id)
    total_nr_of_orbits = total_nr_of_steps * nr_of_orbits_between_outputs
    eccentricity = float(simulation_id.split('e')[1])

    plt.xlim(0, total_nr_of_orbits)

    mass = [float(row.split('\t')[5]) for row in content]
    t = np.linspace(0, total_nr_of_orbits, len(mass))

    plt.plot(t, mass / initial_planet_mass,
        label=f'{r"e="}{eccentricity:.2f}', color=color
    )


def create_plot_for_acc_rate_vs_t(simulation_id, color):
    """
    create plot for accretion rate vs time

    Parameters:
    -----------
    x: type
    Description

    Returns:
    --------
    y: type
    Description

    """

    with open(f'../fargo2d1d/{SIMULATION_DIR}/{simulation_id}/out/planet1.dat') as fp:
        content = fp.readlines()

    initial_planet_mass = get_initial_planet_mass(SIMULATION_DIR, simulation_id)
    nr_of_orbits_between_outputs = get_nr_of_orbits_between_outputs(SIMULATION_DIR)
    total_nr_of_steps = get_total_nr_of_steps(SIMULATION_DIR, simulation_id)
    total_nr_of_orbits = total_nr_of_steps * nr_of_orbits_between_outputs
    eccentricity = float(simulation_id.split('e')[1])

    plt.xlim(0, total_nr_of_orbits)

    mass = [float(row.split('\t')[5]) for row in content]
    t = np.linspace(0, total_nr_of_orbits, len(mass))
    acc_rate = np.diff(mass) / np.diff(t)

    plt.plot(t[1:], acc_rate, label=f'{r"e="}{eccentricity:.2f}', color=color)


if __name__ == '__main__':
    # check if figures folder exists
    if SIMULATION_DIR not in os.listdir('../figures/'):
        os.mkdir(f'../figures/{SIMULATION_DIR}')

    # create individual plots
    for simulation_id in os.listdir(f'../fargo2d1d/{SIMULATION_DIR}'):
        if simulation_id in ['.DS_Store']:
            continue

        # check if figures folder exists
        if simulation_id not in os.listdir(f'../figures/{SIMULATION_DIR}/'):
            os.mkdir(f'../figures/{SIMULATION_DIR}/{simulation_id}')

        # plots for relative mass increase m/m0
        plt.figure(figsize=(8, 4))
        plt.xlabel('number of orbits since simulation start')
        plt.ylabel(r'relative mass increase $m/m_0$')

        create_plot_for_rel_mass_vs_t(simulation_id, color='black')

        plt.savefig(f'../figures/{SIMULATION_DIR}/{simulation_id}/rel_mass_increase_vs_t.pdf')

        # plots for accretion rate (m_i - m_j, i=j+1)
        plt.figure(figsize=(8, 4))
        plt.xlabel('number of orbits since simulation start')
        plt.ylabel(r'relative mass increase $m/m_0$')

        create_plot_for_acc_rate_vs_t(simulation_id, color='black')

        plt.savefig(f'../figures/{SIMULATION_DIR}/{simulation_id}/acc_rate_vs_t.pdf')


    # one plot showing results for different eccentricities

    # plot for relative mass increase m/m0
    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'relative mass increase $m/m_0$')
    plt.title(r'relative mass increase for planets with $m_0=1M_{jupiter}$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0,0), axis='y')

    colors = ['blue', 'green', 'orange', 'red', 'black']
    for idx, simulation_id in enumerate([
        i for i in reversed(sorted(
            os.listdir(f'../fargo2d1d/{SIMULATION_DIR}'))
        ) if i != '.DS_Store' and i.startswith('1')]
    ):
        create_plot_for_rel_mass_vs_t(simulation_id, color=colors[idx])

    plt.legend(loc='upper left')
    plt.savefig(f'../figures/{SIMULATION_DIR}/rel_mass_increase_vs_t.pdf')

    # plot for accretion rate (m_i - m_j, i=j+1)
    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'mass accretion rate $\dot m$')
    plt.title(r'accretion rate for planets with $m_0=1M_{jupiter}$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0,0), axis='y')
    plt.ylim(0, 3e-6)

    colors = ['blue', 'green', 'orange', 'red', 'black']
    for idx, simulation_id in enumerate([
        i for i in reversed(sorted(
            os.listdir(f'../fargo2d1d/{SIMULATION_DIR}'))
        ) if i != '.DS_Store' and i.startswith('1')]
    ):
        create_plot_for_acc_rate_vs_t(simulation_id, color=colors[idx])

    plt.legend(loc='upper right')
    plt.savefig(f'../figures/{SIMULATION_DIR}/acc_rate_vs_t.pdf')

