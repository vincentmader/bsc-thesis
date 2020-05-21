import os

import numpy as np

import config
from config import FARGO_DIR
import sim_params


def main(sim_group, sim_id, outfile_idx):
    if sim_group not in ['frame_rotation', '50000_orbits']:
        raise Exception(f'no sigma unperturbed simulation for {sim_group}')

    if sim_group in ['frame_rotation', '50000_orbits']:

        unp_file_loc = os.path.join(
            FARGO_DIR, sim_group, 'unp', 'out',
            f'gasdens.ascii_rad.{outfile_idx}.dat'
        )
        with open(unp_file_loc) as fp:
            file_content = fp.readlines()
        # bring into 1D form
        Σs = [float(row.split(' ')[1]) for row in file_content]

        # check if resolutions are the same
        res = sim_params.resolution.get_2D_res(sim_group, sim_id)
        res_unp = sim_params.resolution.get_2D_res(sim_group, 'unp')

        if res[0] != res_unp[0]:
            conversion_factor = res_unp[0] / res[0]

            if conversion_factor == 2:
                new_Σs = []
                for idx, item in enumerate(Σs):
                    if idx % 2 == 0:
                        new_Σs.append(
                            (Σs[idx] + Σs[idx + 1]) / 2
                        )
            else:
                # print(Σs)
                # new_Σs = [row[0] for row in Σs]
                # new_Σs = Σs
                raise Exception(
                    'oh no, sigma unp and sigma have different\
                    resolutions and they are not multiples of 2'
                )

        else:
            new_Σs = Σs

    return np.array(new_Σs)
