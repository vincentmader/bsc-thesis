
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import config
from config import FARGO_DIR
from config import FIGURE_DIR
import sim_params


WANTED_INITIAL_MASS = 1e-3


def main(sim_group, iteration_step):
    # TODO: also allow for other sim_groups ?
    if sim_group not in ['frame_rotation']:
        return

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')

    initial_masses, current_masses, initial_eccentricities = [], [], []
    # loop over all sim_ids with initial_mass of 1 M_J
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        current_mass = sim_params.planets.current_mass(sim_group, sim_id, iteration_step)
        initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if (initial_mass - WANTED_INITIAL_MASS) / initial_mass > 0.05:
            continue

        initial_masses.append(initial_mass)
        current_masses.append(current_mass)
        initial_eccentricities.append(initial_eccentricity)

    # convert to numpy arrays
    initial_masses = np.array(initial_masses)
    current_masses = np.array(current_masses)
    initial_eccentricities = np.array(initial_eccentricities)
    planet_mass_increase = current_masses / initial_masses

    orbit_num = iteration_step * sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)

    # plot setup
    plt.figure(figsize=(8, 4))
    plt.title(f'accretion for 1.0 {"$M_{jupiter}$"} planets after {orbit_num} orbits')
    plt.xlim(min(initial_eccentricities), max(initial_eccentricities))
    plt.ylim(.9 * min(planet_mass_increase), 1.1 * max(planet_mass_increase))
    plt.xlabel('eccentricity')
    plt.ylabel(r'planet mass increase $m/m_0$')  # at iteration_step * nr_of_orbits_between_outputs
    plt.xticks(initial_eccentricities)
    plt.grid(True)

    # plot
    plt.scatter(initial_eccentricities, current_masses / initial_masses)

    # save
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_e.pdf')
    plt.savefig(save_path)

    # fit various functions
    exp = lambda x, a, b: a * np.exp(b * x)
    sqr = lambda x, a, b: a * x**2 + b
    cube = lambda x, a, b: a * x**3 + b

    ecc_linspace = np.linspace(sorted(initial_eccentricities)[0], sorted(initial_eccentricities)[-1], 1000)
    popt_e, pcov_e = curve_fit(exp, initial_eccentricities, planet_mass_increase)
    popt_2, pcov_2 = curve_fit(sqr, initial_eccentricities, planet_mass_increase)
    popt_3, pcov_3 = curve_fit(cube, initial_eccentricities, planet_mass_increase)

    # plot fit functions
    plt.plot(ecc_linspace, exp(ecc_linspace, *popt_e), label=r'fit of $y=a\cdot e^{b\cdot x}$')
    plt.plot(ecc_linspace, sqr(ecc_linspace, *popt_2), label=r'fit of $y=a\cdot x^2+b$', color='red')
    plt.plot(ecc_linspace, cube(ecc_linspace, *popt_3), label=r'fit of $y=a\cdot x^3+b$', color='green')
    plt.legend(loc='upper left')

    # save
    save_path = os.path.join(FIGURE_DIR, sim_group, 'mpm0_vs_e_fit.pdf')
    plt.savefig(save_path)
    plt.close()



if __name__ == '__main__':
    sim_group, iteration_step = sys.argv[1], sys.argv[2]
    main(sim_group, iteration_step)

