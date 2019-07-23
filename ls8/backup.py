"""CPU functionality."""

import sys
#_opcode_'s
LDI = bin(0b10000010) #Load (LD) Immediate (I)
PRN = bin(0b01000111) #Print
MUL = bin(0b10100010) #Multiply
HLT = bin(0b00000001) #Halt

def hex_to_dec(hex):
    return int(hex,16)

def binary_to_dec(binary):
    return int(binary,2)

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 256
        self.pc = 0
        self.reg = [None] * 8
        self.program = []

    def load(self):
        """Load a program into memory."""
        f = open("ls8/examples/mult.ls8", "r")
        start_pc = self.pc
        for s in f:
            #print(s[0])
            #print(s[0].isdigit())
            if s[0].isdigit():
                s = '0b' + s[0:8]
                print(bin(int(s,2)))
                self.ram.append(int(s,2))
        #self.update_mem_stack()
        print(self.program)

    def update_mem_stack(self):
        self.ram = [None] * 8
        index = self.pc
        running = True
        while running == True:
            #print('self.pc: '  + str(self.pc))
            if index < len(self.program) and index < self.pc + 8:
                self.write_memory(index%8, self.program[index])
                index += 1
            else:
                running = False
        self.trace()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] = bin(int(self.reg[reg_a],2) + int(self.reg[reg_b],2))
        elif op == "SUB":
            self.reg[reg_a] = bin(int(self.reg[reg_a],2) - int(self.reg[reg_b],2))
        elif op == "MUL":
            self.reg[reg_a] = bin(int(self.reg[reg_a],2) * int(self.reg[reg_b],2))
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(self.ram)
        '''
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
        '''
        
    def read_memory(self):
        #print('read_mem -> self.pc: '  + str(self.pc))
        #print(self.ram[self.pc%8])
        #print('self.pc%8: ' + str(self.pc%8))
        if self.pc%8 == 0 and self.pc != 0:
            self.update_mem_stack()
        return self.ram[self.pc%8]

    def write_memory(self, address, value):
        self.ram[address] = value

    def increment_pc(self):
        self.pc += 1

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.read_memory()

            #case statement
            if command == LDI:
                self.increment_pc()
                reg_address = int(self.read_memory(),2)
                self.increment_pc()
                self.reg[reg_address] = self.read_memory()
            elif command == PRN:
                self.increment_pc()
                print(int(self.reg[int(self.read_memory(),2)],2))
            elif command == MUL:
                op = "MUL"
                self.increment_pc()
                reg_a = int(self.read_memory(),2)
                self.increment_pc()
                reg_b = int(self.read_memory(),2)
                self.alu(op,reg_a,reg_b)
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
