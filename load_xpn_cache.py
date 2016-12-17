#! /usr/bin/env python

from lxml import html
import requests
import os.path as path
import pandas as pd

cache_dir = './cache'
xpn_cache = path.join(cache_dir, 'xpn')

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters_so_far = list(alphabet)[:25]

playlist = pd.DataFrame(None, columns = ('Title', 'Artist'))
for letter in letters_so_far:
    cache_file = path.join(xpn_cache, '%s.csv' % letter)
    if path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        rows = []
        page = requests.get('http://xpn.org/static/az.php?q=%s' %  letter)
        tree = html.fromstring(page.content)
        songs = tree.xpath('//li/text()')
        for song in songs:
            rows.append(song.split(' - ', 1))
        df = pd.DataFrame(rows, columns = ('Title', 'Artist'))
        df.to_csv(cache_file, index=False)

    playlist = playlist.append(df, ignore_index=True)
    print "adding %d songs for running total of %d" % (len(df), len(playlist))
    
print "%d songs in %d letters" % (len(playlist), len(letters_so_far))

