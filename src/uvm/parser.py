"""Разбор текста на языке ассемблера УВМ.

Формат строки::

    МНЕМОНИКА операнд, операнд, ...   ; комментарий

Мнемоники не зависят от регистра. Операнды — неотрицательные целые
числа в десятичной (``127``) или шестнадцатеричной (``0x7F``) записи.
Пустые строки и строки-комментарии пропускаются.
"""

from .ir import Instruction
from .spec import BY_MNEMONIC

COMMENT = ";"
SEPARATOR = ","
HEX_PREFIX = "0x"
HEX_BASE = 16
DEC_BASE = 10
MINUS = "-"


class AsmError(Exception):
    """Ошибка в тексте программы на языке ассемблера."""

    def __init__(self, line, message):
        """Сохранить номер строки и описание ошибки."""
        super().__init__(f"строка {line}: {message}")
        self.line = line


def parse_number(text, line):
    """Преобразовать запись числа в int."""
    lowered = text.lower()
    if lowered.startswith(MINUS):
        raise AsmError(line, f"отрицательное число {text}")
    base = HEX_BASE if lowered.startswith(HEX_PREFIX) else DEC_BASE
    try:
        return int(lowered, base)
    except ValueError as problem:
        message = f"ожидалось число, получено {text!r}"
        raise AsmError(line, message) from problem


def split_operands(text, line):
    """Разделить операнды по запятым."""
    if not text.strip():
        return []
    parts = [part.strip() for part in text.split(SEPARATOR)]
    if not all(parts):
        raise AsmError(line, "пустой операнд")
    return parts


def check_range(field, value, line):
    """Проверить, что значение помещается в поле команды."""
    if value > field.max_value:
        raise AsmError(line, f"поле {field.name}: {value} не помещается в "
                             f"{field.width} бит (максимум "
                             f"{field.max_value})")


def parse_line(raw, line):
    """Разобрать одну строку; вернуть ``Instruction`` или None."""
    text = raw.split(COMMENT, 1)[0].strip()
    if not text:
        return None
    mnemonic, _space, rest = text.partition(" ")
    fmt = BY_MNEMONIC.get(mnemonic.upper())
    if fmt is None:
        raise AsmError(line, f"неизвестная команда {mnemonic!r}")
    operands = split_operands(rest, line)
    if len(operands) != len(fmt.fields):
        raise AsmError(line, f"{fmt.mnemonic}: ожидалось операндов: "
                             f"{len(fmt.fields)}, получено: "
                             f"{len(operands)}")
    values = []
    for field, operand in zip(fmt.fields, operands):
        value = parse_number(operand, line)
        check_range(field, value, line)
        values.append(value)
    return Instruction(fmt, tuple(values), line)


def parse_program(text):
    """Перевести текст программы в список команд (промежуточный вид)."""
    program = []
    for number, raw in enumerate(text.splitlines(), start=1):
        instruction = parse_line(raw.replace("\t", " "), number)
        if instruction is not None:
            program.append(instruction)
    return program
