"""CPU functionality."""

import sys
#_opcode_'s

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
        self.sp = 256
        self.operations = {
            0b10000010: 'self.op_ldi()',
            0b01000111: 'self.op_prn()',
            0b10100010: 'self.op_alu("MUL")',
            0b00000001: 'self.op_hlt()',
            0b01000101: 'self.op_push()',
            0b01000110: 'self.op_pop()',
        }

    def read_memory(self, address=None):
        if address == None:
            address = self.pc
        return self.ram[address]

    def write_memory(self, address, value):
        self.ram[address] = value

    def increment_pc(self):
        self.pc += 1

    def load(self):
        """Load a program into memory."""
        f = open("ls8/examples/stack.ls8", "r")
        for s in f:
            if s[0].isdigit():
                s = '0b' + s[0:8]
                self.write_memory(self.pc,(int(s,2)))
                self.increment_pc()
        self.pc = 0

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] = self.reg[reg_a] - self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        else:
            #raise Exception("Unsupported ALU operation")
            print("Unsupported ALU operation: " + op)
    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(self.ram)

    def run(self):
        """Run the CPU."""
        while True:
            op_id = self.read_memory()
            if op_id not in self.operations:
                self.op_unknown(op_id)
                sys.exit(1)
            else:
                eval(self.operations.get(op_id))
            self.increment_pc()

    def op_ldi(self):
        print('LDI')
        self.increment_pc()
        reg_address = self.read_memory()
        self.increment_pc()
        self.reg[reg_address] = self.read_memory()

    def op_prn(self):
        print('PRN')
        self.increment_pc()
        #print('prn reg[x]: ' + str(self.read_memory()))
        print(self.reg[self.read_memory()])

    def op_alu(self, op):
        print('MUL')
        self.increment_pc()
        reg_a = self.read_memory()
        self.increment_pc()
        reg_b = self.read_memory()
        self.alu(op,reg_a,reg_b)

    def op_push(self):
        print('PUSH')
        #may need to add a check to make sure sp is not < pc
        self.increment_pc()
        self.sp-=1
        self.write_memory(self.sp, self.reg[self.read_memory()])

    def op_pop(self):
        print('POP')
        self.increment_pc()
        self.reg[self.read_memory()] = self.read_memory(self.sp)
        self.write_memory(self.sp, None)
        self.sp+=1

    def op_hlt(self):
        print('HLT')
        sys.exit(1)
        #running = False

    def op_unknown(self, op_id):
        print("Unknown command")
        print("command: " + str(command))
        sys.exit(1)
            
