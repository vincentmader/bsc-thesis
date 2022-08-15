
import numpy as np

import analysis
import config
import sim_params


def main(r, Σ_2D, search_distance_in_rH, planet_m, planet_a, planet_e):

    M, m, a, e = 1, planet_m, planet_a, planet_e

    Nrad, Nsec = Σ_2D.shape
    r_min, r_max = r[0], r[-1]
    # r = lambda idx: r_min + (r_max - r_min) * idx / Nrad

    idx_by_r = lambda r: int((r - r_min) / (r_max - r_min) * Nrad)

    # create lists holding inner and outer boundary location for given φ index
    r_gap_inner, r_gap_outer = [], []
    # loop over all columns/azimuthal angles
    for φ_idx in range(Nsec):
        # reshape 2D Σ array, only look at 1D column at given azimuthal angle
        Σ_1D = np.array([row[φ_idx] for row in Σ_2D])

        # calculate pressure P as function of distance from center r
        P = analysis.gap.pressure(r, Σ_1D)
        # calculate logarithmic derivative of pressure
        gradLogP = grad(np.log(r), np.log(P))

        # convert search_distance in Hill radii to code units
        search_distance = search_distance_in_rH * analysis.accretion.hill_radius(
            M, m, a, e
        )
        if search_distance > a:
            print('search_distance too large!')

        # look for gap boundaries close to planet, define range
        lower_search_lim = idx_by_r(a - search_distance)
        planet_loc_idx = idx_by_r(a)
        upper_search_lim = idx_by_r(a + search_distance)
#        print(lower_search_lim, upper_search_lim)
        # calculate indices of inner and outer boundary of gap
        gap_min_idx = np.argmin(gradLogP[lower_search_lim:planet_loc_idx]) + lower_search_lim
        gap_max_idx = np.argmax(gradLogP[planet_loc_idx:upper_search_lim]) + planet_loc_idx

        # convert to radial distance in code units
        r_gap_min = r[gap_min_idx]
        r_gap_max = r[gap_max_idx]
        # append to list
        r_gap_inner.append(r_gap_min)
        r_gap_outer.append(r_gap_max)

    return r_gap_inner, r_gap_outer


def grad(x, y):  # len(grad(x, y)) = len(x) - 1 = len(y) - 1   !!!
    Δx = np.diff(x)
    Δy = np.diff(y)
    return Δy / Δx
