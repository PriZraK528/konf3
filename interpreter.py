import xml.etree.ElementTree as ET
import sys

REGISTERS = [0] * 32
MEMORY = [0] * 512

def execute_command(command):
    """Выполняет команду."""
    opcode = command[0] & 0x07
    reg_b = (command[0] >> 3) & 0x0F
    remaining_bit = (command[0] >> 7) & 0x01

    if opcode == 5:  # Загрузка константы
        const = (remaining_bit | (command[1] << 1) | (command[2] << 9) | (command[3] << 17) | (command[4] << 25))
        REGISTERS[reg_b] = const

    elif opcode == 1:  # Чтение значения из памяти
        reg_c = (remaining_bit | (command[1] << 1)) & 0x0F
        mem_addr = REGISTERS[reg_c]
        REGISTERS[reg_b] = MEMORY[mem_addr]

    elif opcode == 2:  # Запись значения в память
        offset = (remaining_bit | (command[1] << 1) | (command[2] & 0x07) << 9)
        reg_d = (command[2] >> 3) & 0x0F
        mem_addr = REGISTERS[reg_b] + offset
        MEMORY[mem_addr] = REGISTERS[reg_d]

    elif opcode == 7:  # Бинарная операция ">="
        reg_c = (remaining_bit | (command[1] << 1)) & 0x0F
        reg_d = (command[1] >> 3) & 0x0F
        REGISTERS[reg_b] = 1 if REGISTERS[reg_d] >= REGISTERS[reg_c] else 0

def interpret(binary_file, result_file, start, end):
    """Интерпретирует бинарный файл."""
    with open(binary_file, 'rb') as f:
        binary = f.read()

    pc = 0  # Program Counter
    while pc < len(binary):
        # Определяем длину команды по opcode
        opcode = binary[pc] & 0x07

        if opcode == 5:  # LOAD
            if pc + 5 > len(binary):
                raise ValueError(f"Неверная длина команды LOAD на позиции {pc}")
            command = binary[pc:pc + 5]
            pc += 5
        elif opcode in [1, 7]:  # READ, CMP_GE
            if pc + 5 > len(binary):
                raise ValueError(f"Неверная длина команды {opcode} на позиции {pc}")
            command = binary[pc:pc + 5]
            pc += 5
        elif opcode == 2:  # WRITE
            if pc + 5 > len(binary):
                raise ValueError(f"Неверная длина команды WRITE на позиции {pc}")
            command = binary[pc:pc + 5]
            pc += 5
        else:
            raise ValueError(f"Неизвестная команда с opcode {opcode} на позиции {pc}")

        execute_command(command)

    # Сохранение памяти в XML
    root = ET.Element("result")
    for i in range(start, end):
        entry = ET.SubElement(root, "memory", addr=str(i))
        entry.text = str(MEMORY[i])
    tree = ET.ElementTree(root)
    tree.write(result_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    interpret(binary_file, result_file, start, end)
