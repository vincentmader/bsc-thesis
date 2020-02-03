
import math
import os

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi as π

import analysis
import config
from config import FARGO_DIR
import setup
import sim_params


GAP_SEARCH_DISTANCES = [5, 10]


def main(ax, sim_group, sim_id, iteration_step, plot_gap_bounds=False):

    CMAP = 'coolwarm'

    # get resolution
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    # get inner and outer radial boundaries for disk simulation
    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)

    m_p = sim_params.planets.initial_mass(sim_group, sim_id)
    a_p = sim_params.planets.initial_semi_major_axis(sim_group, sim_id)
    e_p = sim_params.planets.initial_eccentricity(sim_group, sim_id)

    # define linspace for radial and azimuthal dimension
    r = np.linspace(r_min, r_max, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)

    # load gas density from file
    Σ = setup.load_gas_density.sigma_2D(
        sim_group, sim_id, iteration_step
    )

    # get position of planet in disk
    r_planet, φ_planet = sim_params.planets.current_position_rφ(
        sim_group, sim_id, iteration_step
    )
    # convert position to indices of rows and columns in 2D array
    planet_col_idx = int(math.floor(φ_planet / (2*π) * res_φ))
    planet_row_idx = int(math.floor((1 - r_min) * res_r / (r_max - r_min)))
    # rearange 2D array so that planet sits at the same spot in each image
    for row_idx, row in enumerate(Σ):
        first_half = list(row)[:int(planet_col_idx)]
        second_half = list(row)[int(planet_col_idx):]
        Σ[row_idx] = np.array(second_half + first_half)
    # rearange 2D array so that planet sits in the center of plot
    for row_idx, row in enumerate(Σ):
        first_half = list(row)[:int(res_φ / 2)]
        second_half = list(row)[int(res_φ / 2):]
        Σ[row_idx] = np.array(second_half + first_half)

    # plot gap boundaries
    for idx, gap_search_distance_in_rH in enumerate(GAP_SEARCH_DISTANCES):
        style = ['-', '--'][idx]
        inner_gap_boundary, outer_gap_boundary = analysis.gap.boundaries(
            r, Σ, gap_search_distance_in_rH, m_p, a_p, e_p
        )
        plt.plot(φ, inner_gap_boundary, f'k{style}')
        plt.plot(φ, outer_gap_boundary, f'k{style}')

    # plot gas density
    plt.imshow(
        np.log10(Σ), origin='lower', aspect='auto', cmap=CMAP,
        vmin=-4.5, vmax=-2.5, extent=(0, 2 * np.pi, r_min, r_max)
    )

    # various
    plt.title(r'$log_{10}(\Sigma)$')
    plt.colorbar()

    plt.xticks(
        [0, π/2, π, 3/2*π, 2*π],
        ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3}{2}\pi$', r'$2\pi$']
    )
    # yticks_locs = [0, .25 * res_r, .5 * res_r, .75 * res_r, res_r]
    # seg_to_code_units = lambda seg: np.round(r_min + (r_max - r_min) * seg / res_r, 1)
    # yticks_vals = seg_to_code_units(np.array(yticks_locs))
    # plt.yticks(yticks_locs, yticks_vals)

    plt.xlim(0, 2*π)
    plt.ylim(r_min, r_max)

    ax.set_xlabel(r'azimuthal angle $\varphi$ [deg]')
    ax.set_ylabel(r'radial distance $r$ [code units]')

