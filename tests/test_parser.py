"""Тесты разбора языка ассемблера (этап 1)."""

import io
import unittest

from uvm.assembler import EXIT_ERROR, EXIT_OK, main
from uvm.parser import AsmError, parse_program
from fixture_case import FixtureCase

SPEC = """
; тесты из спецификации
LOAD  127, 814
READ  252, 300, 303
WRITE 237, 401
SQRT  808, 463
"""

SECOND_LINE = 2

EXPECTED = [
    "A=85, B=127, C=814",
    "A=245, B=252, C=300, D=303",
    "A=31, B=237, C=401",
    "A=118, B=808, C=463",
]


class ParserTests(unittest.TestCase):
    """Перевод текста в промежуточное представление."""

    def test_spec_fields(self):
        """Поля совпадают с тестами спецификации УВМ."""
        program = parse_program(SPEC)
        self.assertEqual([i.describe() for i in program], EXPECTED)

    def test_syntax_variants(self):
        """Регистр мнемоник, шестнадцатеричные числа, пробелы, табуляция."""
        program = parse_program("load\t0x7F ,  814 ; comment\n")
        self.assertEqual(program[0].describe(), EXPECTED[0])
        self.assertEqual(program[0].line, 1)

    def test_errors(self):
        """Ошибки с номером строки."""
        cases = {
            "JUMP 5": "неизвестная команда",
            "LOAD 1": "ожидалось операндов",
            "WRITE 1, 2, 3": "ожидалось операндов",
            "LOAD 1, x": "ожидалось число",
            "LOAD -1, 2": "отрицательное",
            "LOAD 16384, 0": "не помещается",
            "LOAD 1, 1048576": "не помещается",
            "READ 1, , 3": "пустой операнд",
        }
        for text, message in cases.items():
            with self.subTest(text=text):
                with self.assertRaises(AsmError) as context:
                    parse_program("\n" + text)
                self.assertIn(message, str(context.exception))
                self.assertEqual(context.exception.line, SECOND_LINE)

    def test_field_limits(self):
        """Максимальные значения полей допустимы."""
        program = parse_program("LOAD 16383, 1048575\nREAD 32767, 0, 0")
        self.assertEqual(program[1].values, (32767, 0, 0))


class AssemblerCliTests(FixtureCase):
    """Запуск ассемблера в режиме тестирования."""

    def test_test_mode_prints_fields(self):
        """Режим тестирования выводит поля всех команд."""
        source = self.write_file("prog.asm", SPEC)
        out = io.StringIO()
        code = main([source, self.temp_path("out.bin"), "--test"], out=out)
        self.assertEqual(code, EXIT_OK)
        for line in EXPECTED:
            self.assertIn(line, out.getvalue())

    def test_errors_exit_code(self):
        """Нет файла или ошибка в программе — код 1."""
        err = io.StringIO()
        self.assertEqual(main(["/no/file.asm", "x.bin"], err=err),
                         EXIT_ERROR)
        bad = self.write_file("bad.asm", "NOP\n")
        self.assertEqual(main([bad, "x.bin"], err=err), EXIT_ERROR)
        self.assertIn("строка 1", err.getvalue())


if __name__ == "__main__":
    unittest.main()
