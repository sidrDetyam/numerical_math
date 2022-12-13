import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import math
from copy import deepcopy


def plot_surface(x, y, z, title=""):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    X, Y = np.meshgrid(x, y)
    z_ = np.linspace(0, 5, x.size * y.size)
    Z = np.reshape(z_, X.shape)
    for i in range(x.size):
        for j in range(y.size):
            Z[j, i] = z[i][j]

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('x')
    ax.set_ylabel('time')

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    mx = max([max(i) for i in z])
    mn = min([min(i) for i in z])

    ax.set_zlim(mn - abs(mn), mx + abs(mx))
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title(title)
    plt.show()


def get_grid(x0, x1, t1, h, tao):
    x = np.linspace(x0, x1, int((x1 - x0) / h))
    y = np.linspace(0, t1, int(t1 / tao))
    z = [[0 for i in range(y.size)] for j in range(x.size)]
    return x, y, z


def analytical(x0, x1, t1, h, tao, g, a):
    x, y, z = get_grid(x0, x1, t1, h, tao)
    for i, x_ in enumerate(x):
        for j, y_ in enumerate(y):
            z[i][j] = g(x_ - a * y_)

    return x, y, z


def three_layer_cross(x0, x1, t1, h, tao, g, a):
    x, y, z = get_grid(x0, x1, t1, h, tao)
    for i, x_ in enumerate(x):
        for j in range(2):
            z[i][j] = g(x_ - a * y[j])

    for j, y_ in enumerate(y):
        z[0][j] = g(x[0] - a * y[j])
        z[x.size - 1][j] = g(x[x.size - 1] - a * y[j])

    r = a * tao / h
    if abs(r) >= 1:
        raise ValueError

    for j in range(1, y.size - 1):
        for i in range(1, x.size - 1):
            z[i][j + 1] = z[i][j - 1] - r * (z[i + 1][j] - z[i - 1][j])

    return x, y, z


def 


def diff(z1, z2):
    if len(z1) != len(z2) or len(z1[0]) != len(z2[0]):
        raise ValueError
    d = deepcopy(z1)

    for i in range(len(z1)):
        for j in range(len(z1[0])):
            d[i][j] = abs(z1[i][j] - z2[i][j])
    return d


def l1_norm(z):
    norm = 0
    for i in range(len(z)):
        for j in range(len(z[0])):
            norm = max(norm, abs(z[i][j]))
    return norm


def fix_grid(x, y, z, h, tao):
    h_orig = x[1] - x[0]
    tao_orig = y[1] - y[0]
    if h_orig > h:
        return x, y, z

    x_, y_, z_ = get_grid(x[0], x[x.size - 1], y[y.size - 1], h, tao)
    for i, x0 in enumerate(x_):
        for j, y0 in enumerate(y_):
            z_[i][j] = z[int((x0 - x_[0]) / h_orig)][int(y0 / tao_orig)]
    return x_, y_, z_


def g1(x):
    if x < 1:
        return 0
    if x < 4:
        return math.sin(math.pi * (x - 1) / 3)
    return 0


def g2(x):
    if x < 0:
        return 5
    return 3


g = g1


x, y, z = analytical(0, 6, 5, 0.01, 0.01, g, 1)
plot_surface(x, y, z, "Аналитическое")

for h in np.linspace(0.5, 0.01, 8):
    x, y, z = analytical(0, 6, 5, h, h / 2, g, 1)
    _, _, z1 = three_layer_cross(0, 6, 5, h, h / 2, g, 1)
    xf, yf, zf = fix_grid(x, y, z1, 0.1, 0.1)
    _, _, z_diff = fix_grid(x, y, diff(z, z1), 0.1, 0.1)

    plot_surface(xf, yf, zf, f"h = {h}, погрешность = {l1_norm(z_diff)}")
    plot_surface(xf, yf, z_diff, f"h = {h}, погрешность = {l1_norm(z_diff)}")
