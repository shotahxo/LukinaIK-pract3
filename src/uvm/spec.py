"""Спецификация учебной виртуальной машины (УВМ), вариант 17.

Каждая команда занимает 7 байт. Поле A (биты 0–7) — код операции,
остальные поля — адреса, смещения и константы. Номера битов считаются
от младшего бита команды; байты записываются от младшего к старшему.
"""

from dataclasses import dataclass

COMMAND_SIZE = 7
OPCODE_BITS = 8


@dataclass(frozen=True)
class Field:
    """Поле команды: имя и диапазон битов (включительно)."""

    name: str
    first_bit: int
    last_bit: int

    @property
    def width(self):
        """Ширина поля в битах."""
        return self.last_bit - self.first_bit + 1

    @property
    def max_value(self):
        """Наибольшее значение, которое помещается в поле."""
        return (1 << self.width) - 1


@dataclass(frozen=True)
class CommandFormat:
    """Формат команды: мнемоника, код операции и поля-операнды."""

    mnemonic: str
    opcode: int
    fields: tuple
    description: str


FORMATS = (
    CommandFormat(
        "LOAD", 85,
        (Field("B", 8, 21), Field("C", 22, 41)),
        "загрузка константы: mem[B] = C",
    ),
    CommandFormat(
        "READ", 245,
        (Field("B", 8, 22), Field("C", 23, 36), Field("D", 37, 50)),
        "чтение из памяти: mem[D] = mem[mem[C] + B]",
    ),
    CommandFormat(
        "WRITE", 31,
        (Field("B", 8, 21), Field("C", 22, 35)),
        "запись в память: mem[C] = mem[B]",
    ),
    CommandFormat(
        "SQRT", 118,
        (Field("B", 8, 21), Field("C", 22, 35)),
        "квадратный корень: mem[mem[C]] = sqrt(mem[B])",
    ),
)

BY_MNEMONIC = {fmt.mnemonic: fmt for fmt in FORMATS}
BY_OPCODE = {fmt.opcode: fmt for fmt in FORMATS}
