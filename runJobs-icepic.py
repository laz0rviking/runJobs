#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess,string

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=5:
  print 'Usage: runJobs [server name, e.g. "nyx/jade/garnet/arrakis"] [data-set, e.g. "DSB", "DS5"] [path-letter, e.g. "a-01", "b-01"] [IC bias-voltage, e.g. "-10", "00", "20"]'
  sys.exit(0)

## Gather server variable
server = sys.argv[1]
data_set = str(sys.argv[2])
path_letter = str(sys.argv[3])
voltage = str(sys.argv[4])

## Choose your run!
path_desc = "b"+voltage

## Choose simulation:
queue_time = "20:00:00"

## Server-specific queueing params
## Make sure you use the ENTIRE node!
## For Garnet this is 16 cores/node
if ("jade" or "garnet") in server:
  queue_cores = "16"
  queue_name = "AFPRD24930028"
  queue_type = "background"
elif "nyx" in server:
<<<<<<< HEAD
  queue_ppn = "8"
  #queue_name = "iainboyd"
  queue_name = "mjkush"
=======
  queue_ppn = "4"
  queue_name = "iainboyd"
  #queue_name = "mjkush"
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85

## Initialize arrays/paths
toppath = os.getcwd()
oldpath = path_letter + "-00-container"

## Make sure enough runs/skips occur
#ii = 0
run_first = 1
<<<<<<< HEAD
if "TEST" in data_set:
  run_last = 11
  run_skip = 2
elif "DSB" in data_set:
  run_last = 11
  #run_skip = 1
  run_skip = 2
=======
if "DSB" in data_set:
  run_last = 11
  run_skip = 1
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85
elif "DS4" in data_set:
  run_last = 12
  run_skip = 1
elif "DS5" in data_set:
  run_last = 34
  run_skip = 3
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
## DSB (t-v)
if "DS5" in data_set:
  if voltage == "-10":
    array_I = numpy.array([12.440,\
                           12.289,\
                           12.088,\
                           11.746,\
                           11.283,\
                           10.820,\
                           10.376,\
                           9.856,\
                           8.270,\
                           7.615,\
                           5.205,\
                           4.160])*1e-9
  elif voltage == "00":
    array_I = numpy.array([12.194,\
                           11.974,\
                           11.681,\
                           11.190,\
                           10.537,\
                           9.897,\
                           9.296,\
                           8.607,\
                           6.620,\
                           5.851,\
                           3.311,\
                           2.368])*1e-9
  elif voltage == "10":
    array_I = numpy.array([14.130,\
                           13.250,\
                           12.146,\
                           10.441,\
                           8.448,\
                           6.776,\
                           5.434,\
                           4.144,\
                           1.645,\
                           1.065,\
                           0.143,\
                           0.044])*1e-9
  elif voltage == "20":
    array_I = numpy.array([17.388,\
                           15.878,\
                           14.043,\
                           11.341,\
                           8.408,\
                           6.157,\
                           4.509,\
                           3.074,\
                           0.833,\
                           0.451,\
                           0.027,\
                           0.005])*1e-9
<<<<<<< HEAD
elif "TEST" in data_set:
  array_I = numpy.array([16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73,\
                         16.73])/4.0*1e-9
  array_N = numpy.array([500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500,\
                         500])
=======
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85
elif "DSB" in data_set:
  array_I = numpy.array([16.73,\
                         16.70,\
                         16.63,\
                         16.52,\
                         16.23,\
                         15.81,\
                         14.19,\
                         13.07,\
                         11.55,\
                         9.59,\
                         7.26])*1e-9
<<<<<<< HEAD
  array_N = numpy.array([10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10,\
                         10])
=======
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85
elif "DS4" in data_set:
  if voltage == "-10":
    array_I = numpy.array([7.329,\
                           7.081,\
                           6.834,\
                           6.571,\
                           6.267,\
                           5.824,\
                           5.339,\
                           4.968,\
                           4.634,\
                           4.187,\
                           3.854,\
                           3.370])*1e-9
  elif voltage == "00":
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
  elif voltage == "10":
    array_I = numpy.array([5.121,\
                           4.225,\
                           3.671,\
                           3.241,\
                           2.852,\
                           2.408,\
                           2.017,\
                           1.760,\
                           1.550,\
                           1.292,\
                           1.112,\
                           0.861])*1e-9
  elif voltage == "20":
    array_I = numpy.array([5.292,\
                           4.314,\
                           3.708,\
                           3.238,\
                           2.813,\
                           2.328,\
                           1.901,\
                           1.620,\
                           1.391,\
                           1.108,\
                           0.912,\
                           0.638])*1e-9
  else:
    print "ERROR: Can't find input conditions for that voltage!"
    quit()
else:
  print "ERROR: Can't find that Data Set!"
  quit()

if "DS5" in data_set:
  array_P = numpy.array([1.53E-02,\
                         4.93E-02,\
                         9.53E-02,\
                         1.75E-01,\
                         2.87E-01,\
                         4.04E-01,\
                         5.21E-01,\
                         6.64E-01,\
                         1.15E+00,\
                         1.38E+00,\
                         2.44E+00,\
                         3.07E+00])
elif "DS4" in data_set:
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
<<<<<<< HEAD
elif "TEST" in data_set:
  array_P = numpy.array([4.23E-04,\
                         1.96E-03,\
                         5.00E-03,\
                         9.90E-03,\
                         2.36E-02,\
                         4.35E-02,\
                         1.26E-01,\
                         1.89E-01,\
                         2.84E-01,\
                         4.25E-01,\
                         6.38E-01]) # Pascals
=======
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85
elif "DSB" in data_set:
  array_P = numpy.array([4.23E-04,\
                         1.96E-03,\
                         5.00E-03,\
                         9.90E-03,\
                         2.36E-02,\
                         4.35E-02,\
                         1.26E-01,\
                         1.89E-01,\
                         2.84E-01,\
                         4.25E-01,\
                         6.38E-01]) # Pascals
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

  if "nyx" in server:
    init_text = ["",\
      "#!/bin/sh\n",\
      "#PBS -S /bin/sh\n",\
      "#PBS -A "+queue_name+"\n",\
      "#PBS -N i"+path_letter+path_desc+"R"+str(path_run).zfill(2)+"\n",\
<<<<<<< HEAD
        "#PBS -l nodes=2:ppn="+queue_ppn+",pmem=900mb,walltime="+queue_time+",qos="+queue_name+"\n",\
=======
        "#PBS -l nodes=1:ppn="+queue_ppn+",pmem=900mb,walltime="+queue_time+",qos="+queue_name+"\n",\
>>>>>>> 2737013a8ba7753a40376909f7bde075e7f87a85
      "#PBS -M pgiulian@umich.edu\n",\
      "#PBS -m abe\n",\
      "#PBS -V\n",\
      "#PBS -joe\n",\
      "\n",\
      "cd $PBS_O_WORKDIR\n",\
      "mpirun icepic\n",\
      "\n"]
  elif ("jade" or "garnet") in server:
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

  inFileName = oldpath + "/test_TEMPLATE.in"
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
  replaceStr = str(array_I[path_run-1])
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert pressure
  findStr= "$PRESSURE"                                  
  replaceStr = str(array_P[path_run-1])
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert voltage
  findStr= "$VOLTAGE"                                  
  replaceStr = voltage
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert N_in
  findStr= "$N_IN"                                  
  replaceStr = str(array_N[path_run-1])
  outputStr = outputStr.replace(findStr, replaceStr)

  ## Insert voltage
  findStr= "$VOLTAGE"                                  
  replaceStr = voltage
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

  #ii += 1
  print ""


