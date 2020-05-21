from scipy.integrate import quad


def main(r_min, r_max, sigma_0, sigma_slope):

    sigma = lambda r: sigma_0 * r ** -sigma_slope

    disk_mass = quad(sigma, r_min, r_max)[0] * 2 * 3.14

    return disk_mass


if __name__ == '__main__':
    print(main(0.02, 50.0, 0.0003, 1.0))

