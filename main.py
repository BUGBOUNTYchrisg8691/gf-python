#!/usr/bin/python3

# gf, in python 3

# Grep wrapper based on "gf" by Tom Hudson (https://github.com/tomnomnom)
# Basically a Python 3 port of his Go program because I could not get it working

import argparse
import json
import os
import subprocess

def get_pattern_dir():
    """ Returns location of flag/pattern json files.
    """

    user_home = os.getenv( 'HOME' )
    base_dir = '.gf/examples' # Change me to location of the examples directory
    pattern_dir = os.path.join( user_home, base_dir )

    return pattern_dir

def get_flags_pattern( name ):
    """ Returns flags and regex string to be passed to grep.
    """

    pattern_dir = get_pattern_dir()
    with open( os.path.join( pattern_dir, name + '.json' ), 'r' ) as file:
        json_file = json.load( file )
    flags = json_file[ 'flags' ]
    try:
        pattern = json_file[ 'pattern' ]
    except KeyError:
        pattern = json_file[ 'patterns' ]

    return flags, pattern


def get_all_patterns():
    """ Returns all patterns in list of json dicts.
    """

    pattern_dir = get_pattern_dir()
    patterns_list = []
    for filename in os.listdir( pattern_dir ):
        with open( os.path.join( pattern_dir, filename ), 'rb' ) as file:
            json_file = json.load( file )
            try:
                patterns_list.append( json_file[ 'pattern' ])
            except KeyError:
                patterns_list.append( json_file[ 'patterns' ])

    return patterns_list

def main():
    """ Formats grep string to be passed to shell and passes it.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', '--mode', help='mode of operation: list, dump, op',
                         nargs=1, dest='mode', required=True )
    parser.add_argument( '-p', '--pattern', help='pattern/flags to be passed to grep ' \
                                                 'from json config files: aws-keys, '\
                                                 'base64, cors, debug-pages, firebase, ' \
                                                 'fw, go-functions, http-auth, ip, ' \
                                                 'json-sec, meg-headers, php-curl, ' \
                                                 'php-errors, php-serialized, php-sinks, ' \
                                                 'php-sources, s3-buckets, sec, servers, ' \
                                                 'strings, takeovers, upload-fields, urls',
                         nargs='+' , dest='pattern' )
    parser.add_argument( '-f', '--files', help='grep in this folder', nargs='+',
                         dest='files' )
    args = parser.parse_args()
    if args.mode[ 0 ] == 'list':
        patterns_list = get_all_patterns()
        for patterns in patterns_list:
            if isinstance( patterns, list ):
                for pattern in patterns:
                    print( pattern )
            else:
                print( patterns )
    if args.mode[ 0 ] == 'dump':
        flags, pattern = get_flags_pattern( args.pattern[ 0 ])
        print( 'grep ' + flags + ' "' + '|'.join( map( str, pattern )) + '" ' + ' '.join( map( str, args.files )))
    if args.mode[ 0 ] == 'op':
        flags, pattern = get_flags_pattern( args.pattern[ 0 ])
        process = subprocess.run([ 'grep', flags, '|'.join( map( str, pattern )),
                                 ' '.join( map( str, args.files ))],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        output = process.stdout.splitlines()
        for line in output:
            print( line.decode())

if __name__ == '__main__':

    main()