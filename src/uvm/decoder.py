"""Перевод машинного кода обратно в промежуточное представление."""

from .encoder import BYTE_ORDER
from .ir import Instruction
from .spec import BY_OPCODE, OPCODE_BITS

OPCODE_MASK = (1 << OPCODE_BITS) - 1


class DecodeError(Exception):
    """Неизвестный код операции или неполная команда."""


def decode(code, address=0):
    """Разобрать 7 байт машинного кода в ``Instruction``."""
    word = int.from_bytes(code, BYTE_ORDER)
    opcode = word & OPCODE_MASK
    fmt = BY_OPCODE.get(opcode)
    if fmt is None:
        raise DecodeError(f"адрес команды {address}: неизвестный код "
                          f"операции {opcode}")
    values = tuple((word >> field.first_bit) & field.max_value
                   for field in fmt.fields)
    return Instruction(fmt, values)
