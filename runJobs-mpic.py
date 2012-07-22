#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=6:
  print 'Usage: runJobs [server name, e.g. "nyx/jade/garnet"] [data-set, e.g. "DS1/DS4/DS5"] [path-letter, e.g. "a-01/bb"] [IC bias-voltage, e.g. "-10/00/20"] [phase, e.g. "init/1500"]'
  sys.exit(0)

## Gather server variable
server = sys.argv[1]
data_set = str(sys.argv[2])
path_letter = str(sys.argv[3])
voltage = str(sys.argv[4])
path_phase = str(sys.argv[5])

if server not in ["garnet", "nyx", "jade"]:
  print "ERROR: Only built for garnet, jade, or nyx!"
  quit()

## Choose your run!
path_desc = "b"+voltage
W_offset = 100

## Choose simulation phase:
## THIS ISN"T CHOOSING RIGHT TIMES
if "init" in path_phase:
  if ("jade" or "garnet") in server:
    queue_time = "5:00:00"
  elif "nyx" in server:
    queue_time = "12:00:00"
elif "1500" in path_phase:
  if ("jade" or "garnet") in server:
    queue_time = "20:00:00"
  elif "nyx" in server:
    queue_time = "24:00:00"
else:
  print "ERROR: phase needs to be init or 1500"
  quit()

## Server-specific queueing params
if "nyx" in server:
  queue_ppn = "4"
  #queue_name = "iainboyd"
  queue_name = "mjkush"
elif ("jade" or "garnet") in server:
  ## Make sure you use the ENTIRE node!
  ## For Garnet this is 16 cores/node
  queue_cores = "16"
  queue_name = "AFPRD24930028"
  queue_type = "standard"
else:
  print "ERROR: Can't find that server!"
  quit()


## Initialize arrays/paths
toppath = os.getcwd()
oldpath = path_letter + "-00-container"
array_files = ["oxford.dat",\
               "spec.dat",\
               "wall.dat",\
               "grid.unf",\
               "grid.ngp",\
               "scatter.xexe",\
               "Qen.dat",\
               "link.dat"]

## Make sure enough runs/skips occur
ii = 0

run_first = 1

if "DS5" in data_set:
  run_last = 34 # brought down from 36
  run_skip = 3
elif "DS4" in data_set:
  run_last = 12
  run_skip = 1
elif "DS1" in data_set:
  run_last = 11
  run_skip = 1
else:
  print "ERROR: Can't find that data set!"
  quit()

array_runs = range(run_first,\
                   run_last+1,\
                   run_skip)

#array_runs = [2, 3, 5, 6, 7, 9, 10, 11, 12]

## Last minute parameters!
q = 1.602e-19
vi = 46900
ri = 1.27e-3
Ai = numpy.pi*ri*ri

## Data set input parameters
## Make sure to check for specific weighting
## variations (e.g., the y/z variation)
## DS5 (aa,bb
## DS4 (x,y,z)
## DS1 (t-v)
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
    array_Wspec = numpy.array([1.0E-07,\
                               9.9E-08,\
                               9.7E-08,\
                               9.4E-08,\
                               9.1E-08,\
                               8.7E-08,\
                               8.3E-08,\
                               7.9E-08,\
                               6.6E-08,\
                               6.1E-08,\
                               4.2E-08,\
                               3.3E-08])/W_offset
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
    array_Wspec = numpy.array([1.0E-07,\
                               9.8E-08,\
                               9.6E-08,\
                               9.2E-08,\
                               8.6E-08,\
                               8.1E-08,\
                               7.6E-08,\
                               7.1E-08,\
                               5.4E-08,\
                               4.8E-08,\
                               2.7E-08,\
                               1.9E-08])/W_offset
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
    array_Wspec = numpy.array([1.0E-07,\
                               9.4E-08,\
                               8.6E-08,\
                               7.4E-08,\
                               6.0E-08,\
                               4.8E-08,\
                               3.8E-08,\
                               2.9E-08,\
                               1.2E-08,\
                               7.5E-09,\
                               1.0E-09,\
                               3.1E-10])/W_offset
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
    array_Wspec = numpy.array([1.0E-07,\
                               9.1E-08,\
                               8.1E-08,\
                               6.5E-08,\
                               4.8E-08,\
                               3.5E-08,\
                               2.6E-08,\
                               1.8E-08,\
                               4.8E-09,\
                               2.6E-09,\
                               1.5E-10,\
                               2.9E-11])/W_offset
  else:
    print "ERROR: can't find input conditions for that voltage"
    quit()
