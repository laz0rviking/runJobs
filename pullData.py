#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=5:
  print 'Usage: pullData.py [server, e.g. "garnet", "nyx"] [letter, e.g "x"] [description, e.g "bias00"] [phase, e.g "1500"]'
  sys.exit(0)

## Gather variables
data_set = "DS5"
server = sys.argv[1]
path_letter = sys.argv[2]
path_desc = sys.argv[3]
path_phase = sys.argv[4]

if server == "garnet":
  command_name = "/usr/local/ossh/bin/scp"
  user_name = "pgiulian"
  server_name = "garnet01.erdc.hpc.mil"
  path_name = "~/mpic-project/work/"
elif server == "nyx":
  command_name = "scp"
  user_name = "pgiulian"
  server_name = "nyx-login.engin.umich.edu"
  path_name = "/home/pgiulian/mpic-project/work/wirz-chamber"
else:
  print "ERROR: Can't find that server!"
  quit()

## Initialize arrays/paths
toppath = os.getcwd()

## Make sure enough runs/skips occur
ii = 0
run_first = 1
if data_set == "DS5":
  run_last = 36
  run_skip = 2
elif data_set == "DS4":
  run_last = 12
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
  print "Pulling on \"" + mypath + "\"!"
  
  file_name = "plasmaout"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".plt\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".plt"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "field"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".plt\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".plt"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "countNumDiag"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".dat\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  ii += 1
  print ""


