#! /usr/bin/env python

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
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
    p = OptionParser(usage = "%prog [options] probmap.png groundtruth.png", 
                     epilog =
                     "Example: %s probmap.png groundtruth.png"
                     % os.path.basename(argv[0]))    
 
    p.add_option("-o", dest = "path_out", metavar = "PATH",
                 help = "Output path to save stats to. {DEFAULT = Current "
                        "working directory).")

    (opts, args) = p.parse_args()

    # Set the arguments
    if len(args) != 2:
        usage("Improper number of arguments. See usage below.")
    pm_in = args[0]
    gt_in = args[1]
    
    # Set and check the output directory
    if not opts.path_out:
        opts.path_out = os.getcwd()
    if not os.path.isdir(opts.path_out):
        usage("The output path {0} does not exist".format(opts.path_out))
    path_out = os.path.join(opts.path_out, "segstats")
    if os.path.isdir(path_out):
        usage("There is already a folder with the name segstats in the "
              "output path {0}".format(opts.path_out))
    os.makedirs(path_out)

    # Check if input arguments are directories or single image files
    if os.path.isdir(pm_in):
        pm_files = sorted(glob.glob("{0}/*".format(pm_in)))
    else:
        pm_files = pm_in

    if os.path.isdir(gt_in):
        gt_files = sorted(glob.glob("{0}/*".format(gt_in)))
    else:
        gt_files = gt_in
    if len(pm_files) != len(gt_files):
        usage("The number of probability map images does not equal the "
              "number of ground truth images.")

    # Loop
    for i in range(0, len(pm_files)):
        pmi = misc.imread(pm_files[0])
        gti = misc.imread(gt_files[0])
        if (pmi.shape[0] != gti.shape[0]) or (pmi.shape[1] != gti.shape[1]):
            usage("The images {0} and {1} do not have the same "
                  "dimensions".format(pm_files[i], gt_files[i]))
        for j in range(0, 256):
            threshi = np.where(pmi > j, 1, 0)
            FP = np.float(np.sum((threshi == 1) & (gti == 0)))
            FN = np.float(np.sum((threshi == 0) & (gti == 1)))
            TP = np.float(np.sum((threshi == 1) & (gti == 1)))
            TN = np.float(np.sum((threshi == 0) & (gti == 0)))
            
            FPR = FP/(FP+TN)
            FNR = FN/(FN+TP)
            TPR = TP/(TP+FN)
            TNR = TN/(FP+TN)
 
            print "{0} {1} {2}".format(j, FPR, TPR)








    

