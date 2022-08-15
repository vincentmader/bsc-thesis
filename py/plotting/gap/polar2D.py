import os

import matplotlib.pyplot as plt
import numpy as np

from config import FARGO_DIR, FIGURE_DIR
import analysis, plotting, setup, sim_params


CMAP = 'coolwarm'


def plot_sigma(sim_group, sim_id, outfile_idx, compare_by):

    m0 = sim_params.planets.initial_mass(sim_group, sim_id)
    e0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)

    fig = plt.figure(figsize=(16, 16))

    ax = plt.subplot(111, projection='polar')
    plotting.gas_density.polar_2D(ax, sim_group, sim_id, outfile_idx)

    plt.yticks(np.arange(0, 2, 0.05))
    plt.grid(True, color='black')
    if compare_by == 'ecc':
        plt.ylim(0.5, 1.5)
        if e0 > 0.1:
            plt.ylim(1.0, 2.2)


    if 'gap_ecc' not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
        os.mkdir(os.path.join(FIGURE_DIR, sim_group, 'gap_ecc'))
    save_loc = os.path.join(
        FIGURE_DIR, sim_group, 'gap_ecc', f'{sim_id}.png'
    )
    plt.savefig(save_loc)


def plot_gap_boundaries(sim_group, sim_id, outfile_idx=50):

    # setup
    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    r = np.linspace(r_min, r_max, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)
    Σ = setup.load_gas_density.sigma_2D(sim_group, sim_id, outfile_idx)
    m_p = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)
    a_p = sim_params.planets.current_semimajor_axis(sim_group, sim_id, outfile_idx)
    e_p = sim_params.planets.current_eccentricity(sim_group, sim_id, outfile_idx)

    # plot sigma
    fig = plt.figure(figsize=(6, 10))

    ax = plt.subplot(211, projection='polar')
    plt.pcolormesh(φ, r, Σ, cmap=CMAP)#, vmin=-4.5, vmax=-2.5)
    for search_distance_in_rH in [10]:
        # get gap bounds
        inner_bounds, outer_bounds = analysis.gap.boundaries(
            r, Σ, search_distance_in_rH, m_p, a_p, e_p
        )
    # plt.plot(φ, inner_bounds, color='green')
    plt.plot(φ, outer_bounds, color='red')

    ax = plt.subplot(212)
    plt.plot(φ, outer_bounds)

    # save
    if 'gap_boundaries' not in os.listdir(
        os.path.join(FIGURE_DIR, sim_group, sim_id)
    ):
        os.mkdir(os.path.join(FIGURE_DIR, sim_group, sim_id, 'gap_boundaries'))
    save_loc = os.path.join(
        FIGURE_DIR, sim_group, sim_id, 'gap_boundaries', f'out{outfile_idx}.png'
    )
    plt.savefig(save_loc)
    plt.close()


def plot_pressure_gradient(sim_group, sim_id, outfile_idx):

    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)

    r = np.linspace(r_min, r_max, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)
    Σ = setup.load_gas_density.sigma_2D(sim_group, sim_id, outfile_idx)

    cols = [[Σ[i][j] for i in range(Σ.shape[0])] for j in range(Σ.shape[1])]
    pressures = [analysis.gap.pressure(r, Σ_1D) for Σ_1D in cols]
    pressures = np.transpose(np.array(pressures))

    grad = lambda x, y: np.diff(y) / np.diff(x)
    grad_log_p = [grad(np.log(r), np.log(p)) for p in np.transpose(pressures)]
    grad_log_p = np.transpose(grad_log_p)

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection='polar')
    plt.pcolormesh(φ, r[1:], grad_log_p, cmap=CMAP)#, vmin=-4.5, vmax=-2.5)

    if 'pressure' not in os.listdir(os.path.join(FIGURE_DIR, sim_group, sim_id)):
        os.mkdir(os.path.join(FIGURE_DIR, sim_group, sim_id, 'pressure'))
    save_loc = os.path.join(
        FIGURE_DIR, sim_group, sim_id, 'pressure', 'gradient.png'
    )
    plt.savefig(save_loc)
    plt.close()



def main(compare_by=None):
    sim_group = 'frame_rotation'
    sim_group_dir = os.path.join(FARGO_DIR, sim_group)
    for sim_id in sorted(os.listdir(sim_group_dir)):
        if sim_id in ['.DS_Store', 'unp']:
            continue

        m0 = sim_params.planets.initial_mass(sim_group, sim_id)
        e0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        outfile_idx = sim_params.general.nr_of_outputs(sim_group, sim_id)
        if compare_by == 'mass' and e0 != 0:
            continue
        elif compare_by == 'ecc' and m0 != 1e-3:
            continue
        print(sim_id)

        # plot_sigma(sim_group, sim_id, outfile_idx)
        plot_pressure_gradient(sim_group, sim_id, outfile_idx)
        plot_gap_boundaries(sim_group, sim_id)

