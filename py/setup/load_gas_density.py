
import numpy as np

import setup
from sim_params.resolution import get_2D_res


def sigma_1D(sim_group, sim_id, outfile_idx):

    path_to_1D_data = setup.outfile_paths.sigma_1D(sim_group, sim_id, outfile_idx)
    Σ = np.fromfile(path_to_1D_data)

    return Σ


def sigma_1D_ascii(sim_group, sim_id, outfile_idx):

    path_to_1D_data = setup.outfile_paths.sigma_1D_ascii(sim_group, sim_id, outfile_idx)
    with open(path_to_1D_data) as fp:
        Σ = fp.readlines()

    return Σ


def sigma_2D(sim_group, sim_id, outfile_idx):

    res_r, res_φ = get_2D_res(sim_group, sim_id)

    path_to_2D_data = setup.outfile_paths.sigma_2D(sim_group, sim_id, outfile_idx)
    Σ = np.fromfile(path_to_2D_data).reshape(res_r, res_φ)

    return Σ

