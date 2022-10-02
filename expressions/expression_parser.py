from .my_ll1 import LL1Grammar, LL1AstBuilder, TokenExtractor, \
    NonTerminalNode, TerminalNode


class ExpressionParser(object):
    @staticmethod
    def _et_prepare(node):
        children = node.children()
        if len(children[1].children()) == 1:
            return ExpressionParser._prepare(children[0])

        res_node = NonTerminalNode(children[1].children()[0].value())
        res_node.add_child(ExpressionParser._prepare(children[0]))
        res_node.add_child(ExpressionParser._prepare(children[1].children()[1]))
        return res_node

    @staticmethod
    def _prepare(node):
        if node.type() in ["E", "T"]:
            return ExpressionParser._et_prepare(node)

        children = node.children()
        if len(children) == 1:
            return children[0]

        if len(children) == 2:
            res_node = NonTerminalNode(children[0].value())
            res_node.add_child(TerminalNode("number", "0"))
            res_node.add_child(children[1])
            return res_node

        if len(children) == 3:
            return ExpressionParser._prepare(children[1])

        if len(children) == 4:
            res_node = NonTerminalNode("func")
            res_node.add_child(children[0])
            res_node.add_child(ExpressionParser._prepare(children[2]))
            return res_node

        res_node = NonTerminalNode("param_func")
        res_node.add_child(children[0])
        res_node.add_child(children[2])
        res_node.add_child(ExpressionParser._prepare(children[4]))
        return res_node

    _extractor = TokenExtractor({
        "var": r"x",
        "func": r"[A-Za-z_]\w*",
        "param_func": r"\$[A-Za-z_]\w*",
        "add_op": r"[+-]",
        "mul_op": r"[*/]",
        "number": r"\d+(\.\d+)?",
    })

    _grammar = LL1Grammar("E", {
        "E": [["T", "EE"]],
        "EE": [["add_op", "E"], [""]],
        "T": [["F", "TT"]],
        "TT": [["mul_op", "T"], [""]],
        "F": [["number"], ["add_op", "number"],
              ["var"], ["add_op", "var"],
              ["(", "E", ")"],
              ["func", "(", "E", ")"],
              ["param_func", "(", "number", ",", "E", ")"]],
    })

    def __init__(self, is_debug=False):
        self._builder = LL1AstBuilder(self._extractor, self._grammar, is_debug)
        self._is_debug = is_debug

    def parse(self, input_str):
        unprepared = self._builder.build(input_str)
        prepared = ExpressionParser._prepare(unprepared)
        if self._is_debug:
            print("Prepared AST:\n")
            prepared.print()
            print("")
        return prepared
