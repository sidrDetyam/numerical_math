import math
from matplotlib import pyplot as plt
from copy import deepcopy


def g(x):
    return math.exp(x) * math.cos(x)


def y(x):
    return ((math.sin(x) + math.cos(x)) * math.exp(x) - 1) / 2


def get_grid(x0, x1, h):
    return [0] * math.ceil((x1 - x0) / h)


def draw_functions(x, name, *functions):
    for function, style in functions:
        y = [function[i] for i in range(len(x))]
        plt.plot(x, y, style)
    plt.title(name)
    plt.grid()
    plt.draw()
    plt.show()


def diff(y1, y2):
    y = deepcopy(y1)
    for i in range(len(y2)):
        y[i] = abs(y1[i] - y2[i])
    return y


def l1_norm(y):
    return max(map(abs, y))


h = 0.5
x0 = 0
x1 = 5
y0 = 0
n = math.ceil((x1 - x0) / h)

x = get_grid(x0, x1, h)
y_ = get_grid(x0, x1, h)
y_h4 = get_grid(x0, x1, h)
y_h2 = get_grid(x0, x1, h)

y_[0] = y0
y_h4[0] = y0
y_h2[0] = y0

for i in range(1, n):
    x__ = x0 + i * h

    y_[i] = y(x__)
    if i == 1:
        y_h2[i] = (1 + h) * y_h2[0]
        y_h4[i] = h * (g(x__) + 4 * g(x__ - h)) / 3
    else:
        y_h2[i] = y_h2[i - 2] + 2 * h * g(x__ - h)  #y_h2[i - 2] + h * (g(x__) + g(x__ - 2 * h))
        y_h4[i] = y_h4[i - 2] + h * (g(x__ + h) + 4 * g(x__) + g(x__ - h))/3


draw_functions([x0 + h*i for i in range(n)], "", [y_, "-r"], [y_h4, "-b"], [y_h2, "-g"])
print(f"y_h2 {l1_norm(diff(y_, y_h4))}")
print(f"y_h4 {l1_norm(diff(y_, y_h2))}")
