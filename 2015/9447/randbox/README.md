This service has 10 "levels" and each level required that you decrypt a ciphertext through the use of an encryption oracle. The following script automatically completes levels 1 through 9. We completed the 10th level manually, but it was just a simple permutation cipher that also mapped `abcdef` to `badcfe`. By sending the alphabet as our plaintext it was trivial to recover the permutation and decrypt the ciphertext. The server then returned the flag to us: `9447{crYpt0_m4y_n0T_Be_S0_haRD}`

```python
#!/usr/bin/env python2

from pwn import *

def solve1():
    r.recvuntil('encrypts to ')
    val = r.recvline().strip()
    val = val[1:-1]
    r.recv()
    key = '1234567890abcdef'
    r.sendline(key)
    mapping = r.recv().strip()
    s = ''
    for c in val:
        s += key[mapping.index(c)]

    log.info(s)
    r.sendline(s)

def solve2():
    r.recvuntil('encrypts to ')
    val = r.recvline().strip()[1:-1]
    r.recv()
    r.sendline(val)
    res = r.recvline().strip()
    shift = val.index(res[:3])
    s = val[-shift:] + val[:-shift]
    r.sendline(s)
    log.info(s)

def solve3():
    solve1()

def solve4():
    solve1()

def solve5():
    solve1()

def solve6():
    r.recvuntil('encrypts to ')
    val = r.recvline().strip()[1:-1]
    r.recv()
    r.sendline('0'*32)
    res = r.recvline().strip()
    mappings = [res]
    for i in range(1, 16):
        mapping = ''
        for j in range(32):
            mapping += hex((int(res[j], 16) + i) % 16)[-1]
        mappings.append(mapping)

    answer = ''
    for i in range(32):
        c = val[i]
        for j in range(16):
            if mappings[j][i] == c:
                answer += hex(j)[-1]
                break
    log.info(answer)
    r.sendline(answer)

def solve7():
    r.recvuntil('encrypts to ')
    val = r.recvline().strip()[1:-1]
    r.recv()

    r.sendline(val[0])
    res = r.recvline().strip()
    r.recv()

    for i in range(31):
        for j in range(16):
            guess = hex(j)[-1]
            result = seven_algo(res + guess, val[0])
            if val.startswith(result):
                res += guess
                break
        if len(res) != i + 2:
            print i, len(res)
            print 'Missed one'
            break
    r.sendline(res)
    log.info(res)

def seven_algo(a, first):
    res = first
    a = [int(x, 16) for x in a]
    for i in range(1, len(a)):
        res += hex(a[i] ^ a[i-1])[-1]

    return res

def solve8():
    r.recvuntil('encrypts to ')
    val = r.recvline().strip()[1:-1]
    print val
    r.recv()

    r.sendline('0')
    shift = 16 - int(r.recvline().strip(), 16)
    res = hex(int(val[0], 16) + shift)[-1]
    for i in range(1, 32):
        res += hex((int(val[i], 16) - int(val[i-1], 16))%16)[-1]

    log.info(res)
    r.sendline(res)

def solve9():
    solve7()

r = remote('randBox-iw8w3ae3.9447.plumbing', 9447)
solve1()
solve2()
solve3()
solve4()
solve5()
solve6()
solve7()
solve8()
solve9()

r.interactive()
```
