
def main(M=1, m=1e-3, a=1, e=0):
    """
    calculate the Hill radius of a body based on the following input params:

    param M: mass of the body that is being orbited by the body with mass m
    param m: mass of the body whose Hill radius is to be determined
    param a: semi-major axis of the smaller body's orbit
    param e: eccentricity of the smaller body's orbit
    """

    r_H = a * (1 - e) * (m / (3 * M)) ** (1 / 3)
    return r_H


if __name__ == '__main__':
    print('M = 1, m = 1e-3, a = 1, e = 0')
    print('rH =', main())

