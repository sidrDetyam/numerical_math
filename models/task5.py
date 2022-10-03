from expressions.expression import get_builder

EPS = 0.0001


def next(x, expr, expr_):
    return x - expr.calculate(x)/expr_.calculate(x)


def newton_iteration(expr_str, x0):
    builder = get_builder()
    expr = builder.build(expr_str)
    expr_ = expr.derivative()

    try:
        x1 = next(x0, expr, expr_)
        x2 = next(x1, expr, expr_)
        while(True):
            if abs(x2-x1) < EPS:
                return x2
            
            if abs(x2-x1) > abs(x1-x0):
                return None

            x0 = x1
            x1 = x2
            x2 = next(x2, expr, expr_)
    except ValueError as err:
        return None

l = 23
s = f"{l} * sin(x) - x"
x0 = 4

from math import ceil, pi
n = ceil((l-pi/2)/2/pi)
for i in range(1, n):
    print(newton_iteration(s, pi/2 + pi*i + 0.001))
    print(newton_iteration(s, pi + pi*i + 0.001))


