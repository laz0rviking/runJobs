#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=3:
  print 'Usage: untarAll.py [letter, e.g "x"] [description, e.g "bias00"]'
  sys.exit(0)

## Gather variables
path_letter = sys.argv[1]
path_desc = sys.argv[2]

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
  main_path = path_letter + "-00-layfiles/"
  folder_path = "plasmaout-" + path_desc + "-" + run_num + "/"
  mypath = main_path + folder_path
           
  print "------------------------------"
  print "Running untarAll.py on \"" + mypath + "\"!"
  os.chdir(mypath)
  subprocess.call("tar -xvf plasmaout-tar5-"+run_num+".tar", shell=True)
  subprocess.call("tar -xvf plasmaout-tar6-"+run_num+".tar", shell=True)
  subprocess.call("mv plasmaout-tar* ~/Desktop/000-TRASH/", shell=True)
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


