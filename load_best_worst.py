#! /usr/bin/env python

from lxml import html
import requests
import os.path as path
import pandas as pd


def load_playlist(playlist_url, pagecount, file_name):
    rows = []
    cache_dir = './cache'
    xpn_cache = path.join(cache_dir, 'xpn')
    cache_file = path.join(xpn_cache, file_name)
    
    for page_no in range(1, pagecount + 1):
        args = {'page': page_no}
        page = requests.get(playlist_url, params = args)
        tree = html.fromstring(page.content)
        tracks = tree.xpath("//*/tr[@class='countdown']")
        for track in tracks:
            artist = track.xpath('./td[2]/text()')[0]
            title = track.xpath('./td[@class="song"]/text()')[0]
            rows.append([title, artist])
        df = pd.DataFrame(rows, columns = ['Title', 'Artist'])
        df.to_csv(cache_file, index=False)




load_playlist('http://www.xpn.org/music-artist/885-countdown/2014/885-countdown-2014',
              18, '885best.csv')
load_playlist('http://www.xpn.org/music-artist/885-countdown/2014/885-countdown-2014-88-worst',
              2, '88worst.csv')


