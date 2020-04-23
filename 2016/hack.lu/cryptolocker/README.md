# cryptolocker

The key observation here was that we could guess two bytes of the password, attempt to decrypt the ciphertext, and immediately know if our decryption was valid because we could check if there were 16 bytes of padding. We know that there should be 16 bytes of padding because when we decrypt a ciphertext, we're left with another valid ciphertext, and a valid ciphertext needs to be a multiple of 32. The only time this isn't true is for the last two bytes of the password, where we decode the ciphertext into the flag file. In this case, we remove the check for 16 padding bytes, and print out matches for any valid padding. There was one decryption that resulted in a valid padding of 28, and these were the last two characters

``` abap
#!/usr/bin/env python3

from AESCipher import *
import hashlib
import string

ciphertext = open('flag.encrypted', 'rb').read()

# These are the characters we recovered. After recovering two characters, we
# would decrypt the ciphertext with those characters before continuing to brute
# force the next two characters. So for example, after discovering that the last
# two bytes of the password were '4D' we would comment in the following two lines.

# ciphertext = AESCipher(hashlib.sha256('4D'.encode('utf-8')).digest()).decrypt(ciphertext)
# ciphertext = AESCipher._unpad(ciphertext)
# ciphertext = AESCipher(hashlib.sha256('WH'.encode('utf-8')).digest()).decrypt(ciphertext)
# ciphertext = AESCipher._unpad(ciphertext)
# ciphertext = AESCipher(hashlib.sha256('52'.encode('utf-8')).digest()).decrypt(ciphertext)
# ciphertext = AESCipher._unpad(ciphertext)

# ciphertext = AESCipher(hashlib.sha256('Sg'.encode('utf-8')).digest()).decrypt(ciphertext)
# ciphertext = AESCipher._unpad(ciphertext)
# open('flag', 'wb').write(ciphertext)

for i in string.printable:
    for j in string.printable:
        s = (i + j).encode('utf8')

        k = hashlib.sha256(s).digest()
        decrypted = AESCipher(k).decrypt(ciphertext)
        last = decrypted[-1]

        valid = True
        for c in decrypted[-last:]:
            if c != last:
                valid = False
                break

        # comment this out for the last two bytes
        if (len(decrypted) - last) % 16 != 0:
            valid = False

        if valid:
            print(s, last)
```

After decrypting the file, you will have an ODT file that contains the flag: flag{v3ry_b4d_crypt0_l0ck3r}
