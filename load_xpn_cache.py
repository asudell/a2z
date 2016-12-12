#! /usr/bin/env python

from lxml import html
import requests
import os.path as path
import csv

cache_dir = './cache'
xpn_cache = path.join(cache_dir, 'xpn')

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters_so_far = list(alphabet)[:19]

rows = []
for letter in letters_so_far:
    cache_file = path.join(xpn_cache, '%s.csv' % letter)
    if not path.exists(cache_file):
        with open(cache_file, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            page = requests.get('http://xpn.org/static/az.php?q=%s' %  letter)
            tree = html.fromstring(page.content)
            plays = tree.xpath('//li/text()')
            for play in plays:
                writer.writerow(play.split(' - ', 1))
                rows.append(play.split(' - ', 1))
    else:
        with open(cache_file, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for play in reader:
                rows.append(play)

print "%d songs in %d letters" % (len(rows), len(letters_so_far))

