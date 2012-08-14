#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=6:
  print 'Usage: pullData.py [server, e.g. "garnet", "nyx"] [data_set, "DSB/DSC/DSD"] [letter, e.g "x"] [description, e.g "b00"] [phase, e.g "1500"]'
  sys.exit(0)

## Gather variables
server = sys.argv[1]
data_set = str(sys.argv[2])
path_letter = str(sys.argv[3])
path_desc = sys.argv[4]
path_phase = str(sys.argv[5])

if "garnet" in server:
  command_name = "/usr/local/ossh/bin/scp"
  user_name = "pgiulian"
  server_name = "garnet01.erdc.hpc.mil"
  #path_name = "~/mpic-project/work/"
  path_name = "~/work/mpic-work/"
elif "jade" in server:
  command_name = "/usr/local/ossh/bin/scp"
  user_name = "pgiulian"
  server_name = "jade01.erdc.hpc.mil"
  #path_name = "~/mpic-project/work/"
  path_name = "~/work/mpic-work/"
elif "nyx" in server:
  command_name = "scp"
  user_name = "pgiulian"
  server_name = "nyx-login.engin.umich.edu"
  path_name = "~/work/mpic-work/"
  #path_name = "/home/pgiulian/mpic-project/work/wirz-chamber"
else:
  print "ERROR: Can't find that server!"
  quit()

## Initialize arrays/paths
toppath = os.getcwd()

## Make sure enough runs/skips occur
ii = 0

#run_first = 11
run_first = 1

if data_set == "DSD":
  run_last = 34 # brought down from 36
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

#array_runs = [1, 4, 8]
#array_runs = [2, 3, 5, 6, 7, 9, 10, 11, 12]

collect_folder = path_letter + "-transfer/"
if not os.path.isdir(collect_folder):
  subprocess.call("mkdir " + collect_folder, shell=True)
#else:
#  print "ERROR: Directory \"" + collect_folder + "\" already exists!"
#  quit()

## First, call batchOXFORD.py
subprocess.call("batchOXFORD.py "+data_set+" "+path_letter+" "+path_desc+" "+path_phase, shell=True)
           
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
  print "Collecting \"" + mypath + "\"!"
  
## ORIGINAL
#  folder_name = path_letter+"-00-layfiles/plasmaout-R"+str(path_run).zfill(2)
#  os.makedirs(folder_name)
#  scp_out = folder_name
#  file_name = "plasmaout_5"
#  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+"*\""
#  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)
#  file_name = "plasmaout_6"
#  scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+"*\""
#  subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)

## NEW TEMP
#  folder_name = path_letter+"-00-layfiles/plasmaout-"+run_num
#  os.makedirs(folder_name)
#  nodes = range(0,16)
#  for ii in nodes:
#    scp_out = folder_name
#    file_name = "plasmaout-tar-"+str(ii)+"_5-"+run_num
#    scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".tar\""
#    subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)
#    file_name = "plasmaout-tar-"+str(ii)+"_6-"+run_num
#    scp_in = "\""+user_name+"@"+server_name+":"+path_name+"/"+mypath+"/"+file_name+".tar\""
#    subprocess.call(command_name+" "+scp_in+" "+scp_out, shell=True)
  
  file_name = "field"
  copy_in = mypath+"/"+file_name+".plt"
  copy_out = collect_folder+file_name+"-"+mypath+".plt"
  subprocess.call("cp "+copy_in+" "+copy_out, shell=True)

  file_name = "wall"
  copy_in = mypath+"/"+file_name+".plt"
  copy_out = collect_folder+file_name+"-"+mypath+".plt"
  subprocess.call("cp "+copy_in+" "+copy_out, shell=True)

  file_name = "countNumDiag"
  copy_in = mypath+"/"+file_name+".dat"
  copy_out = collect_folder+file_name+"-"+mypath+".dat"
  subprocess.call("cp "+copy_in+" "+copy_out, shell=True)

  file_name = "countMultiColl"
  copy_in = mypath+"/"+file_name+".dat"
  copy_out = collect_folder+file_name+"-"+mypath+".dat"
  subprocess.call("cp "+copy_in+" "+copy_out, shell=True)

  file_name = "IEDF"
  subfolder_name = collect_folder+file_name"-"+run_num+"/"
  os.makedirs(folder_name)
  copy_in = mypath+"/"+file_name+"*"
  copy_out = collect_folder+sub_folder_name
  subprocess.call("cp "+copy_in+" "+copy_out, shell=True)

  ii += 1
  print ""

subprocess.call("tar -cvf "+path_letter+"-transfer.tar "+collect_folder, shell=True)

