import argparse
import os
import sys
from lark import Lark
from transformer import ConfigTransformer
from xml_writer import to_xml


def main():
    #настройка парсера аргументов 
    parser = argparse.ArgumentParser(
        description="Config language → XML translator"
    )
    #путь к входному файлу
    parser.add_argument(
        "--in", dest="inp", required=True, help="Input .conf file"
    )
    #путь к выходному файлу
    parser.add_argument(
        "--out", required=True, help="Output .xml file"
    )
    args = parser.parse_args()

    #чтение входных данных
    try:
        with open(args.inp, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Input file not found: {args.inp}", file=sys.stderr)
        sys.exit(1)
    #Проверка ну пустоту
    if not text.strip():
        print("Input file is empty", file=sys.stderr)
        sys.exit(1)

    #определени обсолютного пути к файлу с грамматикой
    base_dir = os.path.dirname(os.path.abspath(__file__))
    grammar_path = os.path.join(base_dir, "grammar.lark")

    #инициализация парсера lark
    if not os.path.exists(grammar_path):
        print(f"grammar.lark not found: {grammar_path}", file=sys.stderr)
        sys.exit(1)

    lark_parser = Lark.open(
        grammar_path,
        parser="lalr",
        transformer=ConfigTransformer()
    )

    
    try:
        lark_parser.parse(text)
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)

    # генерация xml
    vars_dict = lark_parser.options.transformer.vars
    #превращает словарь переменных в xml строкку 
    xml = to_xml(vars_dict)

    # output
    try:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(xml)
    except Exception as e:
        print(f"Cannot write output file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: XML written to {args.out}")


if __name__ == "__main__":
    main()
