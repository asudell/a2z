#! /usr/bin/env python

import os.path as path
import pandas as pd
import musicbrainzngs as mb

cache_dir = './cache'
hist_cache = path.join(cache_dir, 'historical')

# Load up the play lists

playlist = pd.DataFrame(None, columns = ('Artist', 'Title'))
days =  pd.date_range(start='11/1/2016', end='11/29/2016')
for day in days:
    day_s = "%02d-%02d-%04d" % (day.month, day.day, day.year)
    cache_file = path.join(hist_cache, '%s.csv' % day_s)
    if path.exists(cache_file):
        df = pd.read_csv(cache_file)
        playlist = playlist.append(df, ignore_index=True)
    else:
        # asume what we have cached is it
        pass

playlist = playlist.drop_duplicates()
print "playlist has %d rows" % len(playlist)

# Load MusicBrainz Data
mb_cache = path.join(cache_dir, 'musicbrainz', 'hist_years.csv')
if path.exists(mb_cache):
    years = pd.read_csv(mb_cache)
else:
    years = pd.DataFrame(None, columns=('Artist','Title', 'Year'))

print "cached years has %d rows" % len(years)

# merge the two data sets
tmplist = playlist.merge(years, how='left')

def fixup(name):
    # Music Brainz is fussy about some anames
    if "R. E. M." == name:
        return "REM"
    elif "B. T. Express" == name:
        return "BT Express"
    elif "J. J. Cale" == name:
        return "JJ Cale"
    elif "k. d. lang" == name:
        return "kd lang"
    elif "J. J. Jackson" == name:
        return "JJ Jackson"
    elif "B. B. King" == name:
        return "BB King"
    elif "K. T. Tunstall" == name:
        return "KT Tunstall"
    elif "R. L. Burnside" == name:
        return "RL Burnside"
    elif "The J. Geils Band" == name:
        return "The J Giles Band"
    else:
        return name
        
# if there are any null values, query MuicBrainz
# for those songs collect meta data on them
if tmplist.isnull().any().any():
    mb.set_useragent('xpn-a2z',
                     '0.1',
                     'https://github.com/asudell/a2z')
    new_mb_rows = []
    for index, row in tmplist[tmplist['Year'].isnull()].iterrows():
        result = mb.search_recordings(row['Title'],
                                      artist = fixup(row['Artist']),
                                      status = 'official',
                                      strict = True,
                                      limit = 25)
        rel_year = None
        for recording in result['recording-list']:
            
            if recording['release-list']:
                for release in  recording['release-list']:
                    if 'date' in release:
                        y = int(release['date'].split('-')[0])
                        if rel_year is None or rel_year > y:
                            if y > 1900:
                                # assume anything before then is a type
                                # there are a few with missing digits
                                rel_year = y
        if rel_year is not None:
            new_mb_rows.append([row['Artist'], row['Title'], rel_year])

    print "fetched %d new rows" % len(new_mb_rows)
    
    new_years = pd.DataFrame(new_mb_rows, columns=('Artist', 'Title', 'Year'))
    if len(new_years) > 0:
        years = years.append(new_years, ignore_index=True)
        print 'saving cache with %s rows' % len(years)
        years['Year'] = years['Year'].astype(int)
        years.to_csv(mb_cache, index=False)
                

    playlist = playlist.merge(years, how='left')
    playlist['Year'] = playlist['Year'].fillna(0.0).astype(int)
    

print "resulting playlist has %d missing years" \
    % len(playlist[playlist['Year'] == 0])
print
for index, row in playlist[playlist['Year'] == 0].iterrows():
    print row['Artist'], row['Title']
        
        
    

                         


