# Chris Probert
# MUS7 Project
#

import sys, os
import numpy as np

def main() :

	if len( sys.argv ) < 2 :
		print "Must provide WIG file as argument"
		sys.exit(1)

	vector = readWIG ( sys.argv[1] )

	print( "file contains %i entries" % len(vector) )

def readWIG( WIGpath ) :

	ResultVector = []

	# expected WIG format: 2L	1	53	-1.14

	with open ( sys.argv[1] ) as WIGfile :
		for line in WIGfile :

			l = line.strip().split('\t')

			if len( l ) != 4 : continue

			startPos = int ( l[1] )
			endPos =  int ( l[2] )
			value = float( l[3] )

			ResultVector += [ value for i in range ( startPos, endPos) ]

	return ResultVector

if __name__ == "__main__" : main()