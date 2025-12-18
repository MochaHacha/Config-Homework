from lark import Lark
from transformer import ConfigTransformer

parser = Lark.open(
    "grammar.lark",
    parser="lalr",
    transformer=ConfigTransformer()
)

def test_list():
    parser.parse("var A = (list 1.0 2.0 3.0);")
    assert parser.options.transformer.vars["A"] == [1.0, 2.0, 3.0]

def test_nested_list():
    parser.parse("var A = (list (list 1.0 2.0) 3.0);")
    assert parser.options.transformer.vars["A"] == [[1.0, 2.0], 3.0]