elif "DS4" in  data_set:
  if voltage == "20":
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
    array_Wspec = numpy.array([10.,\
                               8.2,\
                               7.0,\
                               6.1,\
                               5.3,\
                               4.4,\
                               3.6,\
                               3.1,\
                               2.6,\
                               2.1,\
                               1.7,\
                               1.2])*1e-8/W_offset
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
    array_Wspec = numpy.array([10.,\
                               8.3,\
                               7.2,\
                               6.3,\
                               5.6,\
                               4.7,\
                               3.9,\
                               3.4,\
                               3.0,\
                               2.5,\
                               2.2,\
                               1.7])*1e-8/W_offset
  elif voltage == "05":
    array_I = numpy.array([5.349,\
                           4.511,\
                           3.992,\
                           3.590,\
                           3.226,\
                           2.810,\
                           2.445,\
                           2.204,\
                           2.007,\
                           1.765,\
                           1.597,\
                           1.363])*1e-9
    array_Wspec = numpy.array([10.,\
                               8.4,\
                               7.5,\
                               6.7,\
                               6.0,\
                               5.3,\
                               4.6,\
                               4.1,\
                               3.8,\
                               3.3,\
                               3.0,\
                               2.5])*1e-8/W_offset
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
    array_Wspec = numpy.array([10.,\
                               9.5,\
                               9.1,\
                               8.6,\
                               8.1,\
                               7.3,\
                               6.5,\
                               5.9,\
                               5.4,\
                               4.7,\
                               4.2,\
                               3.5])*1e-8/W_offset
  elif voltage == "-05":
    array_I = numpy.array([7.564,\
                           7.265,\
                           6.969,\
                           6.657,\
                           6.297,\
                           5.780,\
                           5.220,\
                           4.797,\
                           4.421,\
                           3.926,\
                           3.564,\
                           3.045])*1e-9
    array_Wspec = numpy.array([10.,\
                               9.6,\
                               9.1,\
                               8.8,\
                               8.3,\
                               7.6,\
                               6.9,\
                               6.3,\
                               5.8,\
                               5.2,\
                               4.7,\
                               4.0])*1e-8/W_offset
  elif voltage == "-10":
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
    array_Wspec = numpy.array([10.,\
                               9.7,\
                               9.3,\
                               9.0,\
                               8.6,\
                               7.9,\
                               7.3,\
                               6.8,\
                               6.3,\
                               5.7,\
                               5.3,\
                               4.6])*1e-8/W_offset
  else:
    print "ERROR: Can't find input conditions for that voltage!"
    quit()
elif "DS1" in data_set:
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
  array_Wspec = numpy.array([10.,\
                             10.,\
                             9.9,\
                             9.9,\
                             9.7,\
                             9.5,\
                             8.5,\
                             7.8,\
                             6.9,\
                             5.7,\
                             4.3])*1e-8/W_offset*50.0
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
                         3.07E+00])/133.32

  array_W = numpy.array([3.0E+09,\
                         9.7E+09,\
                         1.9E+10,\
                         3.4E+10,\
                         5.6E+10,\
                         7.9E+10,\
                         1.0E+11,\
                         1.3E+11,\
                         2.3E+11,\
                         2.7E+11,\
                         4.8E+11,\
                         6.0E+11])*2.0
elif "DS4" in data_set:
  array_P = numpy.array([7.00e-2,\
                         1.33e-1,\
                         1.99e-1,\
                         2.71e-1,\
                         3.58e-1,\
                         4.93e-1,\
                         6.53e-1,\
                         7.85e-1,\
                         9.13e-1,\
                         1.10e+0,\
                         1.25e+0,\
                         1.50e+0])/133.32

  array_W = numpy.array([1.0e+8,\
                         1.9e+8,\
                         2.8e+8,\
                         3.9e+8,\
                         5.1e+8,\
                         7.0e+8,\
                         9.3e+8,\
                         1.1e+9,\
                         1.3e+9,\
                         1.6e+9,\
                         1.8e+9,\
                         2.1e+9])*10*3
