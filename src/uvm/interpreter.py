"""Интерпретатор УВМ: ``python3 -m uvm.interpreter PROG DUMP RANGE``."""

import argparse
import sys

from .decoder import DecodeError
from .dump import RangeError, parse_range, save_dump
from .machine import DATA_SIZE, Machine, VmError

EXIT_OK = 0
EXIT_ERROR = 1


def build_parser():
    """Описать аргументы командной строки интерпретатора."""
    parser = argparse.ArgumentParser(
        prog="uvm-run",
        description="Интерпретатор учебной виртуальной машины.")
    parser.add_argument("program", help="двоичный файл программы (.bin)")
    parser.add_argument("dump", help="файл для дампа памяти (.csv)")
    parser.add_argument("range", help="диапазон адресов дампа, например 0-31")
    return parser


def read_program(path):
    """Прочитать двоичный файл программы."""
    with open(path, "rb") as handle:
        return handle.read()


def execute(args, out):
    """Выполнить программу и сохранить дамп памяти."""
    start, end = parse_range(args.range, DATA_SIZE)
    machine = Machine(read_program(args.program))
    steps = machine.run()
    save_dump(args.dump, machine.data, start, end)
    print(f"Выполнено команд: {steps}", file=out)
    print(f"Дамп памяти {start}-{end} сохранён в {args.dump}", file=out)


def main(argv=None, out=None, err=None):
    """Запустить интерпретатор и вернуть код завершения."""
    out = out or sys.stdout
    err = err or sys.stderr
    args = build_parser().parse_args(argv)
    try:
        execute(args, out)
    except OSError as problem:
        print(f"Ошибка: {problem.filename}: {problem.strerror}", file=err)
        return EXIT_ERROR
    except (RangeError, VmError, DecodeError) as problem:
        print(f"Ошибка: {problem}", file=err)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
