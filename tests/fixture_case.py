"""Базовый класс тестов: подготовка окружения и временные файлы."""

import os
import tempfile
import unittest


class FixtureCase(unittest.TestCase):
    """Тест, который перед запуском вызывает метод ``prepare``.

    Используется вместо ``setUp``, чтобы имена методов соответствовали
    PEP8 (snake_case).
    """

    def prepare(self):
        """Подготовить окружение теста (по умолчанию ничего не делает)."""

    def run(self, result=None):
        """Подготовить окружение и выполнить тест."""
        self.prepare()
        return super().run(result)

    def temp_path(self, name):
        """Путь к файлу во временном каталоге теста."""
        folder = tempfile.mkdtemp()
        self.addCleanup(lambda: [os.remove(os.path.join(folder, f))
                                 for f in os.listdir(folder)])
        return os.path.join(folder, name)

    def write_file(self, name, text):
        """Создать временный файл с текстом и вернуть путь."""
        path = self.temp_path(name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path
