#! /usr/bin/env python

#
# [1] Fawcett, T. (2006). An introduction to ROC analysis. Pattern recognition
#     letters, 27(8), 861-874.
# [2] Celebi, M. E., Schaefer, G., Iyatomi, H., Stoecker, W. V., Malters,
#     J. M., & Grichnik, J. M. (2009). An improved objective evaluation
#     measure for border detection in dermoscopy images. Skin Research and
#     Technology, 15(4), 444-450.
# [3] Powers, D. M. (2011). Evaluation: from precision, recall and F-measure to
#     ROC, informedness, markedness & correlation. Journal of Machine Learning
#     Technologies, 2(1), 37-63.
# [4] Seyedhosseini, M., Sajjadi, M., & Tasdizen, T. (2013). Image Segmentation
#     with Cascaded Hierarchical Models and Logistic Disjunctive Normal 
#     Networks. Computer Vision.
#

import os
import glob
import math
import shutil
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
    plt.legend(fontsize = 10, loc = 4)
    plt.tight_layout()
    plt.savefig(fnameout)
    plt.close()

def writePRplot(precision, recall, fnamein, fnameout, opts):
    plt.plot(precision, recall, linewidth = 2, label = "Precision")
    plt.xlabel("Precision", fontsize = 14)
    plt.ylabel("Recall", fontsize = 14)
    plt.title("Precision-Recall Curve - {0}".format(fnamein, fontsize = 14))
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.tight_layout()
    plt.savefig(fnameout)
    plt.close()

