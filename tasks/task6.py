import matplotlib.pyplot as plt

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


def draw_functions(left, right, cells_count, name, *functions):
    x = [i / cells_count for i in range(left * cells_count, right * cells_count)]
    for function, style in functions:
        y = [function(i) for i in x]
        plt.plot(x, y, style)
    plt.title(name)
    plt.draw()
    plt.show()


s = "$pow(0.5, x) + cos(x)"
a, b = 1, 30
n = 4
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
