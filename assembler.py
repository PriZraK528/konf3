import struct
import sys

def assemble_load(opcode, reg_b, const):
    """Формирует команду LOAD."""
    # Формируем 38-битную команду
    full_bits = (const << 7) | (reg_b << 3) | opcode

    # Извлекаем байты справа налево
    byte1 = full_bits & 0xFF
    byte2 = (full_bits >> 8) & 0xFF
    byte3 = (full_bits >> 16) & 0xFF
    byte4 = (full_bits >> 24) & 0xFF
    byte5 = (full_bits >> 32) & 0xFF

    return bytes([byte1, byte2, byte3, byte4, byte5])


def assemble_read(opcode, reg_b, reg_c):
    """Формирует команду READ."""
    # Формируем 11-битную команду
    full_bits = (reg_c << 7) | (reg_b << 3) | opcode

    # Извлекаем байты справа налево
    byte1 = full_bits & 0xFF
    byte2 = (full_bits >> 8) & 0xFF

    # Дополняем до 5 байтов нулями
    return bytes([byte1, byte2, 0x00, 0x00, 0x00])


def assemble_write(opcode, reg_b, offset, reg_d):
    """Формирует команду WRITE."""
    # Формируем 23-битную команду
    full_bits = (reg_d << 19) | (offset << 7) | (reg_b << 3) | opcode

    # Извлекаем байты справа налево
    byte1 = full_bits & 0xFF
    byte2 = (full_bits >> 8) & 0xFF
    byte3 = (full_bits >> 16) & 0xFF

    return bytes([byte1, byte2, byte3, 0x00, 0x00])


def assemble_cmp_ge(opcode, reg_b, reg_c, reg_d):
    """Формирует команду CMP_GE."""
    # Формируем 15-битную команду
    full_bits = (reg_d << 11) | (reg_c << 7) | (reg_b << 3) | opcode

    # Извлекаем байты справа налево
    byte1 = full_bits & 0xFF
    byte2 = (full_bits >> 8) & 0xFF

    # Дополняем до 5 байтов нулями
    return bytes([byte1, byte2, 0x00, 0x00, 0x00])


def assemble_line(line):
    """Преобразует строку ассемблерного кода в машинный код."""
    parts = line.split()
    cmd = parts[0].upper()

    if cmd == "LOAD":
        opcode = 5
        reg_b = int(parts[1].rstrip(","))
        const = int(parts[2])
        return assemble_load(opcode, reg_b, const)

    elif cmd == "READ":
        opcode = 1
        reg_b = int(parts[1].rstrip(","))
        reg_c = int(parts[2])
        return assemble_read(opcode, reg_b, reg_c)

    elif cmd == "WRITE":
        opcode = 2
        reg_b = int(parts[1].rstrip(","))
        offset = int(parts[2].rstrip(","))
        reg_d = int(parts[3])
        return assemble_write(opcode, reg_b, offset, reg_d)

    elif cmd == "CMP_GE":
        opcode = 7
        reg_b = int(parts[1].rstrip(","))
        reg_c = int(parts[2].rstrip(","))
        reg_d = int(parts[3])
        return assemble_cmp_ge(opcode, reg_b, reg_c, reg_d)

    else:
        raise ValueError(f"Unknown command: {cmd}")


def assemble_file(input_file, output_file, log_file):
    """Ассемблирует файл ассемблерного кода в бинарный файл."""
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile, open(log_file, 'w') as logfile:
        for line in infile:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Пропуск пустых строк и комментариев
            machine_code = assemble_line(line)
            outfile.write(machine_code)

            # Логируем инструкцию
            logfile.write(f"{line} => {' '.join(f'{byte:02X}' for byte in machine_code)}\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    try:
        assemble_file(input_file, output_file, log_file)
        print(f"Assembly completed: {output_file}, log: {log_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
