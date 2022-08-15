import numpy as np

import setup
from setup import get_2D_res


def v_rad(sim_group, sim_id, outfile_idx):

    res_r, res_φ = get_2D_res(sim_group, sim_id)

    path_to_2D_data = setup.outfile_paths.v_rad(sim_group, sim_id, outfile_idx)
    v = np.fromfile(path_to_2D_data).reshape(res_r, res_φ)

    return v


def v_theta(sim_group, sim_id, outfile_idx):

    res_r, res_φ = get_2D_res(sim_group, sim_id)

    path_to_2D_data = setup.outfile_paths.v_theta(sim_group, sim_id, outfile_idx)
    v = np.fromfile(path_to_2D_data).reshape(res_r, res_φ)

    return v

