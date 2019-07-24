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
        self.fl = 0b00000000
        self.operations = {
            0b10000010: 'self.op_ldi()',
            0b01000111: 'self.op_prn()',
            0b10100000: 'self.op_alu("ADD")',
            0b10100010: 'self.op_alu("MUL")',
            0b00000001: 'self.op_hlt()',
            0b01000101: 'self.op_push()',
            0b01000110: 'self.op_pop()',
            0b01010000: 'self.op_call()',
            0b00010001: 'self.op_ret()',
            0b10100111: 'self.op_alu("CMP")',
            0b01010100: 'self.op_jmp()',
            0b01010101: 'self.op_jeq()',
            0b01010110: 'self.op_jne()',
        }

    def read_memory(self, address=None):
        if address == None:
            address = self.pc
        return self.ram[address]

    def write_memory(self, address, value):
        self.ram[address] = value

    def increment_pc(self):
        self.pc += 1
        #print(self.pc)

    def load(self):
        """Load a program into memory."""
        f = open("ls8/examples/sprint.ls8", "r")
        for s in f:
            if s[0].isdigit():
                s = '0b' + s[0:8]
                self.write_memory(self.pc,(int(s,2)))
                self.increment_pc()
        self.pc = 0
        #print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] = self.reg[reg_a] - self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            '''
            CMP - This is an instruction handled by the ALU.
            Compare the values in two registers.
            FL bits: 00000LGE
            '''
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
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
        print(self.reg[self.read_memory()])

    def op_alu(self, op):
        print(op)
        self.increment_pc()
        reg_a = self.read_memory()
        self.increment_pc()
        reg_b = self.read_memory()
        self.alu(op,reg_a,reg_b)

    def op_push(self, value=None):
        print('PUSH')
        #may need to add a check to make sure sp is not < pc
        self.increment_pc()
        self.sp-=1
        if value==None:
            value = self.reg[self.read_memory()]
        self.write_memory(self.sp, value)


    def op_pop(self):
        '''
        POP register - Pop the value at the top of the stack into the given register.

        Copy the value from the address pointed to by SP to the given register.
        Increment SP.
        '''
        print('POP')
        self.increment_pc()
        self.reg[self.read_memory()] = self.read_memory(self.sp)
        self.write_memory(self.sp, None)
        self.sp+=1

    def op_call(self):
        '''
        CALL register - Calls a subroutine (function) at the address stored in the register.

        The address of the instruction directly after CALL is pushed onto the stack. 
        This allows us to return to where we left off when the subroutine finishes executing.
        The PC is set to the address stored in the given register. 
        We jump to that location in RAM and execute the first instruction in the subroutine. 
        The PC can move forward or backwards from its current location.
        '''
        print('CALL')
        self.op_push(self.pc+1)
        self.pc = self.reg[self.read_memory()]-1



    def op_ret(self):
        '''
        RET - Return from subroutine.

        Pop the value from the top of the stack and store it in the PC.
        '''
        print('RET')
        self.pc = self.read_memory(self.sp)
        self.write_memory(self.sp, None)
        self.sp+=1

    def op_jmp(self):
        '''
        JMP register - Jump to the address stored in the given register.

        Set the PC to the address stored in the given register.
        '''
        print('JMP')
        self.increment_pc()
        self.pc = self.reg[self.read_memory()]
        self.pc-=1

    def op_jeq(self):
        '''
        JEQ - JEQ register

        If equal flag is set (true), jump to the address stored in the given register.
        '''
        print('JEQ')
        self.increment_pc()
        if self.fl == 0b00000001:
            self.pc = self.reg[self.read_memory()]
            self.pc-=1

    def op_jne(self):
        '''
        JNE register

        If E flag is clear (false, 0), jump to the address stored in the given register.
        '''
        print('JNE')
        self.increment_pc()
        if self.fl != 0b00000001:
            self.pc = self.reg[self.read_memory()]
            self.pc-=1

    def op_hlt(self):
        print('HLT')
        sys.exit(1)
        #running = False

    def op_unknown(self, op_id):
        print("Unknown command")
        print("command: " + str(op_id))
        sys.exit(1)
            
