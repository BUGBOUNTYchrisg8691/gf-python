#!/bin/bash/env python3

# Grep-For-Python - A grep wrapper based on Tom Hudson's (https://github.com/tomnomnom) "gf"

import argparse
from bisect import bisect_left
import json
import os
import sys
import subprocess

def getPatternDir():
	"""Returns path to flag/pattern json files."""
	userHome = os.getenv( 'HOME' )
	baseDir = 'Documents/scripts-projects/python3/grep_for/examples/' # Change to location of the examples directory
	patternDir = os.path.join( userHome, baseDir )

	return patternDir

def getFlagsPattern( name ):
	"""Returns flags and regex to be passed to grep."""

	patternDir = getPatternDir()
	with open( os.path.join( patternDir, name + '.json' ), 'r' ) as file:
		jsonFile = json.load( file )
	flags = jsonFile['flags']
	try:
		pattern = jsonFile['pattern']
	except KeyError:
		pattern = jsonFile['patterns']

	return flags, pattern

def main():
	"""Formats grep string with proper flags and pattern, passes it to shell,
	and returns result."""

	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mode', nargs=1, dest='mode', required=True,
		help='mode of operation: list, dump, op, add')
	parser.add_argument( '-p', '--pattern', nargs='+', dest='pattern',
		help='pattern/flags to be passed to grep from json config files: ' \
		'aws-keys, base64, cors, debug-pages, firebase, fw, go-functions, ' \
		'http-auth, ip, json-sec, meg-headers, php-curl, php-errors, ' \
		'php-serialized, php-sinks, php-sources, s3-buckets, sec, servers, ' \
		'strings, takeovers, upload-fields, urls' )
	parser.add_argument( '-f', '--file', nargs='+', dest='file',
		help='file to be grep\'d' )
	args = parser.parse_args()
	if args.mode[0] == 'list':
		patternDir = getPatternDir()
		patterns = os.listdir( patternDir )
		for pattern in patterns:
			print( pattern[:-5] )
	if args.mode[0] == 'dump':
		flags, pattern = getFlagsPattern( args.pattern[0] )
		if isinstance( pattern, str ):
			command = f'grep --color {flags} "{pattern}"'
		else:
			if len( pattern ) == 1:
				command = f'grep --color {flags} "{pattern[0]}"'
			else:
				command = f'grep --color {flags} "{"|".join( map( str, pattern ))}"'
		print( command )
	if args.mode[0] == 'op':
		flags, pattern = getFlagsPattern( args.pattern[0] )
		if isinstance( pattern, str ):
			command = f'grep {flags} "{pattern}" {args.file[0]}'
			#command = ['grep --color', flags, f'"{pattern}"', args.file[0]]
		else:
			if len( pattern ) == 1:
				command = f'grep {flags} "{pattern[0]}" {args.file[0]}'
				#command = ['grep --color', flags, f'"{pattern}"', args.file[0]]
			else:
				command = f'grep {flags} "{"|".join( map( str, pattern ))}" {args.file[0]}'
				#command = ['grep --color', flags, f'"{'|'.join( map( str, pattern ))}"', args.file[0]]
		print( command )
		proc = subprocess.run( command, capture_output=True, text=True, shell=True )
		if proc.returncode != 0:
			print( 'There was an error processing your arguments. Errors have been logged.' )
			print( proc )
			print( proc.stderr )
			with open( 'error', 'a' ) as file:
				file.write( proc.stderr )
		else:
			print( proc )
			print( proc.stdout )
			print( 'This has been logged in an output file in your current directory.' )
			with open( 'output', 'a' ) as file:
				file.write( proc.stdout )

		
if __name__ == '__main__':
	main()