import unittest
from assembler import assemble_load, assemble_read, assemble_write, assemble_cmp_ge

class TestAssembler(unittest.TestCase):
    def test_load(self):
        opcode = 5
        reg_b = 5
        const = 328
        expected = bytes([0x2D, 0xA4, 0x00, 0x00, 0x00])
        self.assertEqual(assemble_load(opcode, reg_b, const), expected)

    def test_read(self):
        opcode = 1
        reg_b = 15
        reg_c = 8
        expected = bytes([0x79, 0x04, 0x00, 0x00, 0x00])
        self.assertEqual(assemble_read(opcode, reg_b, reg_c), expected)

    def test_write(self):
        opcode = 2
        reg_b = 15
        offset = 243
        reg_d = 9
        expected = bytes([0xFA, 0x79, 0x48, 0x00, 0x00])
        self.assertEqual(assemble_write(opcode, reg_b, offset, reg_d), expected)

    def test_cmp_ge(self):
        opcode = 7
        reg_b = 0
        reg_c = 4
        reg_d = 4
        expected = bytes([0x07, 0x22, 0x00, 0x00, 0x00])
        self.assertEqual(assemble_cmp_ge(opcode, reg_b, reg_c, reg_d), expected)

if __name__ == "__main__":
    unittest.main()
