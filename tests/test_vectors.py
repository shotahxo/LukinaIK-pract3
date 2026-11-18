"""Тесты основной задачи: sqrt() над вектором длины 10 на месте."""

import io
import math
import os
import re
import unittest

from fixture_case import FixtureCase
from uvm import assembler, interpreter

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")
VECTOR_LENGTH = 10
PROGRAMS = ("vector_squares", "vector_mixed", "vector_large")
LOAD_RE = re.compile(r"^LOAD (\d+), (\d+)$", re.MULTILINE)


def initial_vector(text):
    """Адрес начала и исходные значения вектора из текста программы."""
    pairs = [(int(a), int(v)) for a, v in LOAD_RE.findall(text)]
    vector = pairs[:VECTOR_LENGTH]
    return vector[0][0], [value for _address, value in vector]


class VectorProgramTest(FixtureCase):
    """Каждая из трёх программ даёт корни на месте исходного вектора."""

    def run_program(self, name):
        """Выполнить пример и вернуть его текст и строки дампа."""
        source = os.path.join(EXAMPLES, f"{name}.asm")
        with open(source, encoding="utf-8") as handle:
            text = handle.read()
        base, _values = initial_vector(text)
        program = self.temp_path(f"{name}.bin")
        dump = self.temp_path(f"{name}.csv")
        assembler.main([source, program], io.StringIO())
        end = base + VECTOR_LENGTH - 1
        interpreter.main([program, dump, f"{base}-{end}"], io.StringIO())
        with open(dump, encoding="utf-8") as handle:
            return text, handle.read()

    def test_roots_replace_source(self):
        """В ячейках вектора — целые корни исходных значений."""
        for name in PROGRAMS:
            with self.subTest(program=name):
                text, dump = self.run_program(name)
                base, values = initial_vector(text)
                expected = ["address,value"] + [
                    f"{base + i},{math.isqrt(v)}"
                    for i, v in enumerate(values)]
                self.assertEqual(dump.split(), expected)

    def test_expected_files(self):
        """Дампы совпадают с файлами examples/expected/*.csv."""
        for name in PROGRAMS:
            with self.subTest(program=name):
                _text, dump = self.run_program(name)
                path = os.path.join(EXAMPLES, "expected", f"{name}.csv")
                with open(path, encoding="utf-8") as handle:
                    self.assertEqual(dump, handle.read())


if __name__ == "__main__":
    unittest.main()
