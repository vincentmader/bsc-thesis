
import numpy as np


x = lambda r, φ: r * np.cos(φ)
y = lambda r, φ: r * np.sin(φ)

def xy(r, φ):

    a = x(r, φ)
    b = y(r, φ)

    return a, b


print(xy(2, 0))
print(xy(2, np.pi / 10))

print(xy(2.5, 0))
print(xy(2.5, np.pi / 10))

