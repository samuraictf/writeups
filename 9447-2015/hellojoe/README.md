## hellojoe, reversing challenge from 9447 CTF 2015
#### by dropkick from team Samurai

tl;dr - hellojoe mainly consisted of six functions that each checked the input (i.e., the flag) against a set of possible characters.  The intersection of all the constraints in each 'verifier' function yielded the flag.

The main function of `hellojoe` copied six code segments from the .data section into some freshly mmap()'d executable memory.  It then calls these six functions in random order on `argv[1]`.  If they all return `1`, you have found the flag.

#### Verifier functions
Each verifier function contained 38 blocks of code that all took a similar form, which looked something like this:

```
   0x602685:	rdtsc
   0x602687:	test   eax,0xfffff
   0x60268c:	jne    0x602685
   0x60268e:	movzx  rax,BYTE PTR [rdi]
   0x602692:	inc    rdi
   0x602695:	cmp    al,0x35
   0x602697:	je     0x6026b0
   0x60269d:	cmp    al,0x64
   0x60269f:	je     0x6026b0
   0x6026a5:	cmp    al,0x65
   0x6026a7:	je     0x6026b0
   0x6026ad:	xor    eax,eax
   0x6026af:	ret
```

The blocks either contained a series of (usually three) `cmp` instructions against the current char from the input (38 in total) or it simply skipped to the next character.  The beginning `rdtsc` loop appears to simply waste time and can be ignored.  The important part is the set of characters (again usually three) that are compared against the current input character.  By comparing the possible 'valid' characters for any given position of the input across all six validation functions, you can discover the flag.  I did this more-or-less by hand during the ctf (with a helper IDApython script), then wrote the below python script that leverages the pwntools ELF loader, the capstone disassembly library, and python sets to automate the solution.  

```python
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
```

And the script yields the flag: 
`9447{94ea5e32f2b5b37d947eea3a38932ae1}`

   
