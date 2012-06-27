#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess,string

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=4:
  print 'Usage: runJobs [data-set, e.g. "DS1", "DS5"] [path-letter, e.g. "aa", "bb"] [IC bias-voltage, e.g. "-10", "00", "20"]'
  sys.exit(0)

## Gather server variable
data_set = str(sys.argv[1])
path_letter = str(sys.argv[2])
voltage = str(sys.argv[3])

## Choose your run!
path_desc = "b"+voltage

## Choose simulation:
queue_time = "4:00:00"

## Server-specific queueing params
## Make sure you use the ENTIRE node!
## For Garnet this is 16 cores/node
queue_cores = "16"
queue_name = "AFPRD24930028"
queue_type = "standard"

## Initialize arrays/paths
toppath = os.getcwd()
oldpath = path_letter + "-00-container"

## Make sure enough runs/skips occur
ii = 0
run_first = 1
if data_set == "DS4":
  run_last = 12
  run_skip = 1
else:
  print "ERROR: Can't find that data set!"
  quit()
array_runs = range(run_first,\
                   run_last+1,\
                   run_skip)

q = 1.602e-19
vi = 46900
ri = 1.27e-3
Ai = numpy.pi*ri*ri
T = 298
k = 1.38e-23

## Data set input parameters
## Make sure to check for specific weighting
## variations (e.g., the y/z variation)
## DS5 (aa,bb
## DS4 (x,y,z)
## DS1 (t-v)
if data_set == "DS4":
  if voltage == "00":
    array_I = numpy.array([6.922,\
                           6.610,\
                           6.302,\
                           5.980,\
                           5.611,\
                           5.087,\
                           4.527,\
                           4.110,\
                           3.744,\
                           3.268,\
                           2.925,\
                           2.443])*1e-9
  else:
    print "ERROR: Can't find input conditions for that voltage!"
    quit()
else:
  print "ERROR: Can't find that Data Set!"
  quit()

if data_set == "DS4":
  array_P = numpy.array([1.40E-02,\
                         2.67E-02,\
                         3.97E-02,\
                         5.41E-02,\
                         7.16E-02,\
                         9.85E-02,\
                         1.31E-01,\
                         1.57E-01,\
                         1.83E-01,\
                         2.20E-01,\
                         2.50E-01,\
                         3.00E-01]) # Pascals
else:
  print "ERROR: Can't find that Data Set!"
  quit()


##########################
## Write pbs.sh
##########################
def write_pbs():
  filename = "pbs.sh"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")

  init_text = ["",\
    "#!/bin/sh\n",\
    "#PBS -S /bin/sh\n",\
    "#PBS -A "+queue_name+"\n",\
    "#PBS -q "+queue_type+"\n",\
    "#PBS -N i"+path_letter+path_desc+"R"+str(path_run).zfill(2)+"\n",\
    "#PBS -l ncpus="+queue_cores+",walltime="+queue_time+"\n",\
    "#PBS -M pgiulian@umich.edu\n",\
    "#PBS -m be\n",\
    "#PBS -V\n",\
    "#PBS -joe\n",\
    "\n",\
    "cd $PBS_O_WORKDIR\n",\
    "aprun -n "+queue_cores+" icepic\n",\
    "\n"]

  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"

  return

##########################
## Write test.in
##########################
def write_test():

  inFileName = oldpath + "/test_DS4.in"
  outFileName = mypath + "/test.in"

  inFile = open(inFileName, 'r')
  inFileStr = inFile.read()
  inFile.close()  

  outputStr = inFileStr
  
  ## Insert Run number
  findStr= "$RUN_NUM"                                  
  replaceStr = run_num
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert current
  findStr= "$CURRENT"                                  
  replaceStr = str(array_I[ii])
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert pressure
  findStr= "$PRESSURE"                                  
  replaceStr = str(array_P[ii])
  outputStr = outputStr.replace(findStr, replaceStr)

  outFile = open(outFileName, 'w')
  outFile.write(outputStr)
  outFile.close()

  return


############################
## Main Loop
############################
for path_run in array_runs:
  run_num = "R" + str(path_run).zfill(2)
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           run_num

  print "------------------------------"
  print "Working on \"" + mypath + "\"!"

  if not os.path.isdir(mypath):
    os.makedirs(mypath)
    print "Folder created!"
  else:
    print "ERROR: Directory \"" + mypath + "\" already exists!"
    quit()

  write_pbs()
  write_test()

  ## Copy gas-model.xml
  if not os.path.isfile(oldpath + "/gas-model.xml"):
    print "ERROR: Where is \"gas-model.xml\"?"
    quit()
  else:
    shutil.copyfile(oldpath + "/gas-model.xml", mypath + "/gas-model.xml")
    print "Copied gas-model.xml!"

  os.chdir(mypath)
  subprocess.call("ipp.py test.in ice.dat", shell=True)
  subprocess.call("qsub pbs.sh", shell=True)
  os.chdir(toppath)

  ii += 1
  print ""


