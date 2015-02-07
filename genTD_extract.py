#! /usr/bin/env python

# genTD_extract.py
#
# Extracts a set of training images and labels from a given MRC image stack
# with seeds and contours given by the provided IMOD model file. Seeds must
# be provided in Object 1 of the IMOD model file and contours must be provided
# in Object 2 of the IMOD model file.
#
# If no output path is given, the extracted images and labels will be output
# to the current working directory. A new directory named ./training_data will
# be made, and the images and labels will be saved to its sub-directories,
# ./training_data/images and ./training_data/labels. Training images and 
# labels are given the same names so that they will be compatible with the 
# SLASH portal. If an output path is optionally specified, the training_data
# directory and all output will be written there instead of in the current
# working directory.

import os
import textwrap
import getopt
import re
import numpy
import Image
import subprocess
from sys import stderr, argv

def usage(err = 0, msg = None):
    tw = textwrap.TextWrapper(width = 70, initial_indent = ' '*4, 
                              subsequent_indent = ' '*8);
    if msg != None:
        print >> stderr, tw.fill(msg)
    print ""
    print "Usage:"
    print(tw.fill("%s -i file.mrc -o file.mod -d 500,500" % argv[0]))
    print ""
    print("Required Arguments:")
    print(tw.fill("-i  Input MRC file to extract training images from."))
    print(tw.fill("-m  Input IMOD model file to generate training labels "
                  "from. The model file must contain two object: (1) A "
		  "scattered object consisting of seed points, and (2) a "
		  "closed contour object containing the segmentations to "
		  "generate training labels from."))
    print(tw.fill(
        "-d  Dimensions of the training data in X,Y (i.e. 500,500)."))
    print ""
    print "Optional Arguments:"
    print(tw.fill(
        "-o  Output path to store training images and labels to. The "
        "default path is the current directory."))
    print(tw.fill("-h  Display this help information."))
    print ""
    exit(err)

if __name__ == "__main__":
    path_out = os.getcwd()
    try:
        opts, args = getopt.getopt(argv[1:], "ho:i:m:d:")
    except getopt.GetoptError as err: 
	usage(2, str(err))
    for opt, arg in opts:
        if opt == '-h': 
	    usage()
	elif opt in ("-o"): 
	    path_out = arg
	elif opt in ("-i"):
	    file_mrc = arg
	elif opt in ("-m"):
	    file_mod = arg
	elif opt in ("-d"):
	    dims = arg
    
    # Check the validity of the input arguments
    if len(opts) < 3:
        usage(2, "Arguments -i, -m, and -d are required.")
    if not os.path.isfile(file_mrc):
        usage(2, "The MRC file specified by -i does not exist.")
    if not os.path.isfile(file_mod):
        usage(2, "The model file specified by -m does not exist.")
    if not os.path.isdir(path_out):
        usage(2, "The output path specified by -o does not exist.")
    if not "," in dims:
        usage(2, 
	      "The dimensions specified by -d must be separated by a comma.")
    
    # Check that the input mrc file is 8-bit. Return error and quit if not
    cmd = "header -mode %s" % file_mrc    
    mode = int(subprocess.Popen(cmd.split(), stdout = 
               subprocess.PIPE).communicate()[0])
    if mode != 0:
        usage(2, "The input MRC file must be 8-bit to continue.")

    # Make output directories if necessary
    if not os.path.isdir(os.path.join(path_out,"training_data","images")):
        os.makedirs(os.path.join(path_out,"training_data","images"))
    if not os.path.isdir(os.path.join(path_out,"training_data","labels")):
        os.makedirs(os.path.join(path_out,"training_data","labels"))

    # Parse training dimensions
    dims_split = dims.split(",",1)
    dimx = int(dims_split[0])
    dimy = int(dims_split[1])
    radx = int(dimx / 2)
    rady = int(dimy / 2)

    # Extract seeds and contours from the input model file 
    mod_base = os.path.splitext(os.path.basename(file_mod))[0]
    file_extract = os.path.join(path_out,mod_base)
    os.system("imodextract 1 %s %s" %(file_mod, file_extract + "_seed.mod"))
    os.system("imodextract 2 %s %s" %(file_mod, file_extract + "_cont.mod"))

    # Extract point listings from the seed model file
    os.system("model2point %s %s" %(file_extract + "_seed.mod", 
              file_extract + "_seed.txt"))
   
    # Loop over each seed point
    coords = numpy.loadtxt(file_extract + "_seed.txt", dtype="int")
    for i in range(0,coords.shape[0]):
        td_i = os.path.join(path_out,"training_data","images",
	                    str(i + 1).zfill(3))     
        tl_i = os.path.join(path_out,"training_data","labels",
	                    str(i + 1).zfill(3))
	xi = coords[i,0]
	yi = coords[i,1]
	zi = coords[i,2]
	xmin = xi - radx
	xmax = xi + radx - 1
	ymin = yi - rady
	ymax = yi + rady - 1

	# Extract tiles from MRC stack
        os.system("trimvol -x %d,%d -y %d,%d -z %d,%d %s %s" %(xmin,xmax,ymin,
	          ymax,zi+1,zi+1,file_mrc,td_i+".mrc"))

        # Create binary labels from tiles and segmentation
        os.system("imodmop -mode 0 -mask 1 %s %s %s" %(file_extract+"_cont.mod",
	          td_i+".mrc",tl_i+".mrc"))

        # Convert files to PNG
        os.system("mrc2tif -p %s %s" %(td_i+".mrc",td_i+".png"))
	os.system("mrc2tif -p %s %s" %(tl_i+".mrc",tl_i+".png"))
        os.remove(td_i + ".mrc")
        os.remove(tl_i + ".mrc")

    # Cleanup
    os.remove(file_extract + "_cont.mod")
    os.remove(file_extract + "_seed.mod")
    os.remove(file_extract + "_seed.txt")
        
