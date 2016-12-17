#! /usr/bin/env python

from lxml import html
import requests
import re
import pandas as pd
import os.path as path

cache_dir = './cache'
history_cache = path.join(cache_dir, 'historical')

# screen scrape playlists to build a historical set
# of tracks for comparision to the a-z
historical_playlist = pd.DataFrame(None, columns=('Artist', 'Title'))
days = pd.date_range(start='11/1/2016', end='11/29/2016')
for day in days:
    day_s = "%02d-%02d-%04d" % (day.month, day.day, day.year)
    cache_file = path.join(history_cache, "%s.csv" % day_s)
    if path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        rows = []
        page = requests.post('http://xpn.org/playlists/xpn-playlist',
                             data = {'playlistdate': day_s})
        tree = html.fromstring(page.content)
        tracks = tree.xpath('//h3/a/text()')
        # not all rows are tracks, some are membership callouts
        # but real tracks start with times and are formatted
        # HH:MM [am|pm] Artist - Title
        # Special programs like World Cafe, Echos, ...
        # also start eith time, but don't have useful track info
        # but those list the program inside bars
        # eg |World Cafe| -  "Wednesday 11-2-2016 Hour 2, Part 7"
        date_regex = re.compile("^\d{2}:\d{2}\s")
        for track in tracks:
            if date_regex.match(track) and track[9:10] != '|':
                rows.append(track[9:].split(' - ', 1))
        df = pd.DataFrame(rows, columns = ('Artist', 'Title'))
        df.to_csv(cache_file, index=False)

    historical_playlist = historical_playlist.append(df, ignore_index=True)
    print "adding %d tracks for running total of %d" % \
        (len(df), len(historical_playlist))

print "%d tracks over %d days" % (len(historical_playlist), len(days))






      
