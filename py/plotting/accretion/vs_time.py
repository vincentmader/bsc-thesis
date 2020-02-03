
import os
import sys

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import plotting
import sim_params


def plot_mpm0_vs_t(sim_group, sim_id, label, color, set_lims=False):

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

    if set_lims:
        plt.xlim(0, total_nr_of_orbits)
        plt.ylim(0, max(y))


def plot_mdot_vs_t(sim_group, sim_id, label, color, set_lims=False):

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

    if set_lims:
        plt.ylim(0, max_mdot)

    plt.plot(t[1:], acc_rate, label=label, color=color)


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

    # if compare_by == 'mass':
    #     sim_ids = [i for i in reversed(sim_ids)]

    # make sure save directory exists
    if sim_group not in os.listdir(FIGURE_DIR):
        os.system(f'mkdir "{os.path.join(FIGURE_DIR, sim_group)}"')

    # plot for relative mass increase m/m0
    figsize = (4, 4)
    plt.figure(figsize=figsize)
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'relative mass increase $m/m_0$')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

    label, info_text = '', ''

#    if compare_by == 'ecc':
#        colors = ['blue', 'green', 'orange', 'red', 'black']
#    if compare_by == 'mass':
#        colors = ['blue', 'red', 'black']

    colors = list(pl.cm.jet(np.linspace(0.1, 0.9, len(sim_ids))))

    # relative mass increase
    for idx, sim_id in enumerate(sim_ids
        # [i for i in reversed(sorted(
        #     os.listdir(f'../fargo2d1d/{sim_group}'))
        # ) if i != '.DS_Store' and i.startswith('1')]
    ):
        initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)

        if compare_by == 'mass':
            label = f'{r"m="}{initial_planet_mass:.4f}'  # TODO: change to .4f ?
            info_text = r'$e=' + str(initial_planet_eccentricity) + r'$'
        elif compare_by == 'ecc':
            label = f'{r"e="}{initial_planet_eccentricity:.3f}'
            info_text = r'$m_0=' + str(initial_planet_mass * 1000) + r'\ M_{jupiter}$'

        set_lims = True
        if compare_by == 'mass':
            set_lims = True if idx == 0 else False

        plot_mpm0_vs_t(sim_group, sim_id, label, color=colors[idx], set_lims=set_lims)

    #plt.title(f'relative mass increase for planets with {info_text}')
#    if compare_by == 'mass' or sim_group == '50000_orbits':
#        plt.gca().legend(
#            loc='lower center', bbox_to_anchor=(0.5, 0.025),
#            ncol=3, fancybox=False, shadow=False
#        )

    plt.savefig(f'{FIGURE_DIR}/{sim_group}/mpm0_vs_t_and_{compare_by}.pdf')
    if sim_group in ['50000_orbits']:
        plt.yscale('log')
        plt.ylim(0.7, 5)
        ticks = np.array(range(1, 5))
        plt.yticks(ticks, ticks)
        plt.gcf().subplots_adjust(left=.175)
#        plt.gca().legend(
#            loc='upper center', bbox_to_anchor=(0.5, 0.025),
#            ncol=3, fancybox=False, shadow=False
#        )
        plt.savefig(f'{FIGURE_DIR}/{sim_group}/mpm0_vs_t_and_{compare_by}_log.pdf')
    plt.close()

    # plot for accretion rate (m_i - m_j, i=j+1)
    figsize = (4, 4)
    plt.figure(figsize=figsize)
    plt.xlabel('number of orbits since simulation start')
    plt.ylabel(r'mass accretion rate $\dot m$ [code units]')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

    # accretion rate
    for idx, sim_id in enumerate(sim_ids
        # [i for i in reversed(sorted(
        #     os.listdir(f'../fargo2d1d/{sim_group}'))
        # ) if i != '.DS_Store' and i.startswith('1')]
    ):

        initial_planet_mass = sim_params.planets.initial_mass(sim_group, sim_id)
        initial_planet_eccentricity = sim_params.planets.initial_eccentricity(sim_group, sim_id)

        if compare_by == 'mass':
            label = f'{r"m="}{initial_planet_mass:.4f}'  # TODO: change to .4f ?
            info_text = r'$e=' + str(initial_planet_eccentricity) + r'$'
        elif compare_by == 'ecc':
            label = f'{r"e="}{initial_planet_eccentricity:.3f}'
            info_text = r'$m_0=' + str(initial_planet_mass * 1000) + r'\ M_{jupiter}$'

        set_lims = True
        if compare_by == 'mass':
            set_lims = True if idx == 0 else False

        plot_mdot_vs_t(sim_group, sim_id, label, color=colors[idx], set_lims=set_lims)

    #plt.title(f'accretion rate for planets with {info_text}')
