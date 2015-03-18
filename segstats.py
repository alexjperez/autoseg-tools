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

def writeROCplot(FPR, TPR, fnamein, fnameout, opts):
    plt.plot(FPR, TPR, linewidth = 2, label = "ROC")
    if opts.randline:
        x = [0.0, 1.0]
        plt.plot(x, x, linestyle = "dashed", color = "red", linewidth = 2,
                 label = "Random")
    plt.xlabel("False Positive Rate", fontsize = 14)
    plt.ylabel("True Positive Rate", fontsize = 14)
    plt.title("ROC Curve - {0}".format(fnamein, fontsize = 14))
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.legend(fontsize = 10, loc = "best")
    plt.tight_layout()
    plt.savefig(fnameout)
    plt.close()

if __name__ == "__main__":
    p = OptionParser(usage = "%prog [options] probmap.png groundtruth.png", 
                     epilog =
                     "Example: %s probmap.png groundtruth.png"
                     % os.path.basename(argv[0]))    
 
    p.add_option("--output", dest = "path_out", metavar = "PATH",
                 help = "Output path to save stats to. (DEFAULT = Current "
                        "working directory).")

    p.add_option("--noroc", action = "store_true", dest = "noroc",
                 help = "Turns off writing of ROC plots.")

    p.add_option("--randomline", action = "store_true", dest = "randline",
                 help = "Adds a line equivalent to making a random choice "
                        "to all ROC plots.")

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

    if not opts.noroc:
        os.makedirs(os.path.join(path_out, "roc"))

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
    nfiles = len(pm_files)

    # Loop 
    FParray = np.zeros([nfiles, 256], dtype = "f")
    FNarray = np.zeros([nfiles, 256], dtype = "f")
    TParray = np.zeros([nfiles, 256], dtype = "f")
    TNarray = np.zeros([nfiles, 256], dtype = "f")
    for i in range(0, nfiles):
        TPRlist = []
        FPRlist = []
        print "Analyzing file {0}...".format(pm_files[i])
        bname = os.path.basename(pm_files[i])
        pmi = misc.imread(pm_files[i])
        gti = misc.imread(gt_files[i])
        if (pmi.shape[0] != gti.shape[0]) or (pmi.shape[1] != gti.shape[1]):
            usage("The images {0} and {1} do not have the same "
                  "dimensions".format(pm_files[i], gt_files[i]))
        for j in range(0, 256):
            # Threshold the image at the given intensity level
            threshi = np.where(pmi > j, 1, 0)
            
            # Compute the confusion matrix
            FP = np.float(np.sum((threshi == 1) & (gti == 0)))
            FN = np.float(np.sum((threshi == 0) & (gti == 1)))
            TP = np.float(np.sum((threshi == 1) & (gti == 1)))
            TN = np.float(np.sum((threshi == 0) & (gti == 0)))
           
            FPR = FP/(FP+TN)
            TPR = TP/(TP+FN)
            FNR = FN/(FN+TP)
            TNR = TN/(FP+TN)

            FParray[i, j] = FP
            FNarray[i, j] = FN
            TParray[i, j] = TP
            TNarray[i, j] = TN
            
            TPRlist.append(TPR)
            FPRlist.append(FPR)

        if not opts.noroc:
            fnameout = os.path.join(path_out, "roc", "{0}.png".format(
                                    bname.split(".")[0]))
            writeROCplot(FPRlist, TPRlist, bname, fnameout, opts)

    FPsum = np.sum(FParray, 0)
    FNsum = np.sum(FNarray, 0)
    TPsum = np.sum(TParray, 0)
    TNsum = np.sum(TNarray, 0)
    if not opts.noroc:
        with np.errstate(invalid = "ignore"):
            FPRsum = FPsum/(FPsum+TNsum)
            TPRsum = TPsum/(TPsum+FNsum)
        fnameout = os.path.join(path_out, "roc", "sum.png")
        writeROCplot(FPRsum, TPRsum, "sum", fnameout, opts)

