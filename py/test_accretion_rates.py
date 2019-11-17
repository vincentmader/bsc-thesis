
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

iteration_step = int(sys.argv[1])


def create_plot_for_1MJ(iteration_step):

    planet_masses, eccentricities = [], []

    for i in os.listdir('../fargo2d1d/testing_masses'):
        if not i.startswith('1mj'):
            continue
        if not i.endswith('b'):
            continue
        planet_file = f'../fargo2d1d/testing_masses/{i}/out/planet1.dat'
        with open(planet_file) as fp:
            content = fp.readlines()
        try:
            m = content[iteration_step].split('\t')[5]
        except IndexError:
            continue
        e = float(i.split('e')[-1])

        planet_masses.append(m)
        eccentricities.append(e)

    plt.scatter(eccentricities, planet_masses)
    plt.savefig('test_accretion_rates.png')


if __name__ == '__main__':
    create_plot_for_1MJ(iteration_step)
