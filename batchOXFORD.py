#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=5:
  print 'Usage: batchOXFORD.py [data-set, e.g. "DSB", "DSD"] [letter, e.g "x"] [description, e.g "bias00"] [phase, e.g "1500"]'
  sys.exit(0)

## Gather variables
data_set = str(sys.argv[1])
path_letter = sys.argv[2]
path_desc = sys.argv[3]
path_phase = sys.argv[4]

## Initialize arrays/paths
toppath = os.getcwd()

## Make sure enough runs/skips occur
ii = 0
run_first = 1
if data_set == "DSD":
  run_last = 34
  run_skip = 3
elif data_set == "DSC":
  run_last = 12
  run_skip = 1
elif data_set == "DSB":
  run_last = 11
  run_skip = 1
elif data_set == "DSA":
  run_last = 9
  run_skip = 1
else:
  print "ERROR: Can't find that data set!"
  quit()
array_runs = range(run_first,\
                   run_last+1,\
                   run_skip)

############################
## Main Loop
############################
for path_run in array_runs:
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           path_phase + "-" + \
           "R" + str(path_run).zfill(2)
  print "------------------------------"
  print "Running OXFORD on \"" + mypath + "\"!"
  os.chdir(mypath)
  subprocess.call("oxford", shell=True)
  os.chdir(toppath)

  ii += 1
  print ""


