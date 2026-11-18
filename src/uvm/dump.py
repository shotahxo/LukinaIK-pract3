"""Диапазон адресов и дамп памяти в формате CSV."""

import csv
import os
import re

RANGE_RE = re.compile(r"^(\d+|0x[0-9a-fA-F]+)[-:](\d+|0x[0-9a-fA-F]+)$")
HEADER = ("address", "value")


class RangeError(Exception):
    """Неверно задан диапазон адресов."""


def parse_range(text, size):
    """Разобрать ``НАЧАЛО-КОНЕЦ`` (включительно) с проверкой границ."""
    match = RANGE_RE.match(text.strip())
    if match is None:
        raise RangeError(f"ожидался диапазон вида 0-31, получено {text!r}")
    start, end = (int(part, 0) for part in match.groups())
    if start > end:
        raise RangeError(f"начало диапазона {start} больше конца {end}")
    if end >= size:
        raise RangeError(f"адрес {end} вне памяти данных (0..{size - 1})")
    return start, end


def save_dump(path, data, start, end):
    """Сохранить ячейки ``start..end`` в CSV: адрес, значение."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        for address in range(start, end + 1):
            writer.writerow((address, data[address]))
