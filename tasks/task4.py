from math import e
from common.draw import draw_functions


def grid(x, h):
    return (1 + h) ** (float(x) / h)


def exp(x):
    return e ** x


h = 0.01
draw_functions(0.0, 5.0, int(5.0 / h), "", [lambda x: grid(x, h), "-b"], [exp, "-r"])
