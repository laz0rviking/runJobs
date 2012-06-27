#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=4:
  print 'Usage: batchOXFORD.py [letter, e.g "x"] [description, e.g "bias00"] [phase, e.g "1500"]'
  sys.exit(0)

## Gather variables
path_letter = sys.argv[1]
path_desc = sys.argv[2]
path_phase = sys.argv[3]

## Choose your run!
#path_letter = "x"
#path_desc = "bias00"
#path_phase = "1500"

#user_name = "paul"
#server_name = "arrakis.engin.umich.edu"
#path_name = "/home/paul/Dropbox/Paulz\ Box/research/mpic/work/from-nyx/test-cell"
#file_name = "plasmaout"

## Initialize arrays/paths
toppath = os.getcwd()

ii = 0
run_first = 1
run_last = 12
run_skip = 1
array_runs = range(run_first,\
                   run_last+1,\
                   run_skip)

############################
## Main Loop
############################
for path_run in array_runs:
  run_num = "R" + str(path_run).zfill(2)
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           path_phase + "-" + \
           run_num
           
  print "------------------------------"
  print "Running OXFORD on \"" + mypath + "\"!"
  os.chdir(mypath)
  subprocess.call("tar -cvf plasmaout-"+run_num+".tar plasmaout*", shell=True)
  os.chdir(toppath)

#  print "Pushing on \"" + mypath + "\"!"
#  if os.path.isdir(mypath):
#    print "Copying " + file_name + ".plt"
#    scp_in = mypath + "/" + file_name + ".plt"
#    scp_out = "\"" + user_name + "@" + server_name + ":" + path_name + "/" + \
#              path_letter + "-00-layfiles/" + file_name + "-" + \
#              mypath + ".plt\""
#    subprocess.call("scp " + scp_in + " " + scp_out, shell=True)
#  else:
#    print "ERROR: Directory \"" + mypath + "\" missing!"
#    quit()

  ii += 1
  print ""


