from .expression_parser import ExpressionParser


class Number(object):
    EPS = 0.00000001

    def __init__(self, number):
        self.number = number

    def calculate(self, x):
        return self.number

    @staticmethod
    def derivative():
        return Number(0)

    def equal(self, other):
        return abs(other - self.number) < self.EPS


class Var(object):
    def __init__(self):
        pass

    @staticmethod
    def calculate(x):
        return x

    @staticmethod
    def derivative():
        return Number(1)


class Plus(object):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    @staticmethod
    def of(expr1, expr2):
        if isinstance(expr1, Number) and expr1.equal(0):
            return expr2
        if isinstance(expr2, Number) and expr2.equal(0):
            return expr1
        if isinstance(expr1, Number) and isinstance(expr2, Number):
            return Number(expr1.number + expr2.number)

        return Plus(expr1, expr2)

    def calculate(self, x):
        return self.expr1.calculate(x) + self.expr2.calculate(x)

    def derivative(self):
        return Plus.of(self.expr1.derivative(), self.expr2.derivative())


class Minus(object):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    @staticmethod
    def of(expr1, expr2):
        if isinstance(expr1, Number) and expr1.equal(0):
            if isinstance(expr2, Number):
                expr2.number *= -1.0
                return expr2

        if isinstance(expr2, Number) and expr2.equal(0):
            return expr1

        if isinstance(expr1, Number) and isinstance(expr2, Number):
            return Number(expr1.number - expr2.number)

        return Minus(expr1, expr2)

    def calculate(self, x):
        return self.expr1.calculate(x) - self.expr2.calculate(x)

    def derivative(self):
        return Minus.of(self.expr1.derivative(), self.expr2.derivative())


class Production(object):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    @staticmethod
    def of(expr1, expr2):
        if isinstance(expr1, Number):
            if expr1.equal(0):
                return Number(0)
            if expr1.equal(1):
                return expr2
        if isinstance(expr2, Number):
            if expr2.equal(0):
                return Number(0)
            if expr2.equal(1):
                return expr1
        if isinstance(expr1, Number) and isinstance(expr2, Number):
            return Number(expr1.number * expr2.number)

        return Production(expr1, expr2)

    def calculate(self, x):
        return self.expr1.calculate(x) * self.expr2.calculate(x)

    def derivative(self):
        return Plus.of(Production.of(self.expr1.derivative(), self.expr2),
                       Production.of(self.expr2.derivative(), self.expr1))


class Division(object):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    @staticmethod
    def of(expr1, expr2):
        if isinstance(expr1, Number) and expr1.equal(0):
            return Number(0)

        if isinstance(expr2, Number) and expr2.equal(1):
            return expr1

        if isinstance(expr1, Number) and isinstance(expr2, Number):
            return Number(expr1.number / expr2.number)

        return Division(expr1, expr2)

    def calculate(self, x):
        return self.expr1.calculate(x) / self.expr2.calculate(x)

    def derivative(self):
        return Division(
            Minus.of(Production.of(self.expr1.derivative(), self.expr2),
                     Production.of(self.expr2.derivative(), self.expr1)),
            Production.of(self.expr2, self.expr2))


class ExpressionBuilder(object):
    _operations = {
        "+": Plus.of,
        "-": Minus.of,
        "*": Production.of,
        "/": Division.of,
    }

    def __init__(self, context, is_debug=False):
        self._parser = ExpressionParser(is_debug)
        self._context = context

    def _build(self, node):
        if node.is_term():
            if node.type() == "number":
                return Number(float(node.value()))
            if node.type() == "var":
                return Var()

        children = node.children()
        if node.type() == "func":
            return self._context[children[0].value()](
                self._build(children[1])
            )
        if node.type() == "param_func":
            return self._context[children[0].value()](
                float(children[1].value()),
                self._build(children[2])
            )

        return self._operations[node.type()](
            self._build(children[0]),
            self._build(children[1])
        )

    def build(self, input_str):
        tree = self._parser.parse(input_str)
        return self._build(tree)
