#!/usr/bin/env python2
import requests
import re

url = "https://cthulhu.fluxfingers.net:1507/"
headers = {"Authorization": "Basic c3VwM3JzM2NyM3R1czNyOm4wYjBkeWM0bmd1M3NteXA0c3N3MHJk"}

visited = []

def solve_challenge(link, spacing = 0):
    global visited
    print " " * spacing + link
    response = requests.get(link, headers=headers)
    try:
        challenge = re.findall("<br>(.+) =", response.text)[0]
        answer = eval(challenge)
    except:
        print response.text
        return

    response = requests.post(link, headers=headers, data={"result" : answer})
    for link_2 in get_links(response.text):
        if link_2 not in visited:
            visited.append(link_2)
            solve_challenge(url + link_2, spacing + 1)

def get_links(text):
    links = []
    for line in text.split(' '):
        res = re.search("href=([^>]+)>", line)
        if res != None:
            links.append(res.group(1))

    return links

response = requests.get(url, headers=headers)

for link in get_links(response.text):
    solve_challenge(url + link)
