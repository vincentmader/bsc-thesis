
import os
import sys

from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


# setup
SIMULATION_DIR = sys.argv[1]
SIMULATION_ID = sys.argv[2]
FIGURES_DIR = f'../figures/{SIMULATION_DIR}/{SIMULATION_ID}/'
CMAP = 'coolwarm'

R_MIN, R_MAX = 0.2, 3.0


def get_initial_planet_mass():
    path = f'../fargo2d1d/{SIMULATION_DIR}/{SIMULATION_ID}/out/planet1.dat'
    with open(path) as fp:
        content = fp.readlines()
    taper = get_taper()
    initial_mass = float(content[taper].split('\t')[5])
    return np.round(initial_mass, 5)


def get_resolution():
    """return tuple (res_r, res_φ)"""
    #RES_r, RES_φ = 101, 634  # for cprH = 2.5
    #RES_r, RES_φ = 202, 1269  # for cprH = 5
    #RES_r, RES_φ = 404, 2537  # for cprH = 10
    #RES_r, RES_φ = 552, 1104  # for first_tests/rH5...
    #RES_r, RES_φ = 300, 600  # for first_tests/ecc...
    if SIMULATION_DIR == 'testing_cells_per_rH':
        if SIMULATION_ID.startswith('2.5'):
            return (101, 634)
        elif SIMULATION_ID.startswith('5'):
            return (202, 1269)
        elif SIMULATION_ID.startswith('10'):
            return (404, 2537)
    elif SIMULATION_DIR in ['testing_masses']:
        return (202, 1269)
    else:  # fallback on resolution calculated for 5 cells in Hill radius (1 MJ)
        return (202, 1269)


def get_eccentricity():
    return float(SIMULATION_ID.split('e')[-1])


def get_taper():
    """return value of taper parameter"""
    if SIMULATION_DIR in ['testing_cells_per_rH']:
        return 3
    elif SIMULATION_DIR in ['testing_masses']:
        return 10


def get_total_nr_of_steps():
    all_files = os.listdir(f'../fargo2d1d/{SIMULATION_DIR}/{SIMULATION_ID}/out')
    return sum([
        1 for f in all_files if f.startswith('gasdens') and
        not f.startswith('gasdens1D') and not f.startswith('gasdens.ascii')
    ])


def create_cartesian_2D_plot(ax, path_to_2D_data):

    res_r, res_φ = get_resolution()

    σ = np.fromfile(f'{path_to_2D_data}').reshape(res_r, res_φ)
    ## rearange 2d array so that planet sits in the center of plot
    #for row_idx, row in enumerate(σ):
    #    first_half = list(row)[:int(res_φ / 2)]
    #    second_half = list(row)[int(res_φ / 2):]
    #    σ[row_idx] = np.array(second_half + first_half)
    plt.imshow(np.log10(σ), origin='lower', aspect='auto', cmap=CMAP, vmin=-4.5, vmax=-2.5)
    plt.colorbar()

    plt.title(r'$log_{10}(\sigma)$')
    xticks_locs = [0, .25 * res_φ, .5 * res_φ, .75 * res_φ, res_φ]
    xticks_vals = [0, 90, 180, 270, 360]
    plt.xticks(xticks_locs, xticks_vals)
    yticks_locs = [0, .25 * res_r, .5 * res_r, .75 * res_r, res_r]
    seg_to_comp_units = lambda seg: np.round(R_MIN + (R_MAX - R_MIN) * seg / res_r, 1)
    yticks_vals = seg_to_comp_units(np.array(yticks_locs))
    plt.yticks(yticks_locs, yticks_vals)

    ax.set_xlabel(r'azimuthal angle $\varphi$ [deg]')
    ax.set_ylabel('radial distance $r$ [comp. units]')


