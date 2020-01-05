
import os
import sys

import config
from config import FIGURE_DIR


def main(sim_group, sim_id):

    print('\ngif for', sim_group, sim_id)

    # define string holding file paths to all pngs, separated by a whitespace
    png_file_paths_separated_by_space = ''
    # define location of collage png files
    png_file_dir = os.path.join(FIGURE_DIR, sim_group, sim_id, 'all_collages')
    # define list with names of all collage png file names
    all_png_file_names = sorted(os.listdir(png_file_dir))
    # check whether there are any png collage files, return if not
    if not all_png_file_names:
        return

    # loop over png collage files for all time steps
    for png_file in all_png_file_names:
        # make sure all non-png files are ignored
        if not png_file.endswith('.png'):
            continue

        # define absolute file path of png file
        abs_fp = os.path.join(
            FIGURE_DIR, sim_group, sim_id, 'all_collages', png_file
        )
        # append to string to be used in gif creation command
        png_file_paths_separated_by_space += f'"{abs_fp}" '

    # define location of output gif
    gif_loc = os.path.join(FIGURE_DIR, sim_group, sim_id, 'collage.gif')
    # execute command for gif creation
    os.system(f'convert {png_file_paths_separated_by_space}"{gif_loc}"')


if __name__ == '__main__':
    sim_group, sim_id = sys.argv[1], sys.argv[2]
    main(sim_group, sim_id)

