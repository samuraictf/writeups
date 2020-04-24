#!/usr/bin/env python2

import zlib

f = open('simplepdf_f8004a3ad0acde31c40267b9856e63fc.pdf').read()
open('dump.out', 'w').write(f)

while True:
    f = open('dump.out').read()
    index = f.find('6 0 obj')
    start_index = f.find('/Length', index)
    end_index = f.find('\n', start_index)
    length = int(f[start_index + 8:end_index].strip())
    stream = f.find('stream', end_index)
    new_file = f[stream + 7:stream + 7 + length]
    open('dump.out', 'w').write(zlib.decompress(new_file))
