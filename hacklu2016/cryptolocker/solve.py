#!/usr/bin/env python3

from AESCipher import *
import hashlib
import string

ciphertext = open('flag.encrypted', 'rb').read()

ciphertext = AESCipher(hashlib.sha256('4D'.encode('utf-8')).digest()).decrypt(ciphertext)
ciphertext = AESCipher._unpad(ciphertext)
ciphertext = AESCipher(hashlib.sha256('WH'.encode('utf-8')).digest()).decrypt(ciphertext)
ciphertext = AESCipher._unpad(ciphertext)
ciphertext = AESCipher(hashlib.sha256('52'.encode('utf-8')).digest()).decrypt(ciphertext)
ciphertext = AESCipher._unpad(ciphertext)

ciphertext = AESCipher(hashlib.sha256('Sg'.encode('utf-8')).digest()).decrypt(ciphertext)
ciphertext = AESCipher._unpad(ciphertext)
open('flag', 'wb').write(ciphertext)
# for i in string.printable:
#     for j in string.printable:
#         s = (i + j).encode('utf8')

#         k = hashlib.sha256(s).digest()
#         decrypted = AESCipher(k).decrypt(ciphertext)
#         last = decrypted[-1]

#         valid = True
#         for c in decrypted[-last:]:
#             if c != last:
#                 valid = False
#                 break

#         if (len(decrypted) - last) % 16 != 0:
#             valid = False

#         if valid:
#             print(s, last)
