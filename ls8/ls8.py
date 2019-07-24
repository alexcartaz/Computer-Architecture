#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
#cpu.trace()
cpu.run()

'''
LDI = 0b01000111
test = 0b00010011

print(test)
'''
