import pytest
from lark import Lark
from transformer import ConfigTransformer

# Создаем один общий экземпляр для тестов
t = ConfigTransformer()
parser = Lark.open(
    "grammar.lark",
    parser="lalr",
    transformer=t
)

def test_postfix_add():
    # Очищаем переменные перед тестом
    t.vars = {}
    parser.parse("var A = ?{2.0 3.0 +};")
    assert t.vars["A"] == 5.0

def test_postfix_len():
    t.vars = {}
    parser.parse("var A = (list 1.0 2.0 3.0); var B = ?{A len};")
    # Твой трансформер возвращает float (3.0), поэтому сравниваем с 3.0
    assert t.vars["B"] == 3.0