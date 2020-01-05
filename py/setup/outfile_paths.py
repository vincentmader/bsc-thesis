

import os

import config
from config import FARGO_DIR


def sigma_1D(sim_group, sim_id, outfile_idx):
    return os.path.join(
        FARGO_DIR, sim_group, sim_id, f'out/gasdens1D{outfile_idx}.dat'
    )


def sigma_1D_ascii(sim_group, sim_id, outfile_idx):
    return os.path.join(
        FARGO_DIR, sim_group, sim_id, f'out/gasdens.ascii_rad.{outfile_idx}.dat'
    )


def sigma_2D(sim_group, sim_id, outfile_idx):
    return os.path.join(
        FARGO_DIR, sim_group, sim_id, f'out/gasdens{outfile_idx}.dat'
    )

