"""Перевод команд из промежуточного представления в машинный код.

Поля упаковываются в 56-битное число (A — младшие биты), которое
записывается в 7 байт от младшего к старшему (little-endian).
"""

from .spec import COMMAND_SIZE

BYTE_ORDER = "little"


def encode(instruction):
    """Машинный код одной команды (7 байт)."""
    word = instruction.fmt.opcode
    for field, value in zip(instruction.fmt.fields, instruction.values):
        word |= value << field.first_bit
    return word.to_bytes(COMMAND_SIZE, BYTE_ORDER)


def encode_program(program):
    """Машинный код всей программы."""
    return b"".join(encode(instruction) for instruction in program)


def format_bytes(code):
    """Байты в виде ``0x55, 0x7F, ...``, как в спецификации."""
    return ", ".join(f"0x{byte:02X}" for byte in code)
