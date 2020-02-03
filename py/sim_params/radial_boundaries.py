

class InvalidSimIdentifiersError(Exception):
    def __init__(self):
        print('Invalid simulation identifiers')


def r_max_2D(sim_group, sim_id):
    if sim_group in [
        'frame_rotation', '10000_orbits', '50000_orbits', 'migration'
    ]:
        return 5.0
    elif sim_group in [
        'first_tests', 'testing_cells_per_rH', 'testing_visc'
    ]:
        return 3.0
    else:
        # if sim_group or sim_id is not found, raise Error
        raise InvalidSimIdentifiersError


def r_max_1D(sim_group, sim_id):
    # TODO: generalize
    return 50.0


def r_min_1D(sim_group, sim_id):
    # TODO: generalize
    return 0.02


def r_min_2D(sim_group, sim_id):
    if sim_group in [
        'frame_rotation', 'testing_cells_per_rH', 'testing_visc',
        '10000_orbits', '50000_orbits', 'migration'
    ]:
        return 0.2
    elif sim_group in ['first_tests']:
        return 0.0
    else:
        # if sim_group or sim_id is not found, raise Error
        raise InvalidSimIdentifiersError


if __name__ == '__main__':
    # TODO: call functions based on argv
    pass

