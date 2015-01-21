#! /usr/bin/env python

# genTD_list_slices.py
#
# Takes an MRC file (SBEM stack) as input, and automatically determines the 
# slices training data should be generated from to yield an even distribution
# throughout Z. The first few and last few slices are ignored from 
# consideration.

import os
import textwrap
import getopt
import subprocess
from sys import stderr,argv

def usage(err=0, msg=None):
    tw = textwrap.TextWrapper(width=70, initial_indent=' '*4,
                              subsequent_indent=' '*8)
    if msg != None:
        print >> stderr, msg
    print ""
    print "Usage:"
    print(tw.fill("%s -i file.mrc" % argv[0]))
    print ""
    print("Required Arguments:")
    print(tw.fill("-i  Input MRC file to analyze."))
    print ""
    print "Optional Arguments:"
    print(tw.fill("-h  Display this help information."))
    print ""
    exit(err)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(argv[1:], "hi:")
    except getopt.GetoptError as err: 
	usage(2, str(err))
    for opt, arg in opts:
        if opt == '-h': 
	    usage()
	elif opt in ("-i"): 
	    file_mrc = arg
    
    # Check the validity of the input arguments
    if len(opts) < 1:
        usage(2, "The argument -i is required.")
    if not os.path.isfile(file_mrc):
        usage(2, "The MRC file specified by -i does not exist.")

    # Obtain the number of slices in the image stack
    cmd = "header -size %s" % file_mrc
    size = subprocess.Popen(cmd.split(), 
                            stdout=subprocess.PIPE).communicate()[0]
    nslices = int(size.split()[2])
    
    # Scale the number of slices by 0.9 to effectively remove the first and 
    # last few slices from consideration. Divide the scaled, total number of
    # slices by 10 so that placing 5 scattered points on each slice will yield
    # 50 total seed points.
    increment = nslices * 0.9 / 10
    lista = range(1,11)
    listb = [increment] * 10
    out = [a*b for a,b in zip(lista, listb)]
    out = ['%.0f' % x for x in out]
    print ""
    print " ".join([str(x) for x in out])
    print ""
