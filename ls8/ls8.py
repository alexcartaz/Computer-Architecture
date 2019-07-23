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
test = 0b00010001

print(test)
'''
'''
dict = {
  130: 'LDI',
  131: 'b',
  71: 'PRN'
}

print(dict[LDI])
'''