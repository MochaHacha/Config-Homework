from lark import Lark
from transformer import ConfigTransformer

parser = Lark.open(
    "grammar.lark",
    parser="lalr",
    transformer=ConfigTransformer()
)

def test_number():
    parser.parse("var A = 1.5;")
    assert parser.options.transformer.vars["A"] == 1.5

def test_string():
    parser.parse('var S = @"hello";')
    assert parser.options.transformer.vars["S"] == "hello"
