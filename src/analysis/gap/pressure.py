import numpy as np


def main(r, Σ_1D):

    # TODO: generalize for different semi-major axes and aspect ratios
    G, M, a = 1, 1, 1
    H = lambda r: r
    # calculate Kepler frequency
    # Ω = lambda r, a: np.sqrt(G * M / r**2 * (2 / r - 1 / a))
    Ω = lambda r, a: np.sqrt(G * M / r**3)
    # calculate sound velocity
    c_s = H(r) * Ω(r, a)
    # calculate pressure
    P = c_s**2 * Σ_1D
    # return
    return P




