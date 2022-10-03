from common.draw import draw_functions
from expressions.expression import get_builder


def generate(function, left, right, n=10):
    h = (right - left) / n
    x = [left + h * i for i in range(n + 1)]
    y = [function(x[i]) for i in range(n + 1)]

    res = []
    for i in range(len(x)):
        numerator = []
        denominator = []
        for j in range(len(x)):
            if i != j:
                numerator.append(f"(x - {x[j]})")
                denominator.append(f"({x[i]} - {x[j]})")
        res.append(f"{y[i]} * (({' * '.join(numerator)}) / ({' * '.join(denominator)}))")

    res = " + ".join(res)
    builder = get_builder(False)
    return res, builder.build(res)


s = "$pow(0.5, x) + cos(x)"
a, b = 1, 30
n = 20
x = 7

function = get_builder(False).build(s)
_, polynom_n = generate(function.calculate, a, b, n)
_, polynom_2n = generate(function.calculate, a, b, n * 2)
draw_functions(a, b, 20, f"{n} точек",
               [function.calculate, "-r"],
               [polynom_n.calculate, ":g"],
               [polynom_2n.calculate, "--b"])

print(f"n: {function.calculate(x) - polynom_n.calculate(x)}\n"
      f"2n: {function.calculate(x) - polynom_2n.calculate(x)}")
