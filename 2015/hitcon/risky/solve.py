#!/usr/bin/env python

from claripy import *
from pwn import *

# if the input has the form AAAA-BBBB-CCCC-DDDD-EEEE, then registers are:
#   s3 = AAAA
#   s2 = BBBB
#   s1 = CCCC
#   s5 = DDDD
#   s0 = EEEE

s0 = BV('s0', 32)
s1 = BV('s1', 32)
s2 = BV('s2', 32)
s3 = BV('s3', 32)
s5 = BV('s5', 32)

s = Solver()

# likely to be only printable chars
for i in xrange(0, 32, 8):
    s.add(s0[i+7:i] >= ord('0'))
    s.add(s0[i+7:i] <= ord('z'))
    s.add(s1[i+7:i] >= ord('0'))
    s.add(s1[i+7:i] <= ord('z'))
    s.add(s2[i+7:i] >= ord('0'))
    s.add(s2[i+7:i] <= ord('z'))
    s.add(s3[i+7:i] >= ord('0'))
    s.add(s3[i+7:i] <= ord('z'))
    s.add(s5[i+7:i] >= ord('0'))
    s.add(s5[i+7:i] <= ord('z'))

s.add(0x4978d844 == s3 * s0)
s.add(0x9bcd30de == s2 * s1)
s.add(0x313ac784 == s1 * s5)
s.add(0xe3b0cdef == s1 + s2 + s0)
s.add(0x181a9c5f == (s1*s5) +(s3*s2) + s0)
s.add(0x2deacccb == (s3*s1) + (s2+s0))
s.add(0x8e2f6780 == s3 + s2 + s1 + s0 + s5)
s.add(0xb3da7b5f == (s0+s1+s2) * (s3+s5))
s.add(0x41c7a3a0 == (s1*s5) * (s2*s1) *s0)

if s.satisfiable():
    print 'Satisfiable'
    model = s.result.model
    a = model['s3_3_32'].value
    b = model['s2_2_32'].value
    c = model['s1_1_32'].value
    d = model['s5_4_32'].value
    e = model['s0_0_32'].value
    print 'Key: {0}-{1}-{2}-{3}-{4}'.format(p32(a), p32(b), p32(c), p32(d), p32(e))

    aa = a ^ 0x2c280d2f
    bb = b ^ 0x38053525
    cc = c ^ 0x6b5c2a24
    dd = d ^ 0x27542728
    ee = e ^ 0x2975572f
    print 'Flag: hitcon{%s}' % (p32(aa)+p32(bb)+p32(cc)+p32(dd)+p32(ee))
else:
    print 'Balls.'


