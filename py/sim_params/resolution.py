
def get_1D_res(sim_dir, sim_id):
    pass
    # TODO: return r resolution for 1D output files


def get_2D_res(sim_dir, sim_id):
    """return tuple (res_r, res_φ)"""

    #RES_r, RES_φ = 101, 634  # for cprH = 2.5
    #RES_r, RES_φ = 202, 1269  # for cprH = 5
    #RES_r, RES_φ = 404, 2537  # for cprH = 10
    #RES_r, RES_φ = 552, 1104  # for first_tests/rH5...
    #RES_r, RES_φ = 300, 600  # for first_tests/ecc...

    if sim_dir == 'testing_cells_per_rH':
        if sim_id.startswith('2.5'):
            return (101, 634)
        elif sim_id.startswith('5'):
            return (202, 1269)
        elif sim_id.startswith('7.5'):
            return (303, 1902)
        elif sim_id.startswith('10'):
            return (404, 2537)

    elif sim_dir in ['frame_rotation', 'testing_visc']:
        if sim_id in ['1.0mj_e.250', '1.0mj_e.275', '1.0mj_e.300']:
            return (404, 909)
        elif 'unp' in sim_id:
            return (404, 404)
        else:
            return (202, 456)

    elif sim_dir in ['testing_masses']:
        return (202, 1269)

    elif sim_dir in ['migration']:
        if sim_id == 'unp':
            return (404, 404)
        else:
            return (202, 456)

    elif sim_dir in ['50000_orbits']:
        if sim_id in ['unp']:
            return (404, 202)
        else:
            return (202, 456)

    # fallback on resolution calculated for 5 cells in Hill radius (1 MJ)
    else:
        return (202, 456)


if __name__ == '__main__':
    pass
    # TODO: call either 2D or 1D

