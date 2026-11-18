"""Тесты виртуальной машины: команды LOAD, READ, WRITE, SQRT."""

import unittest

from uvm.encoder import encode_program
from uvm.machine import Machine, VmError
from uvm.parser import parse_program

SMALL_MEMORY = 16


def run_source(text, data_size=SMALL_MEMORY):
    """Ассемблировать текст, выполнить и вернуть машину."""
    machine = Machine(encode_program(parse_program(text)), data_size)
    machine.run()
    return machine


class MachineTest(unittest.TestCase):
    """Выполнение отдельных команд."""

    def test_load(self):
        """LOAD записывает константу."""
        self.assertEqual(run_source("LOAD 3, 814").data[3], 814)

    def test_write(self):
        """WRITE копирует ячейку B в ячейку C."""
        machine = run_source("LOAD 1, 7\nWRITE 1, 2")
        self.assertEqual(machine.data[2], 7)

    def test_read_with_offset(self):
        """READ берёт mem[mem[C] + B]."""
        machine = run_source("LOAD 9, 42\nLOAD 0, 5\nREAD 4, 0, 1")
        self.assertEqual(machine.data[1], 42)

    def test_sqrt_through_pointer(self):
        """SQRT пишет корень по адресу из ячейки C."""
        machine = run_source("LOAD 1, 144\nLOAD 2, 7\nSQRT 1, 2")
        self.assertEqual(machine.data[7], 12)

    def test_sqrt_takes_integer_part(self):
        """Для неточного квадрата берётся целая часть корня."""
        machine = run_source("LOAD 1, 10\nLOAD 2, 3\nSQRT 1, 2")
        self.assertEqual(machine.data[3], 3)

    def test_sqrt_bad_pointer(self):
        """Указатель за пределами памяти — ошибка."""
        with self.assertRaisesRegex(VmError, "вне памяти данных"):
            run_source("LOAD 2, 500\nSQRT 1, 2")

    def test_memories_are_separate(self):
        """Запись в данные не меняет память команд."""
        machine = run_source("LOAD 0, 1")
        self.assertEqual(machine.code[0], 0x55)
        self.assertEqual(machine.steps, 1)

    def test_address_out_of_memory(self):
        """Адрес за пределами памяти данных — ошибка."""
        with self.assertRaisesRegex(VmError, "вне памяти данных"):
            run_source("LOAD 100, 1")

    def test_truncated_program(self):
        """Неполная последняя команда — ошибка."""
        machine = Machine(bytes([0x55, 0x00]), SMALL_MEMORY)
        with self.assertRaisesRegex(VmError, "неполная команда"):
            machine.run()


if __name__ == "__main__":
    unittest.main()
