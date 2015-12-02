#!/usr/bin/env python

from pwn import *
from capstone import *

hellojoe = ELF('hellojoe')

verify_funcs = [
    0x6025c5,
    0x602065, 
    0x601b05,
    0x601625,
    0x6010c5
]

# vc_set is the set of all valid input characters, which one disocvers when analyzing the first
# verifier function
vc_set = set()
vc_set.update([c for c in '0123456789abcdef{}'])
# sets1 represent the constraints from the first verifier function, 
# which simply ensures the flag is in the format 9447{...}
sets1 = [{'9'},{'4'},{'4'},{'7'},{'{'}]
for i in xrange(32):
    sets1.append(vc_set)
sets1.append({'}'})
# cl is a list to contain all constraint lists
cl = []
cl.append(sets1)

md = Cs(CS_ARCH_X86, CS_MODE_64)

for i, func in enumerate(verify_funcs):
    constraints = []
    # each verification function will check all 38 bytes
    next_block = func
    for j in xrange(38):
        print j
        disasm = md.disasm(hellojoe.read(next_block,60),next_block)
        # skip first five instructions
        for _ in xrange(5):
            print '\t' + disasm.next().mnemonic
        insn = disasm.next()
        if insn.mnemonic == 'jmp':
            # this character position has no constraints
            constraints.append(vc_set)
            print '\tadded constraints (vc_set)'
            # move to the next block
            next_block = int(insn.op_str,16)
            continue
        poss_chars = set()
        while insn.mnemonic != 'xor':
            if insn.mnemonic == 'cmp':
                # add char to the set
                c = chr(int(insn.op_str.split(',')[1],16))
                poss_chars.add(c)
            elif insn.mnemonic == 'je':
                next_block = int(insn.op_str,16)
            insn = disasm.next()
        constraints.append(poss_chars)
        print '\tadded constraints {0}'.format(poss_chars)
    cl.append(constraints)

flag = ''
# for each character position, take the intersection of the sets of character constraints from each 
# verifier function
for i in xrange(38):
    c = cl[0][i] & cl[1][i] & cl[2][i] & cl[3][i] & cl[4][i] & cl[5][i]
    flag += c.pop()
print flag
print 'Done.'
