#! /usr/bin/env python

import os.path as path
import pandas as pd

cache_dir = './cache'
xpn_cache = path.join(cache_dir, 'xpn')

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

playlist = pd.DataFrame(None, columns = ('Title', 'Artist'))
for letter in list(alphabet):
    cache_file = path.join(xpn_cache, '%s.csv' % letter)
    df = pd.read_csv(cache_file)
    playlist = playlist.append(df, ignore_index=True)
    print "adding %d songs for running total of %d" % (len(df), len(playlist))
print "%d songs total" % len(playlist)
originals_cache = path.join(xpn_cache, 'originals.csv')
playlist.to_csv(originals_cache, index=False)
