"""Тесты декодера: машинный код → промежуточное представление."""

import unittest

from uvm.decoder import DecodeError, decode
from uvm.encoder import encode
from uvm.parser import parse_program

SPEC = """LOAD 127, 814
READ 252, 300, 303
WRITE 237, 401
SQRT 808, 463
"""
UNKNOWN_OPCODE = bytes([0x00] * 7)


class DecoderTest(unittest.TestCase):
    """Декодирование команд из спецификации."""

    def test_decode_reverses_encode(self):
        """decode(encode(x)) возвращает те же поля."""
        for instruction in parse_program(SPEC):
            decoded = decode(encode(instruction))
            self.assertEqual(decoded.mnemonic, instruction.mnemonic)
            self.assertEqual(decoded.values, instruction.values)

    def test_spec_bytes(self):
        """Байты из спецификации дают поля из спецификации."""
        code = bytes([0xF5, 0xFC, 0x00, 0x96, 0xE0, 0x25, 0x00])
        self.assertEqual(decode(code).describe(),
                         "A=245, B=252, C=300, D=303")

    def test_unknown_opcode(self):
        """Неизвестный код операции — ошибка с адресом команды."""
        with self.assertRaisesRegex(DecodeError, "адрес команды 14"):
            decode(UNKNOWN_OPCODE, 14)


if __name__ == "__main__":
    unittest.main()
