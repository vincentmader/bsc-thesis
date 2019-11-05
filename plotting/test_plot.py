
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os


SIMULATION_ID = 'template2'
RES_r = 300
RES_φ = 600

r = np.linspace(0, RES_r - 1, RES_r)
φ = np.linspace(0, RES_φ - 1, RES_φ)

for i in range(1000):

    file_path = f'../fargo2d1d/out/{SIMULATION_ID}/gasdens{i}.dat'

    try:
        σ = np.log10(np.fromfile(f'{file_path}').reshape(RES_r, RES_φ))
    except FileNotFoundError:
        continue

    print(f'plotting data from file {file_path}')
    fig = plt.figure()

    ax = plt.subplot(211, projection='polar')
    plt.pcolormesh(σ)
    plt.xticks([])
    plt.yticks([])

    ax2 = plt.subplot(212)
    plt.imshow(σ, origin='lower', aspect='auto')
    plt.colorbar()

    plt.savefig(f'../figures/testing/{SIMULATION_ID}/plot{i}.png')
    plt.clf()
    plt.close()

