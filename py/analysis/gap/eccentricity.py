
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi as π

import analysis
import config
import setup
import sim_params


def main(sim_group, sim_id, outfile_idx, search_distance_in_rH=10):
    # notify when bullshit files are being given as input
    if sim_group == '.DS_Store' or sim_id == '.DS_Store':
        raise Exception('cannot calculate gap eccentricity for .DS_Store')

    # get resolution
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    # get inner and outer radial boundaries of disk simulation
    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)
    # define linspace for radial and azimuthal dimension
    # r = np.linspace(r_min, r_max, res_r)
    # φ = np.linspace(0, 2 * np.pi, res_φ)

    # load gas density from file
    Σ_2D = setup.load_gas_density.sigma_2D(sim_group, sim_id, outfile_idx)
    # load sigma_unp
    Σ_unp = setup.setup.sigma_unp(sim_group, sim_id, outfile_idx)
    # load r velocity
    v_rad = setup.load_velocity.v_rad(sim_group, sim_id, outfile_idx)
    # load theta velocity
    v_theta = setup.load_velocity.v_theta(sim_group, sim_id, outfile_idx)

    cell_eccs = []
    for row_idx, row in enumerate(Σ_2D):
        for col_idx, col in enumerate(row):
            # test if cell is in gap
            if col / Σ_unp[row_idx] > 0.1:
                continue
            G, M = 1, 1
            # calculate position of cell
            r = row_idx / res_r * (r_max - r_min) + r_min
            φ = col_idx / res_φ * 2 * π
            x = r * np.cos(φ)
            y = r * np.sin(φ)
            # calculate 2D velocity vector of cell
            vx = v_rad[row_idx][col_idx] * np.sin(φ) + v_theta[row_idx][col_idx] * np.cos(φ)
            vy = v_rad[row_idx][col_idx] * np.cos(φ) - v_theta[row_idx][col_idx] * np.sin(φ)
            # calculate length of angular momentum vector via cross product r x v
            # which is equal to the z-component of the vector (2D rotation)
            L = x * vy - y * vx
            # calculate length of semimajor axis from energy conservation
            a = - G * M / 2 / ((vx**2 + vy**2) / 2 - G * M / r)
            # calculate cell eccentricity
            cell_ecc = np.sqrt(L**2 / (G * M * a))
            # the above should actually be sqrt(1 - ...), why does this lead
            # to the opposite of the trend in the results one would ecpect?
            # several other things are wrong too...
            cell_eccs.append(cell_ecc)

    gap_ecc = np.mean(cell_eccs)

    # define current mass, semi-major axis and eccentricity of planet
    # planet_m = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)
    # planet_a = sim_params.planets.current_position_rφ(sim_group, sim_id, outfile_idx)[0]  # TODO: this is r, not a! correct this
    # planet_e = sim_params.planets.current_eccentricity(sim_group, sim_id, outfile_idx)

    # r_gap_inner, r_gap_outer = analysis.gap.boundaries(
    #     r, Σ_2D, search_distance_in_rH, planet_m, planet_a, planet_e
    # )

    return gap_ecc


if __name__ == '__main__':
    sim_group, sim_id = 'frame_rotation', '1mj_e.00'
    outfile_idx = 50
    main(sim_group, sim_id, outfile_idx)

