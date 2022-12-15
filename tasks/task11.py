#import matplotlib.pyplot as plt
#import numpy as np


def rk4(x, y, h, f):
    k1 = f(x, y)
    k2 = f(x + h / 2, y + h / 2 * k1)
    k3 = f(x + h / 2, y + h / 2 * k2)
    k4 = f(x + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def rk2(x, y, h, f):
    k1 = f(x, y)
    k2 = f(x + h, y + h * k1)
    return y + h/2 * (k1 + k2)


def runge_rule(y, y2, p):
    mx = 0
    for i in range(len(y)):
        mx = max(y[i] - y2[2*i], mx)
    return mx / (2**p - 1)


eps = 0.0001
x1 = 1
x2 = 2
y0 = 1
p = 4
f = lambda x, y: (-y ** 2 + 2 * x ** 3 + x ** 2) / (2 * x * x * y)
rk = lambda x, y, h: rk4(x, y, h, f)


n = 2
while True:
    h = (x2-x1) / n
    y = [0]*n
    y2 = [0]*2*n
    y[0] = y2[0] = y0

    for i in range(2*n-1):
        y2[i+1] = rk(x1 + h/2 * i, y2[i], h/2)
        if i%2 == 1:
            y[i//2 + 1] = rk(x1 + h/2 * i, y[i//2], h)

    # if n % 50 == 0:
    #     xn = np.linspace(x1, x2, n)
    #     plt.plot(xn, y, "-b")

    e = runge_rule(y, y2, p)
    if e < eps:
        print(e, n)
        break
    n += 1


# plt.grid()
# plt.draw()
# plt.show()