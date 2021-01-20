
import os

import numpy as np
from numpy import pi as π

import analysis
import config
from config import FARGO_DIR
import sim_params
from sim_params import general


def current_eccentricity(sim_group, sim_id, outfile_idx):
    out_file_path = os.path.join(
        FARGO_DIR, sim_group, sim_id, 'out/orbit1.dat'
    )
    with open(out_file_path) as fp:
        content = fp.readlines()
    ecc = float(content[outfile_idx].split('\t')[1])
    return ecc


def current_mass(sim_group, sim_id, iteration_step):
    out_file_path = os.path.join(
        FARGO_DIR, sim_group, sim_id, 'out/planet1.dat'
    )
    with open(out_file_path) as fp:
        content = fp.readlines()

    mass = float(content[iteration_step].split('\t')[5])
    return np.round(mass, 6)


def current_position_xy(sim_group, sim_id, iteration_step):
    # TODO: this leads to wrong results,
    #       instead use corrected polar coordinate position
    path_to_planet1_file = os.path.join(
        FARGO_DIR, sim_group, sim_id, f'out/planet1.dat'
    )

    with open(path_to_planet1_file) as fp:
        planet1_file = fp.readlines()

    relevant_row = planet1_file[iteration_step]

    x = np.array(float(relevant_row.split('\t')[1]))
    y = np.array(float(relevant_row.split('\t')[2]))

    return x, y


def current_position_rφ(sim_group, sim_id, iteration_step):
    x, y = current_position_xy(sim_group, sim_id, iteration_step)

    r = np.sqrt(x**2 + y**2)
    φ = np.arctan(y / x)

    # make sure all angles are between 0 and 2π
    if φ < 0:
        φ += 2*π
    elif φ > 2*π:
        φ -= 2*π
    # arctan leads to same result for angles in opposing quadrants, fix:
    if y > 0 and φ > π:
        φ -= π
    elif y < 0 and φ < π:
        φ -= π

    return r, φ


def current_semimajor_axis(sim_group, sim_id, outfile_idx):
    orbit1_file = os.path.join(FARGO_DIR, sim_group, sim_id, 'out/orbit1.dat')
    with open(orbit1_file) as fp:
        content = fp.readlines()

    return float(content[outfile_idx].split('\t')[2])


def initial_mass(sim_group, sim_id):

    if sim_group in ['50000_orbits']:
        initial_mass = float(sim_id.split('m')[0]) / 1000
        return initial_mass

    out_file_path = os.path.join(
        FARGO_DIR, sim_group, sim_id, 'out/planet1.dat'
    )
    with open(out_file_path) as fp:
        content = fp.readlines()
    taper = general.mass_taper_duration_out_file_idx(sim_group, sim_id)
    initial_mass = float(content[taper].split('\t')[5])
    return np.round(initial_mass, 6)


def initial_eccentricity(sim_group, sim_id):
    if sim_group == 'migration':
        return float('0' + sim_id.split('_')[1][1:])
    else:
        return float('0.' + sim_id.split('.')[-1])


def initial_semi_major_axis(sim_group, sim_id):
    return 1
    # TODO: generalize


def machida(sim_group, sim_id):
    if sim_group not in ['machida']:
        return 1.
    else:
        return float(sim_id.split('_')[-1])

def nr(sim_group, sim_id):
    if sim_group in ['frame_rotation']:
        return 1


def semi_major_axis(sim_group, sim_id):
    pass


def gas_disk_viscosity(sim_group, sim_id):
    if sim_group in [
        'frame_rotation', 'testing_cells_per_rH', 'testing_masses',
        '10000_orbits', 'flaring_idx', 'machida', 'sigma_slope'
    ]:
        return 1e-2
    elif sim_group in ['testing_visc']:
        if sim_id.startswith('vm2'):
            return 1e-2
        elif sim_id.startswith('vm3'):
            return 1e-3
        elif sim_id.startswith('vm4'):
            return 1e-4
        else:
            if sim_id.startswith('v'):
                return float('0.' + sim_id.split('.')[-1])
    elif sim_group in ['migration']:
        return 10**-float(sim_id.split('_')[2][1:])

