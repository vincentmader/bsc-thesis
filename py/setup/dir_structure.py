
import os

from config import FIGURE_DIR


def create_sim_group_dir(sim_group):
    # create needed sim_group directory structure in figures dir
    if sim_group not in os.listdir(FIGURE_DIR):
        sim_group_fig_dir = os.path.join(FIGURE_DIR, sim_group)
        os.mkdir(sim_group_fig_dir)


def create_sim_id_dir(sim_group, sim_id):
    # create needed sim_id directory structure in figures dir
    if sim_id not in os.listdir(os.path.join(FIGURE_DIR, sim_group)):
        sim_id_fig_dir = os.path.join(FIGURE_DIR, sim_group, sim_id)
        os.mkdir(sim_id_fig_dir)

