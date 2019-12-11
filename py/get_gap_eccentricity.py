#!/usr/local/bin/python3
# -*- coding: utf8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np


simulation_name = 'frame_rotation'
simulation_dir = f'../fargo2d1d/{simulation_name}/'
figure_dir = f'../figures/{simulation_name}/'

Nrad, Nsec = 202, 456
r_min, r_max = 0.2, 3.0  # change to 5.0

G, M, a = 1, 1, 1
H = lambda r: r
#Ω = lambda r, a: np.sqrt(G * M / r**2 * (2 / r - 1 / a))
Ω = lambda r, a: np.sqrt(G * M / r**3)
r_by_idx = lambda idx: r_min + (r_max - r_min) * idx / Nrad
idx_by_r = lambda r: int((r - r_min) / (r_max - r_min) * Nrad)

idxs = np.arange(0, Nrad, 1)
r = r_by_idx(idxs)  # radial distance in code units (1 c.u. = 5.2 AU)

c_s = H(r) * Ω(r, a)

plt.figure()
plt.plot(r, c_s)
plt.xlabel(r'radial distance $r$ [code units]')
plt.ylabel(r'acoustic velocity $c_s$ [code units]')
plt.xlim(r[0], r[-1])
plt.ylim(min(c_s), max(c_s))
plt.savefig('../figures/acoustic_velocity.pdf')
plt.clf()


def get_gap_limits(Σ):

    # create dictionaries, here pairs of "angle: r_gap_limit" will be saved
    r_gap_inner, r_gap_outer = {}, {}
    # loop over all columns/azimuthal angles
    for φ_idx in range(Nsec):
        # reshape 2D Σ array, only look at 1D column at given azimuthal angle
        Σ_1D = np.array([row[φ_idx] for row in Σ])

        # calculate pressure P as function of distance from center r
        P = get_P(Σ_1D)
        # calculate logarithmic derivative of pressure 
        gradLogP = grad(np.log(r), np.log(P))

        # plot gradLogP for debugging
        # TODO: remove when not needed anymore
        #plot_gradLogP(φ_idx, gradLogP)

        # look for gap boundaries close to planet, define range
        lower_search_lim = idx_by_r(0.7)
        planet_loc_idx = idx_by_r(1)
        upper_search_lim = idx_by_r(1.3)
        # calculate indices of inner and outer boundary of gap
        gap_min_idx = np.argmin(gradLogP[lower_search_lim:planet_loc_idx]) + lower_search_lim
        gap_max_idx = np.argmax(gradLogP[planet_loc_idx:upper_search_lim]) + planet_loc_idx

        # convert to radial distance in code units
        r_gap_min = r_by_idx(gap_min_idx)
        r_gap_max = r_by_idx(gap_max_idx)

        r_gap_inner[φ_idx], r_gap_outer[φ_idx] = r_gap_min, r_gap_max

    return r_gap_inner, r_gap_outer


def get_gradLogP(P):   # also function of r?
    pass


def get_P(Σ_1D):
    # calculate pressure
    P = c_s**2 * Σ_1D
    # return
    return P


def plot_gradLogP(φ_idx, gradLogP):

    plt.plot(r[:-1], gradLogP)

    plt.savefig(f'{figure_dir}{simulation_id}/pressure/{φ_idx}.pdf')
    plt.clf()


def plot_gap_limits_vs_angle(r_gap_inner, r_gap_outer):

    φ = list(r_gap_inner.keys())
    φ = np.array(φ) / len(φ) * 360

    r_gap_inner = list(r_gap_inner.values())
    r_gap_outer = list(r_gap_outer.values())

    plt.plot(φ, r_gap_inner, label='inner gap limit')
    plt.plot(φ, r_gap_outer, label='outer gap limit')

    plt.title('gap limits determined from logarithmic pressure gradient')
    plt.xlim(0, 360)
    plt.ylim(r_min, r_max)
    plt.xlabel(r'azimuthal angle $\varphi$ [deg]')
    plt.ylabel(r'radial distance r [code units]')
    plt.legend(loc='upper right')

    plt.savefig(f'{figure_dir}{simulation_id}/gap_profile.pdf')
    plt.clf()


def grad(x, y):  # len(grad(x, y)) = len(x) - 1 = len(y) - 1   !!!
    Δx = np.diff(x)
    Δy = np.diff(y)
    return Δy / Δx


