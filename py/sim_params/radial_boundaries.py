

class InvalidSimIdentifiersError(Exception):
    def __init__(self):
        print('Invalid simulation identifiers')


def r_max_2D(sim_group, sim_id):
    if sim_group in [
        'frame_rotation', '10000_orbits', '50000_orbits', 'migration',
        'presentation'
    ]:
        return 5.0
    elif sim_group in [
        'first_tests', 'testing_cells_per_rH', 'testing_visc'
    ]:
        return 3.0
    else:
        # print(f'fell back on resolution 5.0 for {sim_group} {sim_id}')
        return 5.0
        # # if sim_group or sim_id is not found, raise Error
        # raise InvalidSimIdentifiersError


def r_max_1D(sim_group, sim_id):
    # TODO: generalize
    return 50.0


def r_min_1D(sim_group, sim_id):
    # TODO: generalize
    return 0.02


def r_min_2D(sim_group, sim_id):
    if sim_group in [
        'frame_rotation', 'testing_cells_per_rH', 'testing_visc',
        '10000_orbits', '50000_orbits', 'migration', 'presentation'
    ]:
        return 0.2
    elif sim_group in ['first_tests']:
        return 0.0
    else:
        # print(f'fell back on resolution 0.2 for {sim_group} {sim_id}')
        return 0.2
        # # if sim_group or sim_id is not found, raise Error
        # raise InvalidSimIdentifiersError


if __name__ == '__main__':
    # TODO: call functions based on argv
    pass

