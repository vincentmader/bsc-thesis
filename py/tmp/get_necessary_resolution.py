
import numpy as np

from get_hill_radius import main as get_hill_radius


def main(M, m, a, e, rH_cells, r_min, r_max):
    """
    calculate needed values for setup parameters Nrad and Nsec

    param M: mass of the body that is being orbited by the body with mass m
    param m: mass of the body whose Hill radius is to be determined
    param a: semi-major axis of the smaller body's orbit
    param e: eccentricity of the smaller body's orbit
    param rH_cells: number of cells in Hill radius of planet
    """


    rH = get_hill_radius(M, m, a, e)
    print(f'{rH = } supposed to correspond to {rH_cells} cells')

    cell_size_in_r = rH / rH_cells
    print(f'  =>  {cell_size_in_r = }')

    cells_between_star_and_planet = a / cell_size_in_r
    print(f'  =>  {cells_between_star_and_planet = }')

    res_r = (r_max - r_min) / a * cells_between_star_and_planet
    print(f'  =>  {res_r = }')

    res_φ = optimal_Nsec(r_min, r_max, res_r)  # 2 * np.pi * res_r
    print(f'  => {res_φ = }')


def area_of_ring_at_radius_1(r_min, r_max, N_rad):

    # ring width
    δr = (r_max - r_min) / N_rad
    # radial boundaries of ring
    r_1, r_2 = 1, 1 + δr

    return np.pi * (r_2**2 - r_1**2)


def optimal_Nsec(r_min, r_max, N_rad):

    A = area_of_ring_at_radius_1(r_min, r_max, N_rad)
    δr = (r_max - r_min) / N_rad

    return A / δr**2


def testing_cells_per_rH():
    M = 1
    m = 1e-3  # 1 M_J
    a = 1
    e = 0
    r_min = .2
    r_max = 5

    print(f'{M = }, {m = }, {a = }, {e = }, {r_min = }, {r_max = }')

    for rH_cells in [2.5, 5, 10]:
        print(f'\n{rH_cells = }')
        main(M, m, a, e, rH_cells, r_min, r_max)


if __name__ == '__main__':
    testing_cells_per_rH()