def create_polar_2D_plot(ax, path_to_2D_data):
    res_r, res_φ = get_resolution()
    r = np.linspace(R_MIN, R_MAX, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)

    plt.title('')
    σ = np.log10(np.fromfile(f'{path_to_2D_data}').reshape(res_r, res_φ))
    plt.pcolormesh(φ, r, σ, cmap=CMAP, vmin=-4.5, vmax=-2.5)
    plt.xticks([])
    plt.yticks([])


def create_1D_plot(ax, path_to_1D_data):
    #λ = np.fromfile(f'{path_to_1D_data}')
    with open(f'{path_to_1D_data}') as fp:
        content = fp.readlines()
    λ = [float(line.split(' ')[1]) for line in content]
    plt.plot(λ)
    plt.xlim(0, 50)
    plt.xlabel(r'radial distance $r$ [comp. units]')
    plt.ylabel(r'surface density $\sigma$')


def create_info_box(ax, iteration_step):
    initial_mass = get_initial_planet_mass()
    total_nr_of_steps = get_total_nr_of_steps()
    res_r, res_φ = get_resolution()

    plt.plot()
    plt.text(0.1, 0.9, r'planet mass: ' + str(initial_mass) + r' $M_{sun}$')
    plt.text(0.1, 0.8, f'eccentricity: {get_eccentricity()}')
    plt.text(0.1, 0.7, 'resolution: {}{}{}'.format(res_r, r'$\times$', res_φ))
    plt.text(0.1, 0.1, f'orbit num: {iteration_step} / {total_nr_of_steps - 1}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks([])
    plt.yticks([])


def create_gif():
    print('creating gif')
    sorted_img_files = sorted(os.listdir(FIGURES_DIR))
    img_space_img_etc = ' '.join([
        f'{FIGURES_DIR}/{i}' for i in sorted_img_files if i.endswith('.png')
    ])
    os.system(f'convert {img_space_img_etc} {FIGURES_DIR}evolution.gif')


def create_plot_collage(iteration_step):

    # define file paths for 2d and 1d data, then load them in
    path_to_2D_data = f'../fargo2d1d/{SIMULATION_DIR}/{SIMULATION_ID}/out/gasdens{iteration_step}.dat'
    path_to_1D_data = f'../fargo2d1d/{SIMULATION_DIR}/{SIMULATION_ID}/out/gasdens.ascii_rad.{iteration_step}.dat'
    if not (os.path.exists(path_to_2D_data) and os.path.exists(path_to_1D_data)):
        return
    print(f'plotting data for file {iteration_step}')

    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 3, figure=fig)

    # plot 2d data in rectangular grid
    ax = fig.add_subplot(gs.new_subplotspec((0, 0), colspan=3))
    create_cartesian_2D_plot(ax, path_to_2D_data)

    # plot 1d data
    ax = plt.subplot(gs.new_subplotspec((1, 0), colspan=1))
    create_1D_plot(ax, path_to_1D_data)

    # get info
    ax = plt.subplot(gs.new_subplotspec((1, 1), colspan=1))
    create_info_box(ax, iteration_step)

    # plot 2d data in polar coords
    ax = plt.subplot(gs.new_subplotspec((1, 2), colspan=1), projection='polar')
    create_polar_2D_plot(ax, path_to_2D_data)

    # make sure sorting is done right
    if iteration_step < 10:
        iteration_step = f'0{iteration_step}'
    # save and reset figure
    plt.savefig(f'{FIGURES_DIR}plot{iteration_step}.png')
    plt.clf()
    plt.close()


if __name__ == '__main__':
    # create necessary directory structure
    if SIMULATION_DIR not in os.listdir('../figures'):
        os.mkdir(f'../figures/{SIMULATION_DIR}')
    if SIMULATION_ID not in os.listdir(f'../figures/{SIMULATION_DIR}'):
        os.mkdir(f'../figures/{SIMULATION_DIR}/{SIMULATION_ID}')
    # loop over all files in simulation output directory
    for iteration_step in range(100):
        create_plot_collage(iteration_step)
    # create gif of all images that where created
    create_gif()

