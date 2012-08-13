#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=5:
  print 'Usage: pullData.py [server, e.g. "garnet", "nyx"] [data-set, e.g. "DSB", "DSD"] [letter, e.g "x"] [description, e.g "bias00"]'
  sys.exit(0)

## Gather variables
server = sys.argv[1]
data_set = sys.argv[2]
path_letter = sys.argv[3]
path_desc = sys.argv[4]

if server == "garnet":
  command_name = "/usr/local/ossh/bin/scp"
  user_name = "pgiulian"
  server_name = "garnet01.erdc.hpc.mil"
  #path_name = "~/icepic-project/work/"
  path_name = "~/work/icepic-work/"
elif server == "nyx":
  command_name = "scp"
  user_name = "pgiulian"
  server_name = "nyx-login.engin.umich.edu"
  path_name = "~/work/icepic-work/"
  #path_name = "/home/pgiulian/mpic-project/work/wirz-chamber"
else:
  print "ERROR: Can't find that server!"
  quit()

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
elif data_set == "TEST":
  run_last = 11
  run_skip = 2
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
  run_num = "R" + str(path_run).zfill(2)
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           run_num
           
  print "------------------------------"
  print "Pulling on \"" + mypath + "\"!"
  
#  file_name = "field"
#  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".*\""
#  new_dir = path_letter+"-00-layfiles/"+file_name+"-"+run_num
#  subprocess.call("mkdir " + new_dir, shell=True)
#  scp_out = new_dir+"/"
#  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

#  file_name = "part_ion_wall"
#  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".*\""
#  new_dir = path_letter+"-00-layfiles/"+file_name+"-"+run_num
#  subprocess.call("mkdir " + new_dir, shell=True)
#  scp_out = new_dir+"/"
#  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "ice.stat"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+"\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "mcc_stats"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+"\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "curJ_IC"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".dat\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "curJ_EP_EO"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".dat\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  file_name = "curJ_EO"
  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".dat\""
  scp_out = path_letter+"-00-layfiles/"+file_name+"-"+mypath+".dat"
  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

  ii += 1
  print ""


