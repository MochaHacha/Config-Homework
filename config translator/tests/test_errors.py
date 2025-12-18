import pytest
from lark import Lark
from transformer import ConfigTransformer

parser = Lark.open(
    "grammar.lark",
    parser="lalr",
    transformer=ConfigTransformer()
)

def test_missing_semicolon():
    with pytest.raises(Exception):
        parser.parse("var A = 1.0")

def test_unknown_syntax():
    with pytest.raises(Exception):
        parser.parse("var = 1.0;")