#    if compare_by == 'mass':
#        plt.legend(loc='lower right')
#    if sim_group == '50000_orbits':
    plt.legend(loc='upper right')

    save_loc = os.path.join(FIGURE_DIR, sim_group, f'dotm_vs_t_and_{compare_by}.pdf')
    plt.savefig(save_loc)
    if sim_group in ['50000_orbits']:
        plt.yscale('log')
        plt.ylim(1e-8, 1e-6)
        plt.gcf().subplots_adjust(left=.175)
        plt.savefig(f'{FIGURE_DIR}/{sim_group}/dotm_vs_t_and_{compare_by}_log.pdf')

    # compare radial gas profile for times of equal accretion rates
    if sim_group in ['frame_rotation'] and compare_by == 'mass':
        save_loc = os.path.join(FIGURE_DIR, sim_group, f'dotm_vs_t_and_{compare_by}_1.pdf')
        plt.savefig(save_loc)

        x = np.linspace(0, 2500, 2)
        y = [3e-7] * len(x)
        plt.plot(x, y, color='black')

        save_loc = os.path.join(FIGURE_DIR, sim_group, f'dotm_vs_t_and_{compare_by}_2.pdf')
        plt.savefig(save_loc)

        plt.plot([850] * 2, [0, 1], color='black')
        plt.plot([1300] * 2, [0, 1], color='black')
        plt.plot([1750] * 2, [0, 1], color='black')
        save_loc = os.path.join(FIGURE_DIR, sim_group, f'dotm_vs_t_and_{compare_by}_3.pdf')
        plt.savefig(save_loc)
        plt.close()

        plt.figure(figsize=(8, 4))
        for idx, nr_of_orbits in enumerate([1750, 1300, 850]):
            sim_id = ['0.5mj_e.000', '1.0mj_e.000', '1.5mj_e.000'][idx]
            mass = float(sim_id.split('m')[0])
            outfile_idx = nr_of_orbits // 50
            plotting.gas_density.logarithmic_1D(
                plt.gca(), sim_group, sim_id, outfile_idx,
                color=['blue', 'green', 'red'][idx],
                label=f'm={mass} {r"$m_{jupiter}$"} after {nr_of_orbits} orbits'
            )

        plt.xlabel('radial distance $r$ [code units]')
        plt.ylabel('azimuthally averaged surface density $\Sigma$ [code units]')
        plt.legend(loc='lower right')
        plt.xlim(0.2, 5)

        save_loc = os.path.join(FIGURE_DIR, sim_group, f'sigma_vs_r_for_same_acc_rates.pdf')
        plt.savefig(save_loc)

    plt.close()


def main(sim_group):

    # TODO: also allow for new sim_group, with realistic cores,
    #       more orbits (and maybe without fixed frame rotation)
    if sim_group not in ['frame_rotation', '10000_orbits', '50000_orbits']:
        return

    print('  plotting accretion.vs_time')

    # create individual plot for each simulation
    for sim_id in os.listdir(os.path.join(FARGO_DIR, sim_group)):
        if sim_id == '.DS_Store' or 'unp' in sim_id:
            continue
        create_plot_for_single_sim(sim_group, sim_id)

    # create plot comparing all planets with mass   m = 1 M_J
    mass_for_comparison_plot = 1e-3
    # create list with all sim_ids needed for this plot
    sim_ids = []
    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id == '.DS_Store' or 'unp' in sim_id:
            continue
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if ecc >= .25:
            continue
        if ecc == 0.05 and sim_group == '50000_orbits':
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
        if sim_id == '.DS_Store' or 'unp' in sim_id:
            continue
        # check whether initial eccentricity is equal to mass_for_comparison_plot
        ecc = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        if ecc == ecc_for_comparison_plot:
            sim_ids.append(sim_id)
    create_comparison_plot(sim_group, sim_ids, 'mass')


if __name__ == '__main__':
    sim_group, sim_id = sys.argv[1], sys.argv[2]
    main(sim_group)

