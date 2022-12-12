import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import math


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

def fun(x, y):
    return math.sin(x)

N = 100

x = np.linspace(0, 5, N)  # [0, 2,..,10] : 6 distinct values
y = np.linspace(0, 5, N)  # [0, 5,..,20] : 5 distinct values
z = np.linspace(0, 5, N*N)  # 6 * 5 = 30 values, 1 for each possible combination of (x,y)

X, Y = np.meshgrid(x, y)
Z = np.reshape(z, X.shape)  # Z.shape must be equal to X.shape = Y.shape
for i, x0 in enumerate(X[0]):
    for j, y0 in enumerate(Y[0]):
        Z[j, i] = 3-x0

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-7.01, 7.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()