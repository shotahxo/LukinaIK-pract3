"""Промежуточное представление команды УВМ."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    """Команда: формат, значения полей и номер строки исходного текста."""

    fmt: object
    values: tuple
    line: int = 0

    @property
    def mnemonic(self):
        """Мнемоника команды."""
        return self.fmt.mnemonic

    def fields(self):
        """Пары (имя поля, значение), начиная с кода операции A."""
        names = [field.name for field in self.fmt.fields]
        return [("A", self.fmt.opcode)] + list(zip(names, self.values))

    def describe(self):
        """Строка вида ``A=85, B=127, C=814``, как в спецификации."""
        return ", ".join(f"{name}={value}" for name, value in self.fields())
