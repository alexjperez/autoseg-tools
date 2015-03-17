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
import re
import array
from optparse import OptionParser
from subprocess import Popen, call, PIPE
from sys import stderr, exit, argv

def usage(errstr):
    print ""
    print "ERROR: %s" % errstr
    print ""
    p.print_help()
    print ""
    exit(1)

if __name__ == "__main__":
    p = OptionParser(usage = "%prog [options] file.mrc file.mod Xdim Ydim", 
                     description =
                     "Extracts a set of training images and labels from a "
                     "given MRC image stack with seeds and contours provided "
                     "by the IMOD model file. Requires four input arguments: "
                     "1) file.mrc - The name of the input mrc file on which "
                     "segmentations were made; 2) file.mod - The name of the "
                     "IMOD model file that contains seed points and training "
                     "segmentations; 3) Xdim - Horizontal size of the "
                     "training images and labels to be extracted; 4) Ydim - "
                     "Vertical size of the training images and labels to be "
                     "extracted.", 
                     epilog =
                     "Example: %s ZT04_01.mrc ZT04_01_trainMito.mod 500 500"
                     % os.path.basename(argv[0]))    
 
    p.add_option("-o", dest = "path_out", metavar = "PATH",
                 help = "Output path to save training images and labels to "
                        "(DEFAULT = Current directory).")

    p.add_option("-s", dest = "objscat", metavar = "INT",
                 help = "Object number in the IMOD model file that contains "
                        "the scattered seed points (DEFAULT = 1).")

    p.add_option("-c", dest = "objseg", metavar = "INT",
                 help = "Object number in the IMOD model file that contains "
                        "the closed contour segmentations (DEFAULT = 2).")

    (opts, args) = p.parse_args()   

    # Set the arguments
    if len(args) != 4:
        usage("Improper number of arguments. See usage below.")
    file_mrc = args[0]
    file_mod = args[1]
    dimx = int(args[2])
    dimy = int(args[3])

    # Set and check the output directory
    if opts.path_out:
        path_out = opts.path_out
    else:
        path_out = os.getcwd()
    if not os.path.isdir(path_out):
        usage("The output path specified by -o does not exist.")

    # Check the validity of the arguments
    if not os.path.isfile(file_mrc):
        usage("The MRC file {0} does not exist.".format(file_mrc))
    if not os.path.isfile(file_mod):
        usage("The model file {0} does not exist.".format(file_mod))

    # Check the validity of the optional arguments
    if (opts.objscat and not opts.objseg) or (opts.objseg and not opts.objscat):
        usage("If specifying non-default objects, both -s and -c must be used.")

    # Set objects
    if opts.objscat:
        objscat = int(opts.objscat)
    else:
        objscat = 1
    if opts.objseg:
        objseg = int(opts.objseg)
    else:
        objseg = 2

    # Check the version of IMOD
    imoddir = os.getenv('IMOD_DIR')
    if imoddir:
        imodvers_file = open(os.path.join(imoddir, "VERSION"), 'r')
	imodvers = imodvers_file.read()
	if imodvers:
	    imodvers = float(imodvers.split('.')[0]) + 0.1 * float(imodvers.split('.')[1])
	    print "Running IMOD version %0.1f.X" % imodvers
            imodvers_file.close()
	else:
	    usage("Cannot determine the IMOD version. Check $IMOD_DIR/VERSION")
    else:
        usage("IMOD is not installed or sourced properly.")

    # Check that the MRC file is 8-bit
    cmd = "header -mode {0}".format(file_mrc)
    mode = int(Popen(cmd.split(), stdout = PIPE).communicate()[0])
    if mode != 0:
        usage("The input MRC file must be 8-bit to continue. Please run newstack -mode 0.")
 
    # Make output directories if necessary
    if not os.path.isdir(os.path.join(path_out,"training_data","images")):
        os.makedirs(os.path.join(path_out,"training_data","images"))
    if not os.path.isdir(os.path.join(path_out,"training_data","labels")):
        os.makedirs(os.path.join(path_out,"training_data","labels"))

    # Process training dimensions
    radx = int(dimx / 2)
    rady = int(dimy / 2)

    # Extract seeds and contours from the input model file 
    mod_base = os.path.splitext(os.path.basename(file_mod))[0]
    file_extract = os.path.join(path_out,mod_base)
    cmd = "imodextract {0} {1} {2}".format(objscat, file_mod, 
           file_extract + "_seed.mod")
    call(cmd.split())
    cmd = "imodextract {0} {1} {2}".format(objseg, file_mod,
           file_extract + "_cont.mod")
    call(cmd.split())

    # Extract point listings from the seed model file
    cmd = "model2point {0} {1}".format(file_extract + "_seed.mod",
           file_extract + "_seed.txt")
    call(cmd.split())

    # Read seed points into an array
    arrayx = array.array('l');
    arrayy = array.array('l');
    arrayz = array.array('l');
    handle = open(file_extract + "_seed.txt", 'r')
    for line in handle:
        line = line.split()
        arrayx.append(int(line[0]))
        arrayy.append(int(line[1]))
        arrayz.append(int(line[2]))

    # Loop over each point, extract tiles   
    for i in range(0, len(arrayx)):
        td_i = os.path.join(path_out,"training_data","images",
	                    str(i + 1).zfill(3))     
        tl_i = os.path.join(path_out,"training_data","labels",
	                    str(i + 1).zfill(3))
	xi = arrayx[i]
	yi = arrayy[i]
	zi = arrayz[i]
	xmin = xi - radx
	xmax = xi + radx - 1
	ymin = yi - rady
	ymax = yi + rady - 1

	# Extract tiles from MRC stack
        cmd = "trimvol -x {0},{1} -y {2},{3} -z {4},{5} {6} {7}".format(
               xmin, xmax, ymin, ymax, zi+1, zi+1, 
               file_mrc, 
               td_i + ".mrc")
	call(cmd.split())

        # Create binary labels from tiles and segmentation
        cmd = "imodmop -mode 0 -mask 1 {0} {1} {2}".format(
               file_extract + "_cont.mod",
               td_i + ".mrc", 
               tl_i + ".mrc")
        call(cmd.split())

        # Convert files to PNG. If the IMOD version is > 4.7, do this using 
	# mrc2tif with a -p flag. If not, do it in two steps: (1) mrc2tif and
	# (2) ImageMagick convert to go from tif to png. 
        
	if imodvers > 4.7: 
	    cmd = "mrc2tif -p {0} {1}".format(td_i + ".mrc", td_i + ".png")
	    call(cmd.split())
	    cmd = "mrc2tif -p {0} {1}".format(tl_i + ".mrc", tl_i + ".png")
            call(cmd.split())
        else:
	    cmd = "mrc2tif {0} {1}".format(td_i + ".mrc", td_i + ".tif")
            call(cmd.split())
	    cmd = "mrc2tif {0} {1}".format(tl_i + ".mrc", tl_i + ".tif")
	    call(cmd.split())
	    cmd = "convert {0} {1}".format(td_i + ".tif", td_i + ".png")
	    call(cmd.split())
	    cmd = "convert {0} {1}".format(tl_i + ".tif", tl_i + ".png")
	    call(cmd.split())
	    os.remove(td_i + ".tif")
	    os.remove(tl_i + ".tif")
	os.remove(td_i + ".mrc")
        os.remove(tl_i + ".mrc")

    # Cleanup
    os.remove(file_extract + "_cont.mod")
    os.remove(file_extract + "_seed.mod")
    os.remove(file_extract + "_seed.txt")
