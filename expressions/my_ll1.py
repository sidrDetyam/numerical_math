import re
from copy import deepcopy


class TokenExtractor(object):
    @staticmethod
    def _prepare(input_str):
        return input_str.replace(" ", "")

    def get_tokens(self):
        return self._token_regex

    def extract(self, input_str):
        tokens = []
        pos = 0
        input_str = self._prepare(input_str)
        while pos != len(input_str):
            for token_name in self._token_regex:
                match = re.search(self._token_regex[token_name], input_str[pos:])

                if match is not None and match.span()[0] == 0:
                    tokens.append((token_name, match.group()))
                    pos += match.span()[1]
                    break
            else:
                tokens.append((input_str[pos], input_str[pos]))
                pos += 1

        return tokens

    def __init__(self, token_regex):
        self._token_regex = deepcopy(token_regex)


class MyException(Exception):
    pass


class GrammarException(MyException):
    pass


class ParsingException(MyException):
    pass


class LL1Grammar(object):

    # TODO
    def _check_grammar(self, start_symbol, productions):
        return True

    def is_terminal(self, symbol):
        return not (symbol in self._productions)

    def get_non_terminals_set(self):
        return set(self._productions.keys())

    def get_productions(self):
        return dict(self._productions)

    def get_start_symbol(self):
        return self._start

    def first_set(self, non_term):
        first = self._non_term_first_set.get(non_term)
        if first is not None:
            return first

        first = set()
        non_term_prod = self._productions[non_term]
        if non_term_prod is None:
            return None

        for prod in non_term_prod:
            if self.is_terminal(prod[0]):
                first.add(prod[0])
            else:
                first = first | self.first_set(prod[0])
        return first

    def follow_set(self, production):
        if self.is_terminal(production[0]):
            follow = set()
            follow.add(production[0])
            return follow

        return self.first_set(production[0])

    def __init__(self, start_symbol, productions):
        if not self._check_grammar(start_symbol, productions):
            raise GrammarException("Incorrect grammar")

        self._start = start_symbol
        self._productions = deepcopy(productions)

        self._non_term_first_set = dict()
        for non_term in productions.keys():
            self._non_term_first_set[non_term] = self.first_set(non_term)


TAB = "    "


class NonTerminalNode(object):
    def __init__(self, node_type):
        self._node_type = node_type
        self._children = []

    @staticmethod
    def is_term():
        return False

    def type(self):
        return self._node_type

    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def __str__(self):
        return f"{self._node_type} [{', '.join(str(i) for i in self._children)}]"

    def print(self, deep=0):
        print(TAB * deep + "[" + self._node_type + "]{")
        for child in self._children:
            child.print(deep + 1)
        print(TAB * deep + "}")


class TerminalNode(object):
    def __init__(self, node_type, value):
        self._node_type = node_type
        self._value = value

    @staticmethod
    def is_term():
        return True

    def type(self):
        return self._node_type

    def value(self):
        return self._value

    def __str__(self):
        return f"(Term {self._node_type} {self._value})"

    def print(self, deep=0):
        print(f"{TAB * deep}(type: {self._node_type if self._node_type else '<empty>'}, value: {self._value})")


class LL1AstBuilder(object):
    def __init__(self, token_extractor, ll1_grammar, is_debug=False):
        self._token_extractor = token_extractor
        self._grammar = ll1_grammar
        self._is_debug = is_debug

    def _r_build(self, tokens, node_type):
        node = NonTerminalNode(node_type)

        prods = self._grammar.get_productions()[node_type]
        for prod in prods:
            if tokens and tokens[0][0] in self._grammar.follow_set(prod):
                for i in prod:
                    if self._grammar.is_terminal(i):
                        if not tokens:
                            raise ParsingException(f"Expected term [{i}] but nothing found")
                        token = tokens.pop(0)
                        if token[0] != i:
                            raise ParsingException(f"Expected term [{i}] but {token} found")
                        node.add_child(TerminalNode(token[0], token[1]))
                    else:
                        node.add_child(self._r_build(tokens, i))
                return node

        if [""] in prods:
            node.add_child(TerminalNode("", ""))
            return node

        raise ParsingException("Not found rule for " + node.type())

    def build(self, input_str):
        tokens = self._token_extractor.extract(input_str)
        if self._is_debug:
            print(f"Tokens: {tokens}\n")
        ast = self._r_build(tokens, self._grammar.get_start_symbol())
        if self._is_debug:
            print("AST:\n")
            ast.print()
            print()

        if tokens:
            raise ParsingException("Unexpected terms: " + str(tokens))
        return ast
