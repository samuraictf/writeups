# cornelius1

The basic idea of this task is similar to the CRIME TLS bug. The user name we supply will modify the length of the gzipped text, and the length of the gzipped text is preserved after encryption. Thus we can guess the flag prefix character by character, and when we see a shorted encrypted text, that means we matched some characters in the flag. The only tricky part was for some reason when the username we sent was too long, it seems like gzip wasn't compressing the string. So when we sent `flag:Mu7a` as the username, we were unable to get the next character. We had to shrink this to `u7a`.

We ran the script below to get each letter. The script will print the guess and the length of the encrypted text for each guess. When we see a length that is smaller than the others, we update our guess and rerun the script.

``` python
#!/usr/bin/env python2

import requests
import string
import urllib

# Final flag: Mu7aichede
user = 'flag:'
for c in string.printable:
    guess = urllib.quote_plus(user + c)
    r = requests.get('https://cthulhu.fluxfingers.net:1505/?user=%s' % guess)
    l = len(r.cookies.get('auth').decode('base64'))
    print guess, l
```
