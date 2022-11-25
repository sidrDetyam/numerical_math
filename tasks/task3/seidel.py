import numpy as np

eps = 0.001


def seigel(a, x0, b):
    c = a.copy()
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            c[i, j] = 0. if i == j else -(a[i, j] / a[i, i])

    d = b.copy()
    for i in range(b.shape[0]):
        d[i] = b[i] / a[i, i]

    x = x0.copy()
    while True:
        x_ = x.copy()
        for i in range(x.shape[0]):
            x[i] = d[i]
            for j in range(x.shape[0]):
                x[i] += c[i, j] * x[j]

        if np.linalg.norm(x - x_) < eps:
            break

    return x


a = np.matrix([
    [2, 1, -1.],
    [1, -5, 4.],
    [3, 2, 6.]
])
x0 = np.array([0, 0, 0.])
b = np.array([0, 10, 7.])

x = seigel(a, x0, b)
print(x)
print(a.dot(x))

