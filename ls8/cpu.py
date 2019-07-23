"""CPU functionality."""

import sys
#_opcode_'s
LDI = 0b10000010 #Load (LD) Immediate (I)
PRN = 0b01000111 #Print
HLT = 0b00000001 #Halt

def hex_to_dec(hex):
    return int(hex,16)

def binary_to_dec(binary):
    return int(binary,2)

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 8
        self.pc = 0
        self.reg = [None] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def read_memory(self):
        return self.ram[self.pc]

    def write_memory(self, value):
        self.ram[self.pc] = value

    def increment_pc(self):
        if self.pc == 7:
            self.pc = 0
        else:
            self.pc += 1

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.read_memory()

            #case statement
            if command == LDI:
                self.increment_pc()
                reg_address = self.read_memory()
                self.increment_pc()
                self.reg[reg_address] = self.read_memory()
            elif command == PRN:
                self.increment_pc()
                print(self.reg[self.read_memory()])
            elif command == HLT:
                running = False
            else:
                print("Unknown command")
                print("command: " + str(command))
                sys.exit(1)

            #iterate pc
            #I suspect I will have to remove from mem and write from mem to execute
            #code from files w/ more than 8 lines of code
            self.increment_pc()