def computeMetrics(img, gt):
    # Compute the confusion matrix
    FP = np.float(np.sum((img == 1) & (gt == 0)))
    FN = np.float(np.sum((img == 0) & (gt == 1)))
    TP = np.float(np.sum((img == 1) & (gt == 1)))
    TN = np.float(np.sum((img == 0) & (gt == 0)))
    N = FP + FN + TP + TN

    # Compute evaluation metrics 
    with np.errstate(invalid = "ignore"):
        FPR = np.divide(FP, FP+TN) # Ref [1]
        TPR = np.divide(TP, TP+FN) # Ref [1]
        FNR = np.divide(FN, FN+TP) # Ref [1]
        TNR = np.divide(TN, FP+TN) # Ref [1]
        precision = np.divide(TP, TP+FP) # Ref [1]
        recall = TPR # Ref [1]
        accuracy = (TP+TN)/N # Ref [1]
        errorprob = (FP+FN)/N # Ref [2]
        fvalue = np.divide(2*TP, 2*TP+FP+FN) # Ref [1]
        jaccard = np.divide(TP, FP+TP+FN) # Ref [3]
        gmean = math.sqrt(recall*TNR) # Ref [4]
        ppv = precision # Ref [1]
        npv = np.divide(TN, TN+FN) # Ref [1]
        fdr = np.divide(FP, FP+TP) # Ref [1]
        sensitivity = TPR # Ref [1]
        specificity = TNR # Ref [1]
        informedness = sensitivity + specificity - 1 # Ref [1]
        markedness = precision + npv - 1 # Ref [1]
        MCC = np.divide(TP*TN-FP*FN,
                        math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
    # Create data string
    csvdata = "%d,%d,%d,%d,%d,%0.5f,%0.5f,%0.5f,%0.5f,%0.5f,%0.5f," \
              "%0.5f,%0.5f,%0.5f,%0.5f,%0.5f,%0.5f,%0.5f,%0.5f," \
              "%0.5f,%0.5f,%0.5f,%0.5f,%0.5f" % (j, FP, FN, TP, TN,
              FPR, TPR, FNR, TNR, precision, recall, accuracy,
              errorprob, fvalue, jaccard, gmean, ppv, npv, fdr,
              sensitivity, specificity, informedness, markedness, MCC)
    return FP, FN, TP, TN, TPR, FPR, precision, recall, csvdata


if __name__ == "__main__":
    p = OptionParser(usage = "%prog [options] probmap.png groundtruth.png", 
                     epilog =
                     "Example: %s probmap.png groundtruth.png"
                     % os.path.basename(argv[0]))    
 
    p.add_option("--output", dest = "path_out", metavar = "PATH",
                 help = "Output path to save stats to. (DEFAULT = Current "
                        "working directory).")

    p.add_option("--noroc", action = "store_true", dest = "noroc",
                 help = "Turns off the writing of ROC curves.")

    p.add_option("--nopr", action = "store_true", dest = "nopr",
                 help = "Turns off the writing of precision-recall curves.")

    p.add_option("--noint", action = "store_true", dest = "noint",
                 help = "Turns off writing of intermediate curves for all "
                        "images. Will only plot and save the summed curves.")

    p.add_option("--noimg", action = "store_true", dest = "noimg",
                 help = "Turns off writing of all plots and images.")

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

    path_csv = os.path.join(path_out, "csv")
    os.makedirs(path_csv)
    if not opts.noroc:
        path_roc = os.path.join(path_out, "roc")
        os.makedirs(path_roc)
    if not opts.nopr:
        path_pr = os.path.join(path_out, "prec_recall")
        os.makedirs(path_pr)

    # Check if input arguments are directories or single image files
    if os.path.isdir(pm_in):
        pm_files = sorted(glob.glob("{0}/*".format(pm_in)))
    else:
        pm_files = [pm_in]

    if os.path.isdir(gt_in):
        gt_files = sorted(glob.glob("{0}/*".format(gt_in)))
    else:
        gt_files = [gt_in]

    if len(pm_files) != len(gt_files):
        usage("The number of probability map images does not equal the "
              "number of ground truth images.")
    nfiles = len(pm_files)

    csvheader = "\"Threshold\"," \
                "\"TP\"," \
                "\"FP\"," \
                "\"FN\"," \
                "\"TN\"," \
                "\"TPR\"," \
                "\"FPR\"," \
                "\"TNR\"," \
                "\"FNR\"," \
                "\"Precision\"," \
                "\"Recall\"," \
                "\"Accuracy\"," \
                "\"Error Probability\"," \
                "\"F-value\"," \
                "\"Jaccard Similarity\"," \
                "\"G-Mean\"," \
                "\"Positive Predictive Value\"," \
                "\"Negative Predictive Value\"," \
                "\"False Discovery Rate\"," \
                "\"Sensitivity\"," \
                "\"Specificity\"," \
                "\"Informedness\"," \
                "\"Markedness\"," \
                "\"Matthews Correlation Coefficient\""

    # Loop 
    FParray = np.zeros([nfiles, 256], dtype = "f")
    FNarray = np.zeros([nfiles, 256], dtype = "f")
    TParray = np.zeros([nfiles, 256], dtype = "f")
    TNarray = np.zeros([nfiles, 256], dtype = "f")
    imgtype = []

    for i in range(0, nfiles):
        TPRlist = []
        FPRlist = []
        preclist = []
        reclist = []
        print "Analyzing file {0}...".format(pm_files[i])
        bname = os.path.basename(pm_files[i])
        pmi = misc.imread(pm_files[i])
        gti = misc.imread(gt_files[i])
        if (pmi.shape[0] != gti.shape[0]) or (pmi.shape[1] != gti.shape[1]):
            usage("The images {0} and {1} do not have the same "
                  "dimensions".format(pm_files[i], gt_files[i]))

        # Check if the input image is binary or not. If it is binary, compute
        # metrics at only one threshold (pix values > 0). If it is not binary
        # (i.e. it is a probability map), then threshold at all intensity
        # values and compute metrics.
        if len(np.unique(pmi)) == 2:
            intensities = [0]
            imgtype.append(0)
            fname = os.path.join(path_csv, "stats.csv")
        else:
            intensities = range(0, 256)
            imgtype.append(1)
            fname = os.path.join(path_csv, bname.split(".")[0] + ".csv")
        h = open(fname, "a+")

        if i != 0 and imgtype[i] != imgtype[i-1]:
            shutil.rmtree(path_out)
            usage("Images must be either all binary or all grayscale.")

        for j in range(0, len(intensities)):
            # Threshold the image at the given intensity level
            threshi = np.where(pmi > intensities[j], 1, 0)

            # Get metrics
            FP, FN, TP, TN, TPR, FPR, precision, recall, data = computeMetrics(
                threshi, gti)

            if imgtype[i] == 1: 

                # If it is the beginning of the loop, write the csv header
                if j == 0:
                    h.write(csvheader + "\n")
                h.write(data + "\n")

                FParray[i, j] = FP
                FNarray[i, j] = FN
                TParray[i, j] = TP
                TNarray[i, j] = TN
            
                TPRlist.append(TPR)
                FPRlist.append(FPR)
                preclist.append(precision)
                reclist.append(recall)

                if j == len(intensities)-1:
                    h.close()

            else:
                if i == 0:
                    h.write(csvheader + "\n")
                h.write(data + "\n")
        if (imgtype[i] == 1 and not opts.noimg and not opts.noint and not 
           opts.noroc):
            fnameout = os.path.join(path_roc, "{0}.png".format(
                                    bname.split(".")[0]))
            writeROCplot(FPRlist, TPRlist, bname, fnameout, opts)

        if (imgtype[i] == 1 and not opts.noimg and not opts.noint and not 
           opts.nopr):
            fnameout = os.path.join(path_pr, "{0}.png".format(
                                    bname.split(".")[0]))
            writePRplot(preclist, reclist, bname, fnameout, opts)

    if imgtype[0] == 1:
        FPsum = np.sum(FParray, 0)
        FNsum = np.sum(FNarray, 0)
        TPsum = np.sum(TParray, 0)
        TNsum = np.sum(TNarray, 0)

        if not opts.noimg and not opts.noroc:
            with np.errstate(invalid = "ignore"):
                FPRsum = FPsum/(FPsum+TNsum)
                TPRsum = TPsum/(TPsum+FNsum)
            fnameout = os.path.join(path_roc, "sum.png")
            writeROCplot(FPRsum, TPRsum, "sum", fnameout, opts)
 
        if not opts.noimg and not opts.nopr:
            with np.errstate(invalid = "ignore"):
                precsum = TPsum/(TPsum+FPsum)
                recsum = TPsum/(TPsum+FNsum)
            fnameout = os.path.join(path_pr, "sum.png") 
            writePRplot(precsum, recsum, "sum", fnameout, opts)
    else:
        os.rmdir(path_roc)
        os.rmdir(path_pr)