elif "DS1" in data_set:
  array_P = numpy.array([2.07E-03,\
                         9.61E-03,\
                         2.45E-02,\
                         4.85E-02,\
                         1.16E-01,\
                         2.13E-01,\
                         6.18E-01,\
                         9.26E-01,\
                         1.39E+00,\
                         2.08E+00,\
                         3.13E+00])/133.32

  array_W = numpy.array([1.0E+08,\
                         4.6E+08,\
                         1.2E+09,\
                         2.3E+09,\
                         5.6E+09,\
                         1.0E+10,\
                         3.0E+10,\
                         4.5E+10,\
                         6.7E+10,\
                         1.0E+11,\
                         1.5E+11])
else:
  print "ERROR: Can't find that Data Set!"
  quit()

array_ni = array_I/(q*vi*Ai)
T = 298
k = 1.38e-23
array_nn = (array_P*133.32)/(k*T)

###########################
## Write dsmc.dat
##########################
def write_dsmc():
  filename = "dsmc.dat"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")

  if "init" in path_phase:
    init_text = ["",\
        "3.0e-05    ! Reference time step\n",\
        "%.1e" % array_W[ii] + "    ! 1.5e9 Reference particle weight (Nreal/Nmodel)\n",\
        "50000      ! Number of simulation steps before sampling\n",\
        "60000      ! Total number of simulation steps\n",\
        "5000       ! Interval: Write restart file\n",\
        "1          ! Interval: Sample particle data\n",\
        "1000       ! Interval: Evaluate macroscopic data\n",\
        "1000       ! Interval: Print output\n",\
        "100000000  ! Interval: Particle domain decompositon\n",\
        "1E-14      ! Roundoff accuracy for the grid\n",\
        "PIC_AXI    ! Dimensionality:2D, AXI,3D\n"]
  elif "1500" in path_phase:
    init_text = ["",\
        "3.0e-08    ! Reference time step\n",\
        "%.1e" % array_W[ii] + "    ! 1.5e9 Reference particle weight (Nreal/Nmodel)\n",\
        "500000     ! Number of simulation steps before sampling\n",\
        "600000     ! Total number of simulation steps\n",\
        "5000       ! Interval: Write restart file\n",\
        "1          ! Interval: Sample particle data\n",\
        "1000       ! Interval: Evaluate macroscopic data\n",\
        "1000       ! Interval: Print output\n",\
        "100000000  ! Interval: Particle domain decompositon\n",\
        "1E-14      ! Roundoff accuracy for the grid\n",\
        "PIC_AXI    ! Dimensionality:2D, AXI,3D\n"]
  
  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"
  return

###########################
## Write flow.dat
##########################
def write_flow():
  filename = "flow.dat"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")
 
  if "init" in path_phase:
    init_text = ["",\
      "0.     0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_Wspec[ii] + "  ! Xe+\n"]
  elif "1500" in path_phase:
    init_text = ["",\
      "0.     0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_ni[ii] + " %.1e" % array_Wspec[ii] + "  ! Xe+\n"]

  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"
  return

##########################
## Write pbs.sh
##########################
def write_pbs():
  filename = "pbs.sh"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")

  if "init" in path_phase:
    if "nyx" in server:
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -N "+path_letter+"i"+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l nodes=1:ppn="+queue_ppn+",pmem=900mb,walltime="+queue_time+",qos="+queue_name+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m abe\n",\
        "#PBS -V\n",\
        "#PBS -joe\n",\
        "\n",\
        "cd $PBS_O_WORKDIR\n",\
        "mpirun monaco\n",\
        "\n"]
    elif ("jade" or "garnet") in server:
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -q "+queue_type+"\n",\
        "#PBS -N "+path_letter+"i"+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l ncpus="+queue_cores+",walltime="+queue_time+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m be\n",\
        "#PBS -j oe\n",\
        "#PBS -V\n",\
        "\n",\
        "cd $PBS_O_WORKDIR\n",\
        "aprun -n "+queue_cores+" monaco\n",\
        "\n"]
    else:
      print "ERROR: Can't write pbs.sh for that server!"
      quit()
  elif "1500" in path_phase:
    if "nyx" in server:
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -N "+path_letter+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l nodes=1:ppn="+queue_ppn+",pmem=900mb,walltime="+queue_time+",qos="+queue_name+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m abe\n",\
        "#PBS -V\n",\
        "#PBS -joe\n",\
        "\n",\
        "cd $PBS_O_WORKDIR\n",\
        "mpirun monaco\n",\
        "\n"]
    elif ("jade" or "garnet") in server:
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -q "+queue_type+"\n",\
        "#PBS -N "+path_letter+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l ncpus="+queue_cores+",walltime="+queue_time+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m be\n",\
        "#PBS -j oe\n",\
        "#PBS -V\n",\
        "\n",\
        "cd $PBS_O_WORKDIR\n",\
        "aprun -n "+queue_cores+" monaco\n",\
        "\n"]
    else:
      print "ERROR: Can't write pbs.sh for that server!"
      quit()

  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"
  return

