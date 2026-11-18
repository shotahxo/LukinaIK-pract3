"""Тесты интерпретатора: аргументы, дамп CSV, программа копирования."""

import io
import os
import unittest

from fixture_case import FixtureCase
from uvm import assembler, interpreter
from uvm.dump import RangeError, parse_range

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")
MEMORY = 1000
SOURCE = [11, 22, 33, 44, 55]


def read_dump(path):
    """Прочитать CSV-дамп в словарь «адрес → значение»."""
    with open(path, encoding="utf-8") as handle:
        rows = handle.read().split()
    return {int(a): int(v) for a, v in (row.split(",") for row in rows[1:])}


class RangeTest(unittest.TestCase):
    """Разбор диапазона адресов."""

    def test_decimal_and_hex(self):
        """Поддерживаются десятичная и шестнадцатеричная записи."""
        self.assertEqual(parse_range("0-31", MEMORY), (0, 31))
        self.assertEqual(parse_range("0x10-0x1F", MEMORY), (16, 31))

    def test_bad_ranges(self):
        """Неверные диапазоны отклоняются."""
        for text in ("abc", "5-1", "0-1000", "-3"):
            with self.subTest(text=text):
                with self.assertRaises(RangeError):
                    parse_range(text, MEMORY)


class InterpreterTest(FixtureCase):
    """Запуск интерпретатора через main()."""

    def prepare(self):
        """Ассемблировать пример копирования массива."""
        self.program = self.temp_path("copy.bin")
        self.dump = self.temp_path("dump.csv")
        source = os.path.join(EXAMPLES, "copy_array.asm")
        assembler.main([source, self.program], io.StringIO())

    def run_vm(self, *args):
        """Запустить интерпретатор, вернуть код, stdout и stderr."""
        out, err = io.StringIO(), io.StringIO()
        code = interpreter.main(list(args), out, err)
        return code, out.getvalue(), err.getvalue()

    def test_copy_array(self):
        """Массив скопирован на адреса 200–204 и 300–304."""
        code, out, _err = self.run_vm(self.program, self.dump, "100-304")
        self.assertEqual(code, interpreter.EXIT_OK)
        self.assertIn("Выполнено команд: 16", out)
        dump = read_dump(self.dump)
        for base in (100, 200, 300):
            values = [dump[base + i] for i in range(len(SOURCE))]
            self.assertEqual(values, SOURCE)

    def test_csv_header_and_range(self):
        """Дамп содержит заголовок и ровно запрошенные адреса."""
        self.run_vm(self.program, self.dump, "8-12")
        with open(self.dump, encoding="utf-8") as handle:
            lines = handle.read().split()
        self.assertEqual(lines, ["address,value", "8,0", "9,0",
                                 "10,100", "11,0", "12,0"])

    def test_missing_program(self):
        """Нет файла программы — сообщение и код ошибки."""
        code, _out, err = self.run_vm("nope.bin", self.dump, "0-1")
        self.assertEqual(code, interpreter.EXIT_ERROR)
        self.assertIn("nope.bin", err)

    def test_bad_range(self):
        """Неверный диапазон — сообщение и код ошибки."""
        code, _out, err = self.run_vm(self.program, self.dump, "9-1")
        self.assertEqual(code, interpreter.EXIT_ERROR)
        self.assertIn("больше конца", err)


if __name__ == "__main__":
    unittest.main()