def get_gap_eccentricities(Σ):
    r_gap_inner, r_gap_outer = get_gap_limits(Σ)
    plot_gap_limits_vs_angle(r_gap_inner, r_gap_outer)
    #print('\n', r_gap_inner, '\n')

    # calculate eccentricity for outer and inner gap limit each
    e_inner = 1
    e_outer = 1
    # return 
    return e_inner, e_outer
    # TODO:
    #   - calculate eccentricities from inner and outer boundaries 
    #   - also do this for average/median gap position


if __name__ == '__main__':

    # loop over all simulations in simulation_dir
    for simulation_id in sorted(os.listdir(simulation_dir)):
        if simulation_id == '.DS_Store':
            continue

        # loop over all 2D gas density files for given simulation
        out_dir = os.path.join(simulation_dir, simulation_id, 'out')
        for out_file in sorted(os.listdir(out_dir)):

            # only interested in 2D gas density data for last time step
            if not out_file.startswith('gasdens'):
                continue
            if out_file.startswith('gasdens1D'):
                continue
            elif out_file.startswith('gasdens.ascii'):
                continue
            if not os.path.exists(os.path.join(out_dir, out_file)):
                continue
            if not out_file.endswith('50.dat'):
                continue
            #if not out_dir.endswith('0.dat'):    # can be deleted later, fix init a ?
            #    continue

            file_path = os.path.join(out_dir, out_file)

            # load 2D density from simulation output file
            Σ = np.fromfile(file_path).reshape(Nrad, Nsec)
            # calculate eccentricity for 2D gas density files
            e = get_gap_eccentricities(Σ)
            #print(e)


#def get_gap_eccentricity(Σ, simulation_id):
#
#    #for Σ_1D in np.array([[row[i] for row in Σ] for i in range(Nsec)])
#
#    gap_start_positions, gap_end_positions = [], []
#    averageP = np.array([0.] * Nrad)
#
#    cols = np.array([[row[i] for row in Σ] for i in range(Nsec)])  # quicker with np?
#    for col in cols:
#
#        P = c_s**2 * col
#        logGradientP = (np.log(P[1:]) - np.log(P[:-1])) / (r[1:] - r[:-1])
#        print(logGradientP[129])
#
#        gap_start = r_by_idx(np.argmin(logGradientP))
#        gap_end = r_by_idx(np.argmax(logGradientP))
#        gap_start_positions.append(gap_start)
#        gap_end_positions.append(gap_end)
#
#        averageP += P
#
#        #plt.plot(r[:-1], logGradientP)
#        #plt.savefig(f'{figure_dir}/{simulation_id}/{idx}.png')
#        #plt.clf()
#        #input()
#        #print(P[202 // 3])
#
#    averageP /= Nsec
#    logGradAverageP = (np.log(P[1:]) - np.log(P[:-1])) / (r[1:] - r[:-1])
#
#    #print(gap_start_positions)
#    plt.plot(gap_start_positions)
#    #plt.plot(gap_end_positions)
#    plt.savefig(f'../figures/testing_masses/{simulation_id}/gap_eccentricity/gap.pdf')
#    plt.clf()
#
#    plt.plot(r, averageP)
#    plt.savefig(f'../figures/testing_masses/{simulation_id}/avgP.pdf')
#    plt.clf()
#
#    plt.plot(r[:-1], logGradAverageP)
#    plt.savefig(f'../figures/testing_masses/{simulation_id}/logGradAvgP.pdf')
#    plt.clf()
#
#    return 1
#
#
#
#
#
#
#if __name__ == '__main__':
#
#    # loop over all simulations in simulation_dir
#    for simulation_id in sorted(os.listdir(simulation_dir)):
#        if simulation_id == '.DS_Store':
#            continue
#
#        # loop over all 2D gas density files for given simulation
#        out_dir = os.path.join(simulation_dir, simulation_id, 'out')
#        for out_file in sorted(os.listdir(out_dir)):
#
#            # only interested in 2D gas density data for last time step
#            if not out_file.startswith('gasdens'):
#                continue
#            if out_file.startswith('gasdens1D'):
#                continue
#            elif out_file.startswith('gasdens.ascii'):
#                continue
#            if not os.path.exists(os.path.join(out_dir, out_file)):
#                continue
#            if not out_file.endswith('50.dat'):
#                continue
#            if out_file.endswith('0'):    # can be deleted later
#                continue
#
#            file_path = os.path.join(out_dir, out_file)
#            print(file_path)
#            Σ = np.fromfile(file_path).reshape(Nrad, Nsec)
#
#            # calculate eccentricity for 2D gas density files
#            e = get_gap_eccentricity(Σ, simulation_id)
#
