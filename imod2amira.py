#! /usr/bin/env python

import os
import sys
import re
import fileinput
import shutil
from optparse import OptionParser
from subprocess import Popen, call, PIPE
from sys import stderr, exit, argv

# Print erorr messages and exit
def usage(errstr):
    print ""
    print "ERROR: %s" % errstr
    print ""
    p.print_help()
    print ""
    exit(1)

# Parse through a text file until the regexp is matched. Once a match occurs,
# return the entire line and break the loop.
def matchLine(regexp, handle):
    for line in handle:
        if re.match(regexp, line.lstrip()):
            return line
            break
        else:
            continue
        break

# Convert IMOD model file to ASCII using imodinfo
def mod2ascii(mod_in, ascii_out):
    handle = open(ascii_out, "w+")
    cmd = "imodinfo -a {0}".format(mod_in)
    call(cmd.split(), stdout = handle)
    return handle

if __name__ == "__main__":
    p = OptionParser(usage = "%prog [options] file_in.mod file_out.wml")

    p.add_option("--scale", dest = "scale", metavar = "X,Y,Z",
                 help = "Pixel scales in X,Y,Z.")

    (opts, args) = p.parse_args()

    # Parse the positional arguments
    if len(args) is not 2:
        usage("Improper number of arguments. See the usage below.")
    file_in = args[0]
    file_out = args[1]
    path_out = os.path.dirname(file_out)
    if not path_out:
        path_out = os.getcwd()
    path_tmp = os.path.join(path_out, "tmp")
    base_out = os.path.basename(file_out)

    # Check validity of positional arguments
    if not os.path.isfile(file_in):
        usage("The input file {0} does not exist".format(file_in))

    if not os.path.isdir(path_out):
        usage("The output path {0} does not exist.".format(path_out))

    # Create temporary directory in the output path
    if os.path.isdir(path_tmp):
        usage("There is already a folder with the name tmp in the output "
              "path {0}".format(path_out))
    os.makedirs(path_tmp)

    # Parse the scale option if provided. If not provided, extract scale info
    # from the model header
    if opts.scale:
        scalex = opts.scale.split(",")[0]
        scaley = opts.scale.split(",")[1]
        scalez = opts.scale.split(",")[2]
    else:
        # Convert entire model to ASCII format 
        asciifile = os.path.join(path_tmp, file_in.split('.')[0] + ".txt")
        handle = mod2ascii(file_in, asciifile)

        # Parse the ASCII file to get the unit scales
        handle.seek(0)
        line = matchLine("^refcurscale", handle)
        scalex = float(line.split()[1])
        scaley = float(line.split()[2])
        scalez = float(line.split()[3])
        handle.close()

    ##########
    ## MAIN LOOP 
    ##########
    cmd = "imod2vrml2 {0} {1}".format(file_in, file_out)
    call(cmd.split())
    handle = open(file_out, "r+")

    coordswitch = 0
    for line in fileinput.input(file_out, inplace = True):
        if re.match("^point", line.lstrip()):
            coordswitch = 1
            sys.stdout.write(line)
            continue
        if re.match("\]", line.lstrip()):
            coordswitch = 0
            sys.stdout.write(line)
            continue
        if coordswitch:
            lineafter = line.lstrip()
            lenbefore = len(line)
            lenafter = len(lineafter)
            nspaces = lenbefore - lenafter
            blankspace = " " * nspaces
            coordx = float(lineafter.split()[0]) * scalex
            coordy = float(lineafter.split()[1]) * scaley
            coordz = lineafter.split()[2]
            coordz = float(coordz.split(",")[0]) * scalez
            line = "%s%0.1f %0.1f %0.1f,\n" % (blankspace, coordx, coordy, coordz)
            sys.stdout.write(line)
        else:
            sys.stdout.write(line)
    handle.close()
    shutil.rmtree(path_tmp)

