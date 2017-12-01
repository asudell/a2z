#! /usr/bin/env python

from lxml import html
import requests
import os.path as path
import pandas as pd

cache_dir = './cache'
cache_file = path.join(cache_dir, 'xpn', 'seventies.csv')

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWZYZ'
letters_so_far = list(alphabet)[:4]
years = map(str, range(1970,1980))


rows = []
for letter in letters_so_far:
    page = requests.get('http://xpn.org/static/az2017.php?q=%s' % letter)
    tree = html.fromstring(page.content)
    songs = tree.xpath('//li/text()')
    for song in songs:
        rows.append(song.split(' - ', 1) + [letter])

songs_by_letter = pd.DataFrame(rows, columns = ['Title', 'Artist', 'Letter'])
print "got %d songs by letter" % len(songs_by_letter)

rows = []
for year in years:
    page = requests.get('http://xpn.org/static/az2017v2.php?q=%s' % year)
    tree = html.fromstring(page.content)
    songs = tree.xpath('//li/text()')
    for song in songs:
        rows.append(song.split(' - ', 1) + [year])

songs_by_year = pd.DataFrame(rows, columns = ['Title', 'Artist', 'Year'])
print 'got %d songs by year' % len(songs_by_year)

playlist = songs_by_letter.merge(songs_by_year, how='left')
playlist.to_csv(cache_file, index=False)
print "%d songs so far" % len(playlist)


