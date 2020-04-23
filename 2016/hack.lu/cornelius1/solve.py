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
