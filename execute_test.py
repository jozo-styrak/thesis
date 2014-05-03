#!/usr/bin/env python
# script for test execution
# args
#   folder from
#   folder to
import glob
import sys
import os


# get folder names
folder_from = sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/'
folder_to = sys.argv[2] if sys.argv[2].endswith('/') else sys.argv[2] + '/'

# get input files
input_filenames = glob.glob(folder_from + '*.txt')

# command
command = '/home/xstyrak/thesis/shell_scripts/analyse_text.sh '

# sequentially proces files
for filepath in input_filenames:
    try:
        filename = filepath[filepath.rfind('/')+1:]
        test_command = command + filepath + ' > ' + folder_to + filename
        os.system(test_command)
    except:
        print 'error processing file ' + filepath