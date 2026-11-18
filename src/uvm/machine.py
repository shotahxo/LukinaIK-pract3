"""Модель УВМ: раздельные память команд и память данных, цикл работы."""

import math

from .decoder import decode
from .spec import COMMAND_SIZE

DATA_SIZE = 1 << 16
FIRST_ADDRESS = 0


class VmError(Exception):
    """Ошибка выполнения программы."""


class Machine:
    """Виртуальная машина с памятью команд (байты) и данных (числа)."""

    def __init__(self, code, data_size=DATA_SIZE):
        """Загрузить программу в память команд, обнулить память данных."""
        self.code = bytes(code)
        self.data = [0] * data_size
        self.pc = 0
        self.steps = 0
        self.handlers = {
            "LOAD": self.op_load,
            "READ": self.op_read,
            "WRITE": self.op_write,
            "SQRT": self.op_sqrt,
        }

    def check_address(self, address):
        """Проверить, что адрес лежит в памяти данных."""
        if not FIRST_ADDRESS <= address < len(self.data):
            raise VmError(f"адрес {address} вне памяти данных "
                          f"(0..{len(self.data) - 1})")
        return address

    def load(self, address):
        """Прочитать ячейку памяти данных."""
        return self.data[self.check_address(address)]

    def store(self, address, value):
        """Записать значение в ячейку памяти данных."""
        self.data[self.check_address(address)] = value

    def op_load(self, b, c):
        """LOAD: mem[B] = C."""
        self.store(b, c)

    def op_read(self, b, c, d):
        """READ: mem[D] = mem[mem[C] + B]."""
        self.store(d, self.load(self.load(c) + b))

    def op_write(self, b, c):
        """WRITE: mem[C] = mem[B]."""
        self.store(c, self.load(b))

    def op_sqrt(self, b, c):
        """SQRT: mem[mem[C]] = sqrt(mem[B]), целая часть корня."""
        self.store(self.load(c), math.isqrt(self.load(b)))

    def fetch(self):
        """Прочитать команду по счётчику и перевести её в промежуточный вид."""
        chunk = self.code[self.pc:self.pc + COMMAND_SIZE]
        if len(chunk) < COMMAND_SIZE:
            raise VmError(f"адрес команды {self.pc}: неполная команда "
                          f"({len(chunk)} из {COMMAND_SIZE} байт)")
        return decode(chunk, self.pc)

    def step(self):
        """Выполнить одну команду."""
        instruction = self.fetch()
        handler = self.handlers.get(instruction.mnemonic)
        if handler is None:
            raise VmError(f"команда {instruction.mnemonic} не реализована")
        handler(*instruction.values)
        self.pc += COMMAND_SIZE
        self.steps += 1

    def run(self):
        """Выполнять команды, пока не закончится память команд."""
        while self.pc < len(self.code):
            self.step()
        return self.steps
