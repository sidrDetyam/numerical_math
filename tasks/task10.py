import math
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator


def _plot_surf(x, y, z, fig, ind, cnt, inf=1000):
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


def plot_surfaces(surfs, title="", inf=1000):
    fig = plt.figure(figsize=plt.figaspect(1 / len(surfs)))

    for i, s in enumerate(surfs):
        x, y, z = s
        _plot_surf(x, y, z, fig, i + 1, len(surfs), inf)
    plt.title(title)
    plt.show()


def get_grid(x0, x1, t1, n, k):
    x = np.linspace(x0, x1, n)
    y = np.linspace(0, t1, k)
    z = [[0] * k for _ in range(n)]
    return x, y, z


def analytical(x0, x1, t1, n, k, g, a):
    x, y, z = get_grid(x0, x1, t1, n, k)
    for i, x_ in enumerate(x):
        for j, y_ in enumerate(y):
            z[i][j] = g(x_ - a * y_)

    return x, y, z


def three_layer_cross(x0, x1, t1, n, k, g, a):
    x, y, z = get_grid(x0, x1, t1, n, k)
    for i, x_ in enumerate(x):
        for j in range(2):
            z[i][j] = g(x_ - a * y[j])

    for j, y_ in enumerate(y):
        z[0][j] = g(x[0] - a * y[j])
        z[x.size - 1][j] = g(x[x.size - 1] - a * y[j])

    h = (x1 - x0) / n
    tao = t1 / k
    r = a * tao / h
    if abs(r) >= 1:
        raise ValueError

    for j in range(1, y.size - 1):
        for i in range(1, x.size - 1):
            z[i][j + 1] = z[i][j - 1] - r * (z[i + 1][j] - z[i - 1][j])

    return x, y, z


def implicit_central(x0, x1, t1, n, k, g, a):
    x, y, z = get_grid(x0, x1, t1, n, k)
    for i, x_ in enumerate(x):
        z[i][0] = g(x_ - a * y[0])
    alfa = [0] * x.size
    beta = [0] * x.size
    h = (x1 - x0) / n
    tao = t1 / k
    r = a * tao / h

    for j in range(1, y.size):
        alfa[0] = -r / 2
        beta[0] = z[0][j - 1] - g(x[0] - h - a * y[j])
        for i in range(1, x.size):
            alfa[i] = r / 2 / (-1 + (r / 2) * alfa[i - 1])
            beta[i] = (-z[i][j - 1] - (r / 2) * beta[i - 1]) / (-1 + (r / 2) * alfa[i - 1])
        # i = x.size - 1
        # beta[i] = (-(z[i][j - 1] - g(x[0]+h*i - a*y[j])) - (r / 2) * beta[i - 1]) / (-1 + (r / 2) * alfa[i - 1])

        z[x.size - 1][j] = beta[-1]
        for i in range(x.size - 2, -1, -1):
            z[i][j] = alfa[i] * z[i + 1][j] + beta[i]

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
    return max(map(max, z))


def fix_grid(x, y, z, n, k, forced=False):
    h_orig = x[1] - x[0]
    tao_orig = y[1] - y[0]
    h = (x[-1] - x[0]) / n
    if h_orig > h and not forced:
        return x, y, z

    x_, y_, z_ = get_grid(x[0], x[x.size - 1], y[y.size - 1], n, k)
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
        return 2
    return 1


g3 = lambda x: math.sin(math.pi * (x - 1) / 3)
g4 = lambda x: math.sin(math.pi * (x - 1) / 3) / (x + 10) * 2


def three_layer_cross_not_linear(x0, x1, t1, n, k, g, l, r):
    x, y, z = get_grid(x0, x1, t1, n, k)
    for i, x_ in enumerate(x):
        for j in range(2):
            z[i][j] = g(x_)

    for j, y_ in enumerate(y):
        z[0][j] = l(y_)
        z[x.size-1][j] = r(y_)

    h = (x1 - x0) / n
    tao = t1 / k
    for j in range(1, y.size - 1):
        for i in range(1, x.size - 1):
            try:
                z[i][j + 1] = z[i][j - 1] - tao / h * (z[i + 1][j] ** 2 - z[i - 1][j] ** 2) / 2
            except Exception:
                z[i][j + 1] = float("nan")

    return x, y, z


