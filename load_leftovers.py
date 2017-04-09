#! /usr/bin/env python

from lxml import html
import requests
from datetime import date, datetime, time
import re
import sys
import pandas as pd
import os.path as path

# cach results. The speedup and load reduction is minor,
# but it enables the MusicBrainz load to read the cache
# and that ends up being important
cache_dir = './cache'
playlist_cache = path.join(cache_dir, 'xpn', 'leftovers.csv')

# playlist is fri 7-11, sat 10-5 and sun 12-5
# its helpful that none croses midnight
timeslots = [(datetime(2017, 4, 7, 19, 0), datetime(2017, 4, 7, 23, 0)),
             (datetime(2017, 4, 8, 10, 0), datetime(2017, 4, 8, 17, 0)),
             (datetime(2017, 4, 9, 12, 0), datetime(2017, 4, 9, 17, 0))]

# playlists per day live at /playlists/xpn-playlist
# Not all rows are tracks, some are membership callouts
# but real tracks start with times and are formatted
# HH:MM [am|pm] Artist - Title
# Special programs like World Cafe, Echos, ...
# also start with time, but don't have useful track info
# but those list the program inside bars
# eg |World Cafe| -  "Wednesday 11-2-2016 Hour 2, Part 7"

today = date.today()
date_regex = re.compile("^\d{2}:\d{2}\s")

leftovers = pd.DataFrame(None, columns = ('Title', 'Artist', 'AirTime'))

for slot in timeslots:
    d = slot[0].date()
    if d <= today:
        page = requests.post('http://xpn.org/playlists/xpn-playlist',
                             data={'playlistdate': "%02d-%02d-%04d" % (d.month,
                                                                       d.day,
                                                                       d.year)})
        tree = html.fromstring(page.content)
        tracks = tree.xpath('//h3/a/text()')
        for track in tracks:
                if date_regex.match(track) and track[9:10] != '|':
                    (artist, title) = track[9:].split(' - ', 1)
                    hour = int(track[0:2]) % 12
                    minute = int(track[3:5])
                    if track[6:8] == 'pm': hour += 12
                    air_time = datetime(d.year, d.month, d.day,
                            hour, minute)
                    if slot[0] <= air_time < slot[1]:
                        leftovers = leftovers.append({'Title': title,
                                                      'Artist': artist,
                                                      'AirTime': air_time},
                                                     ignore_index=True)

leftovers = leftovers.sort_values(by = ('AirTime'))
leftovers.to_csv(playlist_cache , index=False)