##########################
## Write pic.cfg
##########################
def write_pic():
  filename = "pic.cfg"

  if "init" in path_phase:
    PATH = mypath + "/" + filename
    FILE = open(PATH,"w")
    init_text = ["",\
        "$PLASMABCS 6\n",\
        "-4 2 0.0 0	0.0	0	0.0	! outflow\n",\
        "-1 1 0.0 0	0.0	0	0.0	! EP top+bottom\n",\
        "-1 1 "+voltage+".0 0	0.0	0	0.0	! IC\n",\
        "-1 1 0.0 0	0.0	0	0.0	! AF\n",\
        "-2 2 0.0 0	0.0	0	0.0	! inlet\n",\
        "-8 2 0.0 0	0.0	0	0.0	! symmetry line\n",\
        "\n",\
        "$REPORT_SPAN\n",\
        "1000\n",\
        "\n",\
        "$PIC\n",\
        "0.026 " + "%.2e" % array_ni[ii] + " 0.0    !Ion temperature, ion number density, reference potential\n",\
        "\n",\
        "$MERGE_SMALL_NEUTRAL 1.0\n",\
        "\n",\
        "$PLASMA_POT_METHOD\n",\
        "0                    ! e-method = 0: Boltzmann, 2: detailed model\n",\
        "\n",\
        "$BEGIN_APPLY_E\n",\
        "60000               ! E_begin: after this step, electricity field is applied\n",\
        "\n",\
        "$BEAM_DIVERGENCE\n",\
        "0.35 2 1.27e-3         ! divergence angle, 2=y-axis, variation height(inlet)\n",\
        "\n",\
        "$END\n"]
    FILE.writelines(init_text)
    FILE.close()
    print filename + " created!"
  elif "1500" in path_phase:
    print "Skipping " + filename + "..."

  return

##########################
## Copy all other files
##########################
# Need to write something to copy all of the
# other necessary files into
def copy_files():
  if "init" in path_phase:
    for filename in array_files:
      if not os.path.isfile(oldpath + "/" + filename):
        print "ERROR: Where is \"" + filename + "\"?"
        quit()
      else:
        shutil.copyfile(oldpath + "/" + filename, mypath + "/" + filename)
      print "Copied " + filename + "!"
  elif "1500" in path_phase:
    print "Skipping copying of init files..."
  return

############################
## Main Loop
############################
for path_run in array_runs:
  mypath = path_letter + "-" + \
           path_desc + "-" + \
           path_phase + "-" + \
           "R" + str(path_run).zfill(2)

  print "------------------------------"
  print "Working on \"" + mypath + "\"!"

  if not os.path.isdir(mypath):
    if "1500" in path_phase:
      print "Copying init version..."
      subprocess.call("cp -r " + path_letter + \
                      "-" + path_desc + \
                      "-init-" + "R" + str(path_run).zfill(2) + \
                      "/" + " " + mypath + "/", \
                      shell=True)
    elif "init" in path_phase:
      print "Folder created!"
      os.makedirs(mypath)
  else:
    print "ERROR: Directory \"" + mypath + "\" already exists!"
    quit()

  write_dsmc()
  write_flow()
  write_pbs()
  write_pic()
  copy_files()
  
  os.chdir(mypath)
  subprocess.call("qsub pbs.sh", shell=True)
  os.chdir(toppath)

  ii += 1
  print ""


