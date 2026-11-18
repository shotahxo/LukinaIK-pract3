"""Ассемблер УВМ: ``python3 -m uvm.assembler SRC OUT [--test]``."""

import argparse
import os
import sys

from .encoder import encode, encode_program, format_bytes
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
                        help="режим тестирования: показать поля и байты")
    return parser


def read_source(path):
    """Прочитать исходный текст программы."""
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def print_test_view(program, out):
    """Вывести поля и байты каждой команды, как в спецификации."""
    for instruction in program:
        print(f"{instruction.mnemonic:<6} {instruction.describe()}",
              file=out)
        print(f"{'':<6} {format_bytes(encode(instruction))}", file=out)


def write_binary(path, code):
    """Записать машинный код в двоичный файл (каталог создаётся)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(code)


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
        print_test_view(program, out)
    try:
        write_binary(args.output, encode_program(program))
    except OSError as problem:
        print(f"Ошибка: не удалось записать {args.output}: "
              f"{problem.strerror}", file=err)
        return EXIT_ERROR
    print(f"Ассемблировано команд: {len(program)}", file=out)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
