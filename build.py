import os
import subprocess
import sys

# Пути файлов
ASM_FILE = "tests/program.asm"  # Имя файла с ассемблерным кодом
BIN_FILE = "tests/program.bin"  # Имя выходного бинарного файла
LOG_FILE = "tests/log.xml"      # Имя файла логов
RESULT_FILE = "tests/result.xml"  # Имя файла результатов
TESTS = ["test_assembler.py", "test_interpreter.py"]  # Тестовые файлы
MEMORY_START = 0          # Начальный адрес памяти для интерпретатора
MEMORY_END = 5            # Конечный адрес памяти для интерпретатора

def assemble():
    """Собирает бинарный файл из ассемблерного кода."""
    print("Ассемблируем исходный код...")
    result = subprocess.run(["python", "assembler.py", ASM_FILE, BIN_FILE, LOG_FILE])
    if result.returncode != 0:
        print("Ошибка при ассемблировании. Проверьте исходный код.")
        sys.exit(1)
    print(f"Сборка завершена. Лог записан в {LOG_FILE}")

def interpret():
    """Интерпретирует бинарный файл."""
    print("Интерпретируем бинарный файл...")
    result = subprocess.run(["python", "interpreter.py", BIN_FILE, RESULT_FILE, str(MEMORY_START), str(MEMORY_END)])
    if result.returncode != 0:
        print("Ошибка при интерпретации. Проверьте бинарный файл.")
        sys.exit(1)
    print(f"Интерпретация завершена. Результат записан в {RESULT_FILE}")

def run_tests():
    """Запускает тесты для проверки сборки."""
    print("Запуск тестов...")
    for test in TESTS:
        result = subprocess.run(["python", "-m", "unittest", test])
        if result.returncode != 0:
            print(f"Ошибка при выполнении тестов: {test}")
            sys.exit(1)
    print("Все тесты успешно пройдены.")

def main():
    """Основная функция сборки проекта."""
    if not os.path.exists(ASM_FILE):
        print(f"Ошибка: файл {ASM_FILE} не найден.")
        sys.exit(1)
    
    assemble()
    interpret()
    run_tests()
    print("Проект успешно собран.")

if __name__ == "__main__":
    main()
