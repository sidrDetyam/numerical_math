from math import sin, cos, log

from .expression_builder import Production, Number, ExpressionBuilder, Minus, Division


class Pow(object):
    def __init__(self, pow_, expr):
        self.pow = pow_
        self.expr = expr

    def calculate(self, x):
        return self.expr.calculate(x) ** self.pow

    def derivative(self):
        return Production.of(
            Production.of(Number(self.pow), Pow(self.pow - 1, self.expr)),
            self.expr.derivative())


CosRef = None


class Sin(object):
    def __init__(self, expr):
        self.expr = expr

    def calculate(self, x):
        return sin(self.expr.calculate(x))

    def derivative(self):
        return Production.of(CosRef(self.expr), self.expr.derivative())


class Cos(object):
    def __init__(self, expr):
        self.expr = expr

    def calculate(self, x):
        return cos(self.expr.calculate(x))

    def derivative(self):
        return Production.of(Minus.of(Number(0), Sin(self.expr)), self.expr.derivative())


CosRef = Cos


class Log(object):
    def __init__(self, expr):
        self.expr = expr

    def calculate(self, x):
        return log(self.expr.calculate(x))

    def derivative(self):
        return Division(self.expr.derivative(), self.expr)


class Exp(object):
    def __init__(self, base, expr):
        self.expr = expr
        self.base = base

    def calculate(self, x):
        return self.base ** self.expr.calculate(x)

    def derivative(self):
        return Production(Exp(self.base, self.expr), Log(Number(self.base)))


def get_builder(is_debug=False):
    return ExpressionBuilder({
        "$pow": Pow,
        "sin": Sin,
        "cos": Cos,
        "ln": Log,
        "$exp": Exp,
    },
        is_debug)
