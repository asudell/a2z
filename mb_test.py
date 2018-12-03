#! /usr/bin/env python

import sys
import csv
import musicbrainzngs as mb

def lookup_tracks(input, output=None, verbose=False):

    mb.set_useragent('xpn-a2z', '0.1', 'https://github.com/asudell/a2z')
    
    with open(input) as songs:
        reader = csv.DictReader(songs)
        for row in reader:
            if verbose:
                print "looking up %s by %s" % (row['Title'], row['Artist'])
            result = mb.search_recordings(row['Title'],
                                          artist = row['Artist'],
                                          status = 'official',
                                          strict = True,
                                          limit = 25)

            rel_date = None
            if verbose:
                if 'recording-list' in result:
                    print "found %d recordings" % len(result['recording-list'])
                else:
                    print "no recording-list found"

            for recording in result['recording-list']:

                if verbose:
                    print 'id: %s artist %s' % \
                        (recording['id'],
                         recording['artist-credit'][0]['artist']['sort-name'].encode('utf-8'))
                    if recording['release-list']:
                        print "part of %d releases" % len(recording['release-list'])
                    else:
                        print "no releases"

                if recording['release-list']:
                    for release in recording['release-list']:
                        if verbose:
                            if 'date' in release and len(release['date']) > 0:
                                d = release['date']
                                y = int(release['date'].split('-')[0])
                                if y > 1979 and (rel_date is None or rel_date > y):
                                    rel_date = y
                            else:
                                d = "N/A"
                            if verbose:
                                print 'release id: %s date %s title %s' % \
                                    (release['id'], d, release['title'].encode('utf-8'))

            if verbose:
                if rel_date is not None:
                    print "computed release year of %d" % rel_date
                else:
                    print 'no release date found'

                



        

if __name__ == "__main__":
    lookup_tracks(sys.argv[1], verbose=True)
    
    
