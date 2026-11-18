"""Тесты перевода в машинный код (этап 2)."""

import io
import unittest

from uvm.assembler import EXIT_OK, main
from uvm.encoder import encode, encode_program, format_bytes
from uvm.parser import parse_program
from fixture_case import FixtureCase

SPEC_BYTES = {
    "LOAD 127, 814": [0x55, 0x7F, 0x80, 0xCB, 0x00, 0x00, 0x00],
    "READ 252, 300, 303": [0xF5, 0xFC, 0x00, 0x96, 0xE0, 0x25, 0x00],
    "WRITE 237, 401": [0x1F, 0xED, 0x40, 0x64, 0x00, 0x00, 0x00],
    "SQRT 808, 463": [0x76, 0x28, 0xC3, 0x73, 0x00, 0x00, 0x00],
}


class EncoderTests(unittest.TestCase):
    """Байтовые последовательности команд."""

    def test_spec_bytes(self):
        """Каждая команда совпадает с тестом спецификации."""
        for text, expected in SPEC_BYTES.items():
            with self.subTest(text=text):
                instruction = parse_program(text)[0]
                self.assertEqual(list(encode(instruction)), expected)

    def test_program_is_concatenation(self):
        """Программа — команды подряд по 7 байт."""
        program = parse_program("\n".join(SPEC_BYTES))
        code = encode_program(program)
        expected = [b for value in SPEC_BYTES.values() for b in value]
        self.assertEqual(list(code), expected)

    def test_max_values(self):
        """Биты 8–41 заполнены единицами, старший байт пуст."""
        code = encode(parse_program("LOAD 16383, 1048575")[0])
        self.assertEqual(list(code), [0x55, 0xFF, 0xFF, 0xFF, 0xFF,
                                      0x03, 0x00])

    def test_format(self):
        """Формат вывода байтов."""
        self.assertEqual(format_bytes(bytes([0x55, 0x0A])), "0x55, 0x0A")


class AssemblerOutputTests(FixtureCase):
    """Файл-результат и вывод ассемблера."""

    def test_binary_file_and_count(self):
        """Файл совпадает с тестами, выводится число команд."""
        source = self.write_file("spec.asm", "\n".join(SPEC_BYTES))
        output = self.temp_path("spec.bin")
        out = io.StringIO()
        self.assertEqual(main([source, output, "--test"], out=out),
                         EXIT_OK)
        with open(output, "rb") as handle:
            data = list(handle.read())
        self.assertEqual(data, [b for v in SPEC_BYTES.values() for b in v])
        self.assertIn("Ассемблировано команд: 4", out.getvalue())
        self.assertIn("0x55, 0x7F, 0x80, 0xCB, 0x00, 0x00, 0x00",
                      out.getvalue())


if __name__ == "__main__":
    unittest.main()
