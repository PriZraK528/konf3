import unittest
import os
import xml.etree.ElementTree as ET
from subprocess import run

class TestAssemblerAndInterpreter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем тестовые файлы
        cls.asm_file = "test_program.asm"
        cls.bin_file = "test_program.bin"
        cls.log_file = "test_log.xml"
        cls.result_file = "test_result.xml"
        
        # Ассемблерный код для теста
        asm_code = """
        # Программа для инициализации значений в памяти и выполнения сравнения
        LOAD 10, 0
        LOAD 11, 1
        LOAD 12, 2
        LOAD 13, 3
        LOAD 14, 4

        LOAD 0, 150      # Загружаем значение 150 в R0
        WRITE 10, 0, 0    # Записываем в память по адресу 0

        LOAD 0, 120      # Загружаем значение 120 в R0
        WRITE 11, 0, 0    # Записываем в память по адресу 1

        LOAD 0, 131      # Загружаем значение 131 в R0
        WRITE 12, 0, 0    # Записываем в память по адресу 2

        LOAD 0, 90       # Загружаем значение 90 в R0
        WRITE 13, 0, 0    # Записываем в память по адресу 3

        LOAD 0, 200      # Загружаем значение 200 в R0
        WRITE 14, 0, 0    # Записываем в память по адресу 4

        LOAD 6, 131      # Загружаем число 131 в R6
        READ 0, 10       # Читаем значение из памяти в R0
        CMP_GE 0, 6, 0   # Сравниваем R6 и R0, результат в R0
        WRITE 10, 0, 0    # Пишем результат сравнения в память

        READ 1, 11       # Читаем значение из памяти в R1
        CMP_GE 1, 6, 1   # Сравниваем R6 и R1, результат в R1
        WRITE 11, 0, 1    # Пишем результат сравнения в память

        READ 2, 12       # Читаем значение из памяти в R2
        CMP_GE 2, 6, 2   # Сравниваем R6 и R2, результат в R2
        WRITE 12, 0, 2    # Пишем результат сравнения в память

        READ 3, 13       # Читаем значение из памяти в R3
        CMP_GE 3, 6, 3   # Сравниваем R6 и R3, результат в R3
        WRITE 13, 0, 3    # Пишем результат сравнения в память

        READ 4, 14       # Читаем значение из памяти в R0
        CMP_GE 4, 6, 4   # Сравниваем R6 и R0, результат в R0
        WRITE 14, 0, 4    # Пишем результат сравнения в память
        """
        with open(cls.asm_file, "w") as f:
            f.write(asm_code.strip())

    @classmethod
    def tearDownClass(cls):
        # Удаляем тестовые файлы
        for file in [cls.asm_file, cls.bin_file, cls.log_file, cls.result_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_assembler(self):
        # Запуск assembler.py
        result = run(["python", "assembler.py", self.asm_file, self.bin_file, self.log_file])
        self.assertEqual(result.returncode, 0, "Assembler завершился с ошибкой.")

        # Проверка, что бинарный файл создан
        self.assertTrue(os.path.exists(self.bin_file), "Бинарный файл не создан.")

        # Проверка логов
        with open(self.log_file, "r") as f:
            log_content = f.read()
        self.assertIn("LOAD", log_content, "Логи не содержат инструкции LOAD.")
        self.assertIn("CMP_GE", log_content, "Логи не содержат инструкции CMP_GE.")

    def test_interpreter(self):
        # Устанавливаем начальную память
        expected_results = [1, 0, 1, 0, 1]

        # Запуск interpreter.py
        result = run(["python", "interpreter.py", self.bin_file, self.result_file, "0", "5"])
        self.assertEqual(result.returncode, 0, "Interpreter завершился с ошибкой.")

        # Проверка результата в XML
        tree = ET.parse(self.result_file)
        root = tree.getroot()
        for i, elem in enumerate(root.findall("memory")):
            self.assertEqual(int(elem.text), expected_results[i], f"Ошибка в памяти на индексе {i}.")

        
if __name__ == "__main__":
    unittest.main()
