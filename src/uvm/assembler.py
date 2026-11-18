"""Ассемблер УВМ: ``python3 -m uvm.assembler ИСХОДНИК РЕЗУЛЬТАТ [--test]``."""

import argparse
import sys

from .parser import AsmError, parse_program

EXIT_OK = 0
EXIT_ERROR = 1


def build_parser():
    """Описать аргументы командной строки ассемблера."""
    parser = argparse.ArgumentParser(
        prog="uvm-asm", description="Ассемблер учебной виртуальной машины.")
    parser.add_argument("source", help="файл с текстом программы (.asm)")
    parser.add_argument("output", help="двоичный файл-результат (.bin)")
    parser.add_argument("-t", "--test", action="store_true",
                        help="режим тестирования: показать поля команд")
    return parser


def read_source(path):
    """Прочитать исходный текст программы."""
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def print_fields(program, out):
    """Вывести промежуточное представление в формате «поле=значение»."""
    for instruction in program:
        print(f"{instruction.mnemonic:<6} {instruction.describe()}",
              file=out)


def main(argv=None, out=None, err=None):
    """Запустить ассемблер и вернуть код завершения."""
    out = out or sys.stdout
    err = err or sys.stderr
    args = build_parser().parse_args(argv)
    try:
        program = parse_program(read_source(args.source))
    except OSError as problem:
        print(f"Ошибка: не удалось прочитать {args.source}: "
              f"{problem.strerror}", file=err)
        return EXIT_ERROR
    except AsmError as problem:
        print(f"Ошибка в {args.source}, {problem}", file=err)
        return EXIT_ERROR
    if args.test:
        print_fields(program, out)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
