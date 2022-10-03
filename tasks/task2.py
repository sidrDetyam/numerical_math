from expressions.expression import get_builder

EPS = 0.000000001
def simple_iteration(expr_str, x0):
    builder = get_builder()
    expr = builder.build(expr_str)

    try:
        x1 = expr.calculate(x0)
        x2 = expr.calculate(x1)
        while(True):
            if abs(x2 - x1) < EPS:
                return x2
            
            if abs(x2-x1) > abs(x1-x0):
                return None

            x0 = x1
            x1 = x2
            x2 = expr.calculate(x2)
    except ValueError as err:
        return None


a = 9.7
s = f"$exp(2.718281828, x-{a}) - 1"
s_ = f"ln(1+x) + {a}"
x0 = 0

print(simple_iteration(s, x0))
print(simple_iteration(s_, x0))