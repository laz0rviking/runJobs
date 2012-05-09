#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=2:
  print 'Usage: runJobs [server name, e.g. "nyx", "garnet"]'
  sys.exit(0)

## Gather server variable
server = sys.argv[1]

if not server == ("garnet" or "nyx"):
  print "ERROR: Only built for garnet or nyx!"
  quit()

## Choose your run!
data_set = "DS5"
path_letter = "aa"
voltage = "00"
path_desc = "bias"+voltage

## Choose simulation phase:
path_phase = "init"
queue_time = "12:00:00"
#path_phase = "1500"
#queue_time = "24:00:00"

## Server-specific queueing params
if server == "nyx":
  queue_ppn = "4"
  queue_name = "iainboyd"
  #queue_name = "mjkush"
elif server == "garnet":
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
if data_set == "DS5":
  if voltage == "-10":
    array_I = numpy.array([12.440,\
                          12.381,\
                          12.319,\
                          12.289,\
                          12.260,\
                          12.167,\
                          12.088,\
                          12.016,\
                          11.893,\
                          11.746,\
                          11.595,\
                          11.438,\
                          11.283,\
                          11.138,\
                          10.972,\
                          10.820,\
                          10.684,\
                          10.499,\
                          10.376,\
                          10.219,\
                          10.032,\
                          9.856,\
                          9.248,\
                          8.875,\
                          8.270,\
                          8.108,\
                          7.865,\
                          7.615,\
                          6.660,\
                          5.865,\
                          5.205,\
                          4.572,\
                          4.508,\
                          4.160,\
                          3.674,\
                          3.081])*1e-9
    array_Wspec = numpy.array([1.0E-07,\
                              1.0E-07,\
                              9.9E-08,\
                              9.9E-08,\
                              9.9E-08,\
                              9.8E-08,\
                              9.7E-08,\
                              9.7E-08,\
                              9.6E-08,\
                              9.4E-08,\
                              9.3E-08,\
                              9.2E-08,\
                              9.1E-08,\
                              9.0E-08,\
                              8.8E-08,\
                              8.7E-08,\
                              8.6E-08,\
                              8.4E-08,\
                              8.3E-08,\
                              8.2E-08,\
                              8.1E-08,\
                              7.9E-08,\
                              7.4E-08,\
                              7.1E-08,\
                              6.6E-08,\
                              6.5E-08,\
                              6.3E-08,\
                              6.1E-08,\
                              5.4E-08,\
                              4.7E-08,\
                              4.2E-08,\
                              3.7E-08,\
                              3.6E-08,\
                              3.3E-08,\
                              3.0E-08,\
                              2.5E-08])
    if path_letter == "bb":
      array_Wspec = array_Wspec/100
  else:
    print "ERROR: can't find input conditions for that voltage"
    quit()
elif data_set == "DS4":
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
                               1.2])*1e-8
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
                               1.7])*1e-8
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
                               2.5])*1e-8
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
                               3.5])*1e-8/100
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
                               4.0])*1e-8
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
                               4.6])*1e-8/100
  else:
    print "ERROR: Can't find input conditions for that voltage!"
    quit()
else:
  print "ERROR: Can't find that Data Set!"
  quit()

if data_set == "DS5":
  array_P = numpy.array([1.53E-02,\
                         2.87E-02,\
                         4.27E-02,\
                         4.93E-02,\
                         5.60E-02,\
                         7.73E-02,\
                         9.53E-02,\
                         1.12E-01,\
                         1.41E-01,\
                         1.75E-01,\
                         2.11E-01,\
                         2.49E-01,\
                         2.87E-01,\
                         3.23E-01,\
                         3.65E-01,\
                         4.04E-01,\
                         4.39E-01,\
                         4.88E-01,\
                         5.21E-01,\
                         5.63E-01,\
                         6.15E-01,\
                         6.64E-01,\
                         8.41E-01,\
                         9.56E-01,\
                         1.15E+00,\
                         1.21E+00,\
                         1.29E+00,\
                         1.38E+00,\
                         1.76E+00,\
                         2.11E+00,\
                         2.44E+00,\
                         2.80E+00,\
                         2.84E+00,\
                         3.07E+00,\
                         3.41E+00,\
                         3.90E+00])/133.32

  array_W = numpy.array([3.0E+09,\
                         5.6E+09,\
                         8.3E+09,\
                         9.7E+09,\
                         1.1E+10,\
                         1.5E+10,\
                         1.9E+10,\
                         2.2E+10,\
                         2.8E+10,\
                         3.4E+10,\
                         4.1E+10,\
                         4.9E+10,\
                         5.6E+10,\
                         6.3E+10,\
                         7.1E+10,\
                         7.9E+10,\
                         8.6E+10,\
                         9.5E+10,\
                         1.0E+11,\
                         1.1E+11,\
                         1.2E+11,\
                         1.3E+11,\
                         1.6E+11,\
                         1.9E+11,\
                         2.3E+11,\
                         2.4E+11,\
                         2.5E+11,\
                         2.7E+11,\
                         3.4E+11,\
                         4.1E+11,\
                         4.8E+11,\
                         5.5E+11,\
                         5.6E+11,\
                         6.0E+11,\
                         6.7E+11,\
                         7.6E+11])/5
