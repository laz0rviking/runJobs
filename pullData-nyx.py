#!/usr/bin/env python2

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=4:
  print 'Usage: pullData.py [letter, e.g "x"] [description, e.g "bias00"] [phase, e.g "1500"]'
  sys.exit(0)

## Gather variables
path_letter = sys.argv[1]
path_desc = sys.argv[2]
path_phase = sys.argv[3]

## Choose your run!
#path_letter = "x"
#path_desc = "bias-10"
#path_phase = "1500"

user_name = "pgiulian"
server_name = "nyx-login.engin.umich.edu"
path_name = "/home/pgiulian/mpic-project/work/wirz-chamber"

## Initialize arrays/paths
toppath = os.getcwd()

run_first = 1
run_last = 12
#run_last = 11
ii = 0
array_runs = range(run_first,\
                   run_last+1)

#scp "pgiulian@nyx-login.engin.umich.edu:/home/pgiulian/mpic-project/work/wirz-chamber/s-test-1500-R01/plasmaout.plt" s-00-layfiles/plasmaout-s-test-1500-R01.plt

############################
## Main Loop
############################
for path_run in array_runs:
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           path_phase + "-" + \
           "R" + str(path_run).zfill(2)
  print "------------------------------"
  print "Pulling on \"" + mypath + "\"!"
  
  file_name = "plasmaout"
  scp_in = "\"" + user_name + "@" + server_name + ":" + path_name + "/" + mypath + "/" + file_name + ".plt\""
  scp_out = path_letter + "-00-layfiles/" + file_name + "-" + mypath + ".plt"
  subprocess.call("scp " + scp_in + " " + scp_out, shell=True)

  file_name = "field"
  scp_in = "\"" + user_name + "@" + server_name + ":" + path_name + "/" + mypath + "/" + file_name + ".plt\""
  scp_out = path_letter + "-00-layfiles/" + file_name + "-" + mypath + ".plt"
  subprocess.call("scp " + scp_in + " " + scp_out, shell=True)

  file_name = "countNumDiag"
  scp_in = "\"" + user_name + "@" + server_name + ":" + path_name + "/" + mypath + "/" + file_name + ".dat\""
  scp_out = path_letter + "-00-layfiles/" + file_name + "-" + mypath + ".dat"
  subprocess.call("scp " + scp_in + " " + scp_out, shell=True)

  ii += 1
  print ""


