import numpy as np
from numpy import pi as π

import analysis.accretion.hill_radius


def f_red(r, r_H):
    if r / r_H < 0.45:
        return 2./3
    elif r / r_H < 0.9:
        return 2./3 * np.cos(π*(r/r_H - 0.45))**4
    else:
        return 0.00
