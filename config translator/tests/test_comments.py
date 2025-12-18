from lark import Lark
from transformer import ConfigTransformer

parser = Lark.open(
    "grammar.lark",
    parser="lalr",
    transformer=ConfigTransformer()
)

def test_single_line_comment():
    parser.parse("""
        \\ comment
        var A = 1.0;
    """)
    assert parser.options.transformer.vars["A"] == 1.0

def test_multi_line_comment():
    parser.parse("""
        #[
        multi
        comment
        ]#
        var A = 2.0;
    """)
    assert parser.options.transformer.vars["A"] == 2.0
