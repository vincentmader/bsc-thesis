
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR
from config import FIGURE_DIR
import sim_params


def plot_mpm0_vs_t(sim_group, sim_id, label, color):

    planet1_file_path = os.path.join(FARGO_DIR, sim_group, sim_id, 'out/planet1.dat')
    with open(planet1_file_path) as fp:
        content = fp.readlines()

    initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
    nr_of_orbits_between_outputs = sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    total_nr_of_orbits = sim_params.general.nr_of_iterations(sim_group, sim_id)
    initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)

    mass = [float(row.split('\t')[5]) for row in content]
    t = np.linspace(0, total_nr_of_orbits, len(mass))
    y = np.array(mass) / initial_planet_mass

    plt.plot(t, y, label=label, color=color)

    plt.grid(True)
    plt.xlim(0, total_nr_of_orbits)
    plt.ylim(0, max(y))


def plot_mdot_vs_t(sim_group, sim_id, label, color):

    with open(f'../fargo2d1d/{sim_group}/{sim_id}/out/planet1.dat') as fp:
        content = fp.readlines()

    initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
    nr_of_orbits_between_outputs = sim_params.general.nr_of_iterations_per_output(sim_group, sim_id)
    total_nr_of_steps = sim_params.general.nr_of_iterations(sim_group, sim_id)
    total_nr_of_orbits = total_nr_of_steps
    initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)

    #plt.ylim(0, 3e-6)
    #plt.ylim(
    #    0, max([acc_rate[sim_params.general.accretion_start_time_out_file_idx(sim_group, sim_id)] for sim_id in sim_ids])
    #)

    mass = [float(row.split('\t')[5]) for row in content]
    t = np.linspace(0, total_nr_of_orbits, len(mass))
    acc_rate = np.diff(mass) / np.diff(t)

    accretion_start_orbit_num = sim_params.general.accretion_start_time_in_orbits(sim_group, sim_id)
    plt.xlim(accretion_start_orbit_num, total_nr_of_orbits)
    accretion_start_outfile_idx = sim_params.general.accretion_start_time_out_file_idx(sim_group, sim_id)
    #if sim_group in ['10000_orbits', '50000_orbits']:
    #    accretion_start_time_out_file_idx -= 100
    max_mdot = max(acc_rate[accretion_start_outfile_idx - 1:])
    plt.ylim(0, max_mdot)

    plt.plot(t[1:], acc_rate, label=label, color=color)

    plt.grid(True)


def create_plot_for_single_sim(sim_group, sim_id):

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')
    if sim_id not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group, sim_id)}"')

    label = ''

    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'relative mass increase $m/m_0$')

    # plots for relative mass increase m/m0
    plot_mpm0_vs_t(sim_group, sim_id, label, color='black')

    save_path = os.path.join(FIGURE_DIR, sim_group, sim_id, 'mpm0_vs_t.pdf')
    plt.savefig(save_path)
    plt.close()

    # plots for accretion rate (m_i - m_j, i=j+1)
    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'relative mass increase $m/m_0$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

    plot_mdot_vs_t(sim_group, sim_id, label, color='black')

    save_path = os.path.join(FIGURE_DIR, sim_group, sim_id, 'dotm_vs_t.pdf')
    plt.savefig(save_path)
    plt.close()


def create_comparison_plot(sim_group, sim_ids, compare_by):

    if compare_by == 'mass':
        sim_ids = [i for i in reversed(sim_ids)]

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')

    # plot for relative mass increase m/m0
    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'relative mass increase $m/m_0$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

    label, info_text = '', ''

#    if compare_by == 'ecc':
#        colors = ['blue', 'green', 'orange', 'red', 'black']
#    if compare_by == 'mass':
#        colors = ['blue', 'red', 'black']

    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(sim_ids))))

    for idx, sim_id in enumerate(sim_ids
        # [i for i in reversed(sorted(
        #     os.listdir(f'../fargo2d1d/{sim_group}'))
        # ) if i != '.DS_Store' and i.startswith('1')]
    ):
        initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if compare_by == 'mass':
            label = f'{r"m="}{initial_planet_mass:.3f}'  # TODO: change to .4f ?
            info_text = r'$e=' + str(initial_planet_eccentricity) + r'$'
        elif compare_by == 'ecc':
            label = f'{r"e="}{initial_planet_eccentricity:.2f}'
            info_text = r'$m_0=' + str(initial_planet_mass * 1000) + r'\ M_{jupiter}$'

        plot_mpm0_vs_t(sim_group, sim_id, label, color=colors[idx])

    plt.title(f'relative mass increase for planets with {info_text}')
    plt.legend(loc='upper left')
    plt.savefig(f'{FIGURE_DIR}/{sim_group}/mpm0_vs_t_and_{compare_by}.pdf')
    plt.close()

    # plot for accretion rate (m_i - m_j, i=j+1)
    plt.figure(figsize=(8, 4))
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'mass accretion rate $\dot m$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

    for idx, sim_id in enumerate(sim_ids
        # [i for i in reversed(sorted(
        #     os.listdir(f'../fargo2d1d/{sim_group}'))
        # ) if i != '.DS_Store' and i.startswith('1')]
    ):

        initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if compare_by == 'mass':
            label = f'{r"m="}{initial_planet_mass:.3f}'  # TODO: change to .4f ?
            info_text = r'$e=' + str(initial_planet_eccentricity) + r'$'
        elif compare_by == 'ecc':
            label = f'{r"e="}{initial_planet_eccentricity:.2f}'
            info_text = r'$m_0=' + str(initial_planet_mass * 1000) + r'\ M_{jupiter}$'

        plot_mdot_vs_t(sim_group, sim_id, label, color=colors[idx])

    plt.title(f'accretion rate for planets with {info_text}')
    plt.legend(loc='upper right')

    plt.savefig(f'{FIGURE_DIR}/{sim_group}/dotm_vs_t_and_{compare_by}.pdf')
    plt.close()



def main(sim_group):

    # TODO: also allow for new sim_group, with realistic cores,
    #       more orbits (and maybe without fixed frame rotation)
    if sim_group not in ['frame_rotation', '10000_orbits', '50000_orbits']:
        return

    # create individual plot for each simulation
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id == '.DS_Store':
            continue
        create_plot_for_single_sim(sim_group, sim_id)

    # create plot comparing all planets with mass   m = 1 M_J
    mass_for_comparison_plot = 1e-3
    # create list with all sim_ids needed for this plot
    sim_ids = []
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id == '.DS_Store':
            continue
        # check whether initial mass is equal to mass_for_comparison_plot
        initial_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        if abs(initial_mass - mass_for_comparison_plot) / initial_mass < 0.05:
            sim_ids.append(sim_id)
    create_comparison_plot(sim_group, sim_ids, 'ecc')

    # create plot comparing all planets with eccentricity   e = 0
    ecc_for_comparison_plot = 0.
    # create list with all sim_ids needed for this plot
    sim_ids = []
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id == '.DS_Store':
            continue
        # check whether initial eccentricity is equal to mass_for_comparison_plot
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if ecc == ecc_for_comparison_plot:
            sim_ids.append(sim_id)
    create_comparison_plot(sim_group, sim_ids, 'mass')


if __name__ == '__main__':
    sim_group, sim_id = sys.argv[1], sys.argv[2]
    main(sim_group)

