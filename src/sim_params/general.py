
import numpy as np


def accretion_parameter(sim_group, sim_id):
    pass


def accretion_start_time_in_orbits(sim_group, sim_id):
    if sim_group in ['10000_orbits', '50000_orbits']:
        return 1000
    elif sim_group in ['frame_rotation', 'machida', 'testing_visc', 'flaring_idx', 'aspect_ratio']:
        return 500
    elif sim_group in ['testing_cells_per_rH']:
        return 10


def accretion_start_time_out_file_idx(sim_group, sim_id):
    accretion_start_time = accretion_start_time_in_orbits(sim_group, sim_id)
    iterations_per_output = nr_of_iterations_per_output(sim_group, sim_id)

    return int(accretion_start_time / iterations_per_output)


def aspect_ratio(sim_group, sim_id):
    if sim_group not in ['aspect_ratio']:
        return 0.05
    else:
        return float(sim_id.split('_')[-1])


def flaring_idx(sim_group, sim_id):
    if sim_group not in ['flaring_idx']:
        return 0.
    else:
        return float(sim_id.split('_')[-1])


def mass_taper_duration_in_orbits(sim_group, sim_id):
    """return duration of mass taper in orbits"""

    if sim_group in ['testing_cells_per_rH']:
        return 5  # 3  # sure ?
    elif sim_group in ['testing_masses']:
        return 20  # 10  # sure ?
    elif sim_group in ['10000_orbits', '50000_orbits']:
        return 200  # 4
#    elif sim_group in ['frame_rotation', 'testing_visc', 'machida', 'flaring_idx', 'aspect_ratio', 'migration', 'sigma_slope']:
#        return 50  # 1  # = 50 / 50 = taper orbits / nr of orbits for each out file
    else:
        return 50


def mass_taper_duration_out_file_idx(sim_group, sim_id):

    taper = mass_taper_duration_in_orbits(sim_group, sim_id)
    iterations_per_output = nr_of_iterations_per_output(sim_group, sim_id)

    return int(taper / iterations_per_output)


def nr_of_iterations(sim_group, sim_id):
    if sim_group in ['testing_cells_per_rH']:
        return 500
    elif sim_group in ['10000_orbits']:
        return 10000
    elif sim_group in ['50000_orbits']:
        return 50000
    elif sim_group in [
        'frame_rotation', 'testing_visc', 'machida', 'sigma_slope',
        'flaring_idx', 'aspect_ratio',
    ]:
        return 2500
    elif sim_group == 'migration':
        return 2000
    elif sim_group == 'presentation_500_orbits':
        return 500
    elif sim_group == 'presentation_5000_orbits':
        return 5000
    # TODO: generalize


def nr_of_iterations_per_output(sim_group, sim_id):
    if sim_group in ['50000_orbits']:
        return 250
    elif sim_group in ['presentation_500_orbits']:
        return 1
    elif sim_group in ['presentation_5000_orbits']:
        return 10
    else:
        return 50
    # TODO: generalize


def nr_of_outputs(sim_group, sim_id):

    iterations = nr_of_iterations(sim_group, sim_id)
    iterations_per_output = nr_of_iterations_per_output(sim_group, sim_id)

    return int(iterations / iterations_per_output)


def sigma_slope(sim_group, sim_id):

    if sim_group in ['sigma_slope']:
        return float(sim_id.split('_')[-1])
    else:
        return 1


def time_between_iterations(sim_group, sim_id):
    return 2 * np.pi


if __name__ == '__main__':
    pass
    # TODO: call functions based on argv

