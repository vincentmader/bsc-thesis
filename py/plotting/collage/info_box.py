
import os

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR
import sim_params


def main(ax, sim_group, sim_id, iteration_step):

    # get masses measured in units of one Jupiter mass
    initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
    current_mass = sim_params.planets.current_mass(sim_group, sim_id, iteration_step)
    # get eccentricity
    initial_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
    # get resolution
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    # get number of orbits per output
    orbits_per_output = sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    # get number of current orbit
    current_orbit_nr = iteration_step * orbits_per_output
    # get number of current output file
    current_output_file_nr = iteration_step % orbits_per_output
    # total number of iterations
    nr_of_iterations = sim_params.general.nr_of_iterations(sim_group, sim_id)
    # total number of orbits
    nr_of_orbits = int(nr_of_iterations)

    # other info
#    total_nr_of_steps = get_total_nr_of_steps(SIMULATION_DIR, SIMULATION_ID)
#    nr_of_orbits_between_outputs = get_nr_of_orbits_between_outputs(SIMULATION_DIR)
#    current_orbit_nr = iteration_step * nr_of_orbits_between_outputs
#    total_nr_of_orbits = (total_nr_of_steps - 1) * nr_of_orbits_between_outputs

    plt.plot()
    plt.text(0.1, 0.9, f'initial planet mass: {round(initial_mass, 5)} {r"$M_{jupiter}$"}')
    plt.text(0.1, 0.8, f'current planet mass: {round(current_mass, 5)} {r"$M_{jupiter}$"}')
    plt.text(0.1, 0.7, f'eccentricity: {initial_eccentricity}')
    plt.text(0.1, 0.6, 'resolution: {}{}{}'.format(res_r, r'$\times$', res_φ))
    plt.text(0.1, 0.2, f'orbit number: {current_orbit_nr} / {nr_of_orbits}')
    plt.text(0.1, 0.1, f'out file number: {current_output_file_nr} / {int(nr_of_iterations / orbits_per_output)}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks([])
    plt.yticks([])
