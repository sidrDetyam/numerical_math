from numpy import matrix, dot, array
import numpy as np


def proj(a, b):
    return b.copy().dot(dot(a, b) / dot(b, b))


def gramm(a):
    q = [array([a[j, i] for j in range(a.shape[0])]) for i in range(a.shape[1])]
    for i in range(len(q)):
        ai = q[i].copy()
        for j in range(i):
            q[i] -= proj(ai, q[j])

    for i in range(len(q)):
        q[i] = q[i] / np.linalg.norm(q[i])
    return matrix(q).transpose()


def solve(a, b):
    q = gramm(a)
    r = q.transpose() * a
    y_ = q.transpose().dot(b)
    y = array([y_[0, i] for i in range(b.shape[0])])

    x = y.copy()
    for i in range(b.shape[0]-1, -1, -1):
        for j in range(b.shape[0]-1, i, -1):
            y[i] -= r[i, j] * x[j]
        x[i] = y[i] / r[i, i]

    return x


a = matrix([[20, 20, 0.],
            [15, 15, 5.],
            [0, 1, 1.]])

x = solve(a, array([40, 35, 2.]))

print(x)
print(a.dot(x))

