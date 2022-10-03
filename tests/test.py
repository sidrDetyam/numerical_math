'''
from time import time

from expressions.expression import get_builder
import matplotlib.pyplot as plt


def generate(func, a, b, n=10):
    h = (b - a) / n
    x = [a + h * i for i in range(n + 1)]
    # print(x)
    y = [func(x[i]) for i in range(n + 1)]

    res = []
    for i in range(len(x)):
        a = []
        b = []
        for j in range(len(x)):
            if i != j:
                a.append(f"(x - {x[j]})")
                b.append(f"({x[i]} - {x[j]})")
        res.append(f"{y[i]} * (({' * '.join(a)}) / ({' * '.join(b)}))")

    res = " + ".join(res)
    # print(res)
    # print(eval(res.replace("x", "4")))
    builder = get_builder()
    return res, builder.build(res)


def draw_expressions(left, right, cells_count, name, *expressions):
    x = [i / cells_count for i in range(left * cells_count, right * cells_count)]
    for expr, style in expressions:
        y = [expr.calculate(i) for i in x]
        plt.plot(x, y, style)
    plt.title(name)
    plt.draw()
    plt.show()


def time_check_decorator(function, *args, **kwargs):
    def wrapper():
        label = time()
        ret = function(*args, *kwargs)
        print(f"time: {time()-label}, function: {function}")
        return ret
    return wrapper


s = "$pow(0.5, x) + cos(x)"
a, b = 1, 30  # map(int, input().split())
n = 40  # int(input())
x = 3.456  # float(input())


__ = "x*x*x + 3/sin(x)"
___ = '3*x*x - 3/2/(sin(x)*sin(x)) * cos(x)'

func = time_check_decorator(lambda: get_builder(True).build("(x*x*x - x / 23) + 234 + cos(x)"))()
_, pol = time_check_decorator(lambda: generate(func.calculate, a, b, n))()
der = time_check_decorator(lambda: pol.derivative())()

x = 10
y = time_check_decorator(lambda: pol.calculate(x))()
y2 = eval("x*x*x - x / 23 + 234 + cos(x)")


func2 = func.derivative()

print(y, y2)
print(f"{func2.calculate(x)}, {eval('3*x*x - 1/23 - sin(x)')}")
print(f"{func2.derivative().calculate(x)}, {eval('6*x - cos(x)')}")

'''