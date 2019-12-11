
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from plot_collage import get_nr_of_orbits_between_outputs


def create_plot_for_1MJ(iteration_step):

    # get eccentricity and corresponding planet mass after <iteration_step> steps
    planet_masses, eccentricities = [], []
    for i in sorted(os.listdir('../fargo2d1d/frame_rotation')):
        # only compare simulations of 1mj planets with accretion turned on
        initial_planet_mass = 1e-3
        if not i.startswith('1mj'):
            continue

        planet_file = f'../fargo2d1d/frame_rotation/{i}/out/planet1.dat'
        with open(planet_file) as fp:
            content = fp.readlines()
        try:
            m = float(content[iteration_step].split('\t')[5])
        except IndexError:
            continue
        e = float(i.split('e')[-1])

        planet_masses.append(m)
        eccentricities.append(e)

    # get relative mass increase
    planet_mass_increase = np.array(planet_masses) / initial_planet_mass

    # fit various functions
    exp = lambda x, a, b: a * np.exp(b * x)
    sqr = lambda x, a, b: a * x**2 + b
    cube = lambda x, a, b: a * x**3 + b

    ecc_linspace = np.linspace(sorted(eccentricities)[0], sorted(eccentricities)[-1], 1000)
    popt_e, pcov_e = curve_fit(exp, eccentricities, planet_mass_increase)
    popt_2, pcov_2 = curve_fit(sqr, eccentricities, planet_mass_increase)
    popt_3, pcov_3 = curve_fit(cube, eccentricities, planet_mass_increase)

    # plot relative mass increase m/m_0
    plt.tight_layout()
    plt.title(f'accretion for {r"$1M_{jupiter}$"} planets after {total_nr_of_orbits} orbits')
    #plt.grid(True)

    plt.scatter(eccentricities, planet_mass_increase)
    plt.xlim(min(eccentricities), max(eccentricities))
    plt.ylim(.9 * min(planet_mass_increase), 1.1 * max(planet_mass_increase))

    plt.xlabel('eccentricity')
    plt.ylabel(r'planet mass increase $m/m_0$')  # at iteration_step * nr_of_orbits_between_outputs
    plt.xticks(eccentricities)

    plt.savefig(f'../figures/{simulation_dir}/acc_vs_e.pdf')

    # plot fit functions
    plt.plot(ecc_linspace, exp(ecc_linspace, *popt_e), label=r'fit of $y=a\cdot e^{b\cdot x}$')
    plt.plot(ecc_linspace, sqr(ecc_linspace, *popt_2), label=r'fit of $y=a\cdot x^2+b$', color='red')
    plt.plot(ecc_linspace, cube(ecc_linspace, *popt_3), label=r'fit of $y=a\cdot x^3+b$', color='green')

    plt.legend(loc='upper left')
    plt.savefig(f'../figures/{simulation_dir}/acc_vs_e_with_fit.pdf')


if __name__ == '__main__':

    iteration_step = int(sys.argv[1])
    simulation_dir = 'frame_rotation'

    nr_of_orbits_between_outputs = get_nr_of_orbits_between_outputs(simulation_dir)
    total_nr_of_orbits = iteration_step * nr_of_orbits_between_outputs

    create_plot_for_1MJ(iteration_step)

