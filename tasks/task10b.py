import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import math
from copy import deepcopy

def _plot_surf(x, y, z, fig, ind, cnt, inf = 1000):
    ax = fig.add_subplot(1, cnt, ind, projection="3d")

    X, Y = np.meshgrid(x, y)
    z_ = np.linspace(0, 5, x.size * y.size)
    Z = np.reshape(z_, X.shape)
    for i in range(x.size):
        for j in range(y.size):
            Z[j, i] = z[i][j] if abs(z[i][j]) < inf else float('nan')

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('x')
    ax.set_ylabel('time')

    surf = ax.plot_surface(X, Y, Z, cmap=cm.plasma,
                           linewidth=0, antialiased=True)

    mx = max(map(max, Z))
    mn = min(map(min, Z))
    mx = mx + abs(mx) if abs(mx) < inf else 10
    mn = mn - abs(mn) if abs(mn) < inf else -10
    if mn == -10:
        pass

    ax.set_zlim(mn, mx)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.2f}')
    fig.colorbar(surf, shrink=0.4, aspect=10)


def plot_surfaces(surfs, title=""):
    fig = plt.figure(figsize=plt.figaspect(1 / len(surfs)))

    for i, s in enumerate(surfs):
        x, y, z = s
        _plot_surf(x, y, z, fig, i+1, len(surfs))
    plt.title(title)
    plt.show()


def get_grid(x0, x1, t1, h, tao):
    x = np.linspace(x0, x1, int((x1 - x0) / h))
    y = np.linspace(0, t1, int(t1 / tao))
    z = [[0 for i in range(y.size)] for j in range(x.size)]
    return x, y, z


def three_layer_cross(x0, x1, t1, h, tao, g, l):
    x, y, z = get_grid(x0, x1, t1, h, tao)
    for i, x_ in enumerate(x):
        for j in range(2):
            z[i][j] = g(x_)

    for j, y_ in enumerate(y):
        z[0][j] = l(y_)

    for j in range(1, y.size - 1):
        for i in range(1, x.size - 1):
            # r = abs(z[i][j]) * tao / h
            # if r>1:
            #     raise ValueError
            z[i][j + 1] = z[i][j - 1] - tao/h * (z[i + 1][j]**2 - z[i - 1][j]**2)/2

    return x, y, z


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


def fix_grid(x, y, z, h, tao, forced=False):
    h_orig = x[1] - x[0]
    tao_orig = y[1] - y[0]
    if h_orig > h and not forced:
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

l1 = lambda t: 0

def g2(x):
    if x < 3:
        return 5
    return 0.5

l2 = lambda t: 5


g3 = lambda x: math.sin(math.pi * (x-1)/3)
g4 = lambda x: math.sin(math.pi * (x-1)/3) / (x+10) * 2

g = g1
l = l1
strategy = three_layer_cross
x0 = 0
x1 = 6.5
t1 = 1
demo_h = 0.05


def time_slice(z):
    t_slice = len(z[0])//2
    return [z[i][t_slice] for i in range(len(z))]

slices = []
x = None

def draw_functions(x, name, functions):
    for function, style in functions:
        y = [function[i] for i in range(x.size)]
        plt.plot(x, y, style)
    plt.title(name)
    plt.grid()
    plt.draw()
    plt.show()


for h in np.linspace(0.5, 0.005, 8):
    tao = h * 0.98
    xs, ys, zs = strategy(x0, x1, t1, h, tao, g, l)
    xsf, ysf, zsf = fix_grid(xs, ys, zs, demo_h, demo_h)
    if h==0.005:
        slices.append([time_slice(fix_grid(xsf, ysf, zsf, demo_h, demo_h, True)[2]), "-g"])
    x = xsf
    plot_surfaces([(xsf, ysf, zsf)],
                  f"h = {h}, tao = {tao}")

draw_functions(x, f"t = {t1/2}", slices)
