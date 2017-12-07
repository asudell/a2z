#! /usr/bin/env python

from lxml import html
import requests
from datetime import date, datetime, time
import re
import sys
import pandas as pd
import os.path as path

playlist_url = 'http://xpn.org/playlists/xpn-playlist'

start_time = datetime(2017, 11, 29, 06, 00)
end_time = datetime.now()

cronology = pd.DataFrame(None, columns=('Title', 'Artist', 'Air Time'))
for day in pd.date_range(start_time.date(), end_time.date()):
    day_s = '%02d-%02d-%04d' % (day.month, day.day, day.year)
    
    page = requests.post(playlist_url, data = {'playlistdate': day_s})
    tree = html.fromstring(page.content)
    tracks = tree.xpath('//h3/a/text()')
    # not all rows are tracks, some are membership callouts
    # but real tracks start with times and are formatted
    # HH:MM [am|pm] Artist - Title
    # Special programs like World Cafe, Echos, ...
    # also start with time, but don't have useful track info
    # but those list the program inside bars
    # eg |World Cafe| -  "Wednesday 11-2-2016 Hour 2, Part 7"
    date_regex = re.compile('^\d{2}:\d{2}\s')
    for track in tracks:
        if date_regex.match(track) and track[9:10] != '|':
            hour = int(track[:2])
            minute = int(track[3:5])
            if hour == 12:
                hour = 0
            if track[6:8] == 'pm':
                hour += 12
            air_time = datetime.combine(day, time(hour, minute))
            (artist, title) = track[9:].split(' - ', 1)
            if air_time >= start_time:
                cronology = cronology.append({'Title': title,
                                              'Artist': artist,
                                              'Air Time': air_time},
                                             ignore_index=True)
cronology = cronology.sort_values(by = 'Air Time')
print 'loaded %d songs' % len(cronology)
cronology.to_csv('cache/xpn/airtimes_70s.csv', index=False)
            
            