elif data_set == "DS4":
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

  if path_phase == "init":
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
  elif path_phase == "1500":
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
 
  if path_phase == "init":
    init_text = ["",\
      "0.     0.	0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 	0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_Wspec[ii] + "  ! Xe+\n"]
  elif path_phase == "1500":
    init_text = ["",\
      "0.     0.	0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 	0. 298. 298. 298. 298. 298. " + "%.2e" % array_ni[ii] + " %.1e" % array_Wspec[ii] + "  ! Xe+\n"]

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

  if path_phase == "init":
    if server == "nyx":
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
    elif server == "garnet":
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -q "+queue_type+"\n",\
        "#PBS -N "+path_letter+"i"+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l ncpus="+queue_cores+",walltime="+queue_time+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m be\n",\
        "#PBS -V\n",\
        "#PBS -joe\n",\
        "\n",\
        "cd $PBS_O_WORKDIR\n",\
        "aprun -n "+queue_cores+" monaco\n",\
        "\n"]
    else:
      print "ERROR: Can't write pbs.sh for that server!"
      quit()
  elif path_phase == "1500":
    if server == "nyx":
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
    elif server == "garnet":
      init_text = ["",\
        "#!/bin/sh\n",\
        "#PBS -S /bin/sh\n",\
        "#PBS -A "+queue_name+"\n",\
        "#PBS -q "+queue_type+"\n",\
        "#PBS -N "+path_letter+path_desc+"R"+str(path_run).zfill(2)+"\n",\
        "#PBS -l ncpus="+queue_cores+",walltime="+queue_time+"\n",\
        "#PBS -M pgiulian@umich.edu\n",\
        "#PBS -m be\n",\
        "#PBS -V\n",\
        "#PBS -joe\n",\
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

  if path_phase == "init":
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
        "100\n",\
        "\n",\
        "$PIC\n",\
        "0.026 " + "%.2e" % array_ni[ii] + " 0.0    !Ion temperature, ion number density, reference potential\n",\
        "\n",\
        "$MERGE_SMALL_NEUTRAL 1.0\n",\
        "\n",\
        "$PLASMA_POT_METHOD\n",\
        "99                    ! e-method = 0: Boltzmann, 2: detailed model\n",\
        "\n",\
        "$BEGIN_APPLY_E\n",\
        "60000               ! E_begin: after this step, electricity field is applied\n",\
        "\n",\
        "BEAM_DIVERGENCE\n",\
        "0.0 2 1.27e-3         ! divergence angle, 2=y-axis, variation height(inlet)\n",\
        "\n",\
        "$END\n"]
    FILE.writelines(init_text)
    FILE.close()
    print filename + " created!"
  elif path_phase == "1500":
    print "Skipping " + filename + "..."

  return

##########################
## Copy all other files
##########################
# Need to write something to copy all of the
# other necessary files into
def copy_files():
  if path_phase == "init":
    for filename in array_files:
      if not os.path.isfile(oldpath + "/" + filename):
        print "ERROR: Where is \"" + filename + "\"?"
        quit()
      else:
        shutil.copyfile(oldpath + "/" + filename, mypath + "/" + filename)
      print "Copied " + filename + "!"
  elif path_phase == "1500":
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
    if path_phase == "1500":
      print "Copying init version..."
      subprocess.call("cp -r " + path_letter + \
                      "-" + path_desc + \
                      "-init-" + "R" + str(path_run).zfill(2) + \
                      "/" + " " + mypath + "/", \
                      shell=True)
    elif path_phase == "init":
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