# def implicit_non_linear(x0, x1, t1, n, k, g, l):
#     x, y, z = get_grid(x0, x1, t1, n, k)
#     for i, x_ in enumerate(x):
#         z[i][0] = g(x_)
#     alfa = [0] * x.size
#     beta = [0] * x.size
#     h = (x1 - x0) / n
#     tao = t1 / k
#
#     for j in range(1, y.size):
#         uu = [z[i][j-1] for i in range(x.size)]
#
#         alfa[0] = -r / 2
#         beta[0] = z[0][j - 1] - g(x[0] - h - a * y[j])
#         for i in range(1, x.size):
#             alfa[i] = r / 2 / (-1 + (r / 2) * alfa[i - 1])
#             beta[i] = (-z[i][j - 1] - (r / 2) * beta[i - 1]) / (-1 + (r / 2) * alfa[i - 1])
#         # i = x.size - 1
#         # beta[i] = (-(z[i][j - 1] - g(x[0]+h*i - a*y[j])) - (r / 2) * beta[i - 1]) / (-1 + (r / 2) * alfa[i - 1])
#
#         z[x.size - 1][j] = beta[-1]
#         for i in range(x.size - 2, -1, -1):
#             z[i][j] = alfa[i] * z[i + 1][j] + beta[i]
#
#     return x, y, z


def time_slice(z):
    t_slice = len(z[0]) // 2
    return [z[i][t_slice] for i in range(len(z))]


def draw_functions(x, name, functions):
    for function, style in functions:
        y = [function[i] for i in range(x.size)]
        plt.plot(x, y, style)
    plt.title(name)
    plt.grid()
    plt.draw()
    plt.show()


def runge_rule(z, z2, p, t=None):
    if t is None:
        t = len(z[0]) // 2
    z_ = [z[i][t] for i in range(len(z))]
    z2_ = [0] * len(z)
    for i in range(len(z)):
        z2_[i] = z2[2 * i][2 * t]
    return l1_norm(diff([z_], [z2_])) / (2 ** p - 1)


def linear(g, x0, x1, t1, a, strategy, is_pres=True):
    demo_n = 50
    demo_k = int(2 * t1 / ((x1 - x0) / demo_n))
    # x, y, z = analytical(x0, x1, t1, demo_h, demo_h, g, a)
    # slices = [[time_slice(fix_grid(x, y, z, demo_h, demo_h, True)[2]), "-g"]]

    for n in range(30, 300, 30):
        k = int(2 * a * t1 / ((x1 - x0) / n))
        xa, ya, za = analytical(x0, x1, t1, n, k, g, a)
        _, _, zs = strategy(x0, x1, t1, n, k, g, a)
        _, _, zs2 = strategy(x0, x1, t1, n * 2, k * 2, g, a)
        print(f"n = {n}, r = {runge_rule(zs, zs2, 2)}")

        if is_pres:
            xaf, yaf, zaf = fix_grid(xa, ya, za, demo_n, demo_k)
            _, _, zsf = fix_grid(xa, ya, zs, demo_n, demo_k)
            _, _, z_diff = fix_grid(xa, ya, diff(zs, za), demo_n, demo_k)
            # norm = l1_norm(z_diff)
            # slices.append([time_slice(fix_grid(xsf, ysf, zsf, demo_h, demo_h, True)[2]), "-r"])
            plot_surfaces([(xaf, yaf, zaf), (xaf, yaf, zsf), (xaf, yaf, z_diff)], f"n = {n}, k = {k}")

    # draw_functions(x, f"t = {t1/2}", slices[::-2])


def non_linear(g, l, r, mxg, x0, x1, t1, strategy, inf, is_pres=True):
    demo_n = 50
    demo_k = int(2 * t1 / ((x1 - x0) / demo_n))

    for n in range(30, 300, 30):
        k = int(2 * mxg * t1 / ((x1 - x0) / n))
        x, y, z = strategy(x0, x1, t1, n, k, g, l, r)
        _, _, z2 = strategy(x0, x1, t1, n * 2, k * 2, g, l, r)
        print(f"n = {n}, r = {runge_rule(z, z2, 2)}")

        if n == 270:
            draw_functions(x, f"t = {t1 / 2}", [[time_slice(fix_grid(x, y, z, n, k, True)[2]), "-r"]])

        if is_pres:
            xf, yf, zf = fix_grid(x, y, z, demo_n, demo_k)
            plot_surfaces([(xf, yf, zf)], f"n = {n}, k = {k}", inf)


#linear(g1, 1, 6.5, 2, 1.25, three_layer_cross)
non_linear(g2, lambda t: 2, lambda t: 1, 2, -3, 3, 1, three_layer_cross_not_linear, 30)

