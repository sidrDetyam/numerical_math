from math import ceil, pi

from common.draw import draw_functions
from expressions.expression import get_builder

EPS = 0.0001


def next_x(x, expr, expr_der):
    return x - expr.calculate(x) / expr_der.calculate(x)


def newton_iteration(expr_str, x0):
    builder = get_builder()
    expr = builder.build(expr_str)
    expr_der = expr.derivative()

    try:
        x1 = next_x(x0, expr, expr_der)
        x2 = next_x(x1, expr, expr_der)
        while True:
            if abs(x2 - x1) < EPS:
                return x2

            if abs(x2 - x1) > abs(x1 - x0):
                return None

            x0 = x1
            x1 = x2
            x2 = next_x(x2, expr, expr_der)
    except ValueError:
        return None


l = 52
s = f"{l} * sin(x) - x"

builder = get_builder()
n = ceil((l - pi / 2) / 2 / pi)
solutions = []

for i in range(n):
    s_ = f"{l} * sin(x) + x - {4 * pi * i + pi}"

    x1 = 4 * pi * i + pi - newton_iteration(s_, pi + 2 * pi * i)
    x2 = newton_iteration(s, pi + 2 * pi * i)
    solutions += [x1, x2]

s_ = f"{l} * sin(x) + x - {4 * pi * n + pi}"
x1_ = newton_iteration(s_, pi + n * 2 * pi)
x1 = (4 * pi * n + pi - x1_) if x1_ is not None else None
if x1 is not None:
    if abs(builder.build(f"{l} * sin(x)").derivative().calculate(x1) - 1) > EPS:
        x2 = 4 * pi * n + pi - newton_iteration(s_, pi / 2 + EPS + n * 2 * pi)
        solutions += [x1, x2]
    else:
        solutions += [x1]

solutions += [-i for i in solutions[1:]]
print(solutions)

draw_functions(min(solutions) - 1, max(solutions) + 1, 100, "red: sin(x), blue: x",
               [builder.build(f"{l} * sin(x)").calculate, "-r"],
               [builder.build("x").calculate, "-b"])
