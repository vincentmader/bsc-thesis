
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import analysis
import config
import setup
import sim_params


def main(sim_group, sim_id, outfile_idx, search_distance_in_rH=5):
    # notify when bullshit files are being given as input
    if sim_group == '.DS_Store' or sim_id == '.DS_Store':
        raise Exception('cannot calculate gap eccentricity for .DS_Store')

    # get resolution
    res_r, res_φ = sim_params.resolution.get_2D_res(sim_group, sim_id)
    # get inner and outer radial boundaries of disk simulation
    r_min = sim_params.radial_boundaries.r_min_2D(sim_group, sim_id)
    r_max = sim_params.radial_boundaries.r_max_2D(sim_group, sim_id)
    # define linspace for radial and azimuthal dimension
    r = np.linspace(r_min, r_max, res_r)
    φ = np.linspace(0, 2 * np.pi, res_φ)

    # load gas density from file
    Σ_2D = setup.load_gas_density.sigma_2D(
        sim_group, sim_id, outfile_idx
    )

    # define current mass, semi-major axis and eccentricity of planet
    planet_m = sim_params.planets.current_mass(sim_group, sim_id, outfile_idx)
    planet_a = sim_params.planets.current_position_rφ(sim_group, sim_id, outfile_idx)[0]  # TODO: this is r, not a! correct this
    planet_e = sim_params.planets.current_eccentricity(sim_group, sim_id, outfile_idx)

    r_gap_inner, r_gap_outer = analysis.gap.boundaries(
        r, Σ_2D, search_distance_in_rH, planet_m, planet_a, planet_e
    )

    ecc_inner = calc_eccentricity(max(r_gap_inner), min(r_gap_inner))
    ecc_outer = calc_eccentricity(max(r_gap_outer), min(r_gap_outer))

    return ecc_inner, ecc_outer


def calc_eccentricity(periapsis, apoapsis):
    return (periapsis - apoapsis) / (periapsis + apoapsis)


if __name__ == '__main__':
    sim_group, sim_id = 'frame_rotation', '1mj_e.00'
    outfile_idx = 10
    main(sim_group, sim_id, outfile_idx)

