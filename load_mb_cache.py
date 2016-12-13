#! /usr/bin/env python

from lxml import html
import requests
import os.path as path
import csv
import pandas as pd
import musicbrainzngs as mb

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
playlist = pd.DataFrame(rows, columns=('Artist', 'Title'))
print "playlist has %d rows" % len(playlist)

mb_rows = []
mb_cache = path.join(cache_dir, 'musicbrainz', 'song_years.csv')
if path.exists(mb_cache):
    with open(mb_cache, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mb_rows.append([row[0], row[1], int(row[2])])
years = pd.DataFrame(mb_rows, columns=('Artist', 'Title', 'Year'))
print "cached years has %d rows" % len(years)

tmplist = playlist.join(years, how='left', rsuffix='_mb')
tmplist = tmplist.drop(['Artist_mb', 'Title_mb'], 1)

if tmplist.isnull().any().any():
    mb.set_useragent('xpn-a2z',
                     '0.1',
                     'https://github.com/asudell/a2z')
    new_mb_rows = []
    for index, row in tmplist[tmplist['Year'].isnull()].iterrows():
        result = mb.search_releases(row['Title'],
                                    artist = row['Artist'],
                                    limit=25)
        rel_year = None
        if result['release-list']:
            for release in  result['release-list']:
                if 'date' in release:
                    y = int(release['date'].split('-')[0])
                    if rel_year is None or rel_year > y:
                        rel_year = y
        if rel_year is not None:
            new_mb_rows.append([row['Artist'], row['Title'], rel_year])

    if len(new_mb_rows) > 0:
        print "fetched %d new rows" % len(new_mb_rows)
        mb_rows.extend(new_mb_rows)
        print "saving cache with %d rows" % len(mb_rows) 
        with open(mb_cache, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in mb_rows:
                writer.writerow(row)
                
    years = pd.DataFrame(mb_rows, columns=('Artist', 'Title', 'Year'))
    playlist = playlist.join(years, how='left', rsuffix='_mb')
    playlist = playlist.drop(['Artist_mb', 'Title_mb'], 1)
    playlist['Year'] = playlist['Year'].fillna(0.0).astype(int)
    
else:
    playlist = tmplist

print playlist.describe()
print "resulting playlist has %d missing years" \
    % len(playlist[playlist['Year'] == 0])
        
        
    

                         


