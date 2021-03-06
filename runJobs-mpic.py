#!/usr/bin/env python

import sys,os,numpy,shutil,subprocess

## If arguments aren't given correctly, print a help message
if len(sys.argv)!=9:
  print 'Usage: runJobs [server name, e.g. "nyx/jade/garnet/arrakis"] [data-set, e.g. "DSB/DSC/DSD"] [path-letter, e.g. "a-01/bb"] [IC bias-voltage, e.g. "-10/00/20"] [phase, e.g. "init/1500/e"] [potential solve, e.g. "0/99"] [beam div., e.g. "0.0/0.2/0.3] [nyx queue, e.g. "iainboyd/mjkush"]'
  sys.exit(0)

## Gather server variable
server = sys.argv[1]
data_set = str(sys.argv[2])
path_letter = str(sys.argv[3])
voltage = str(sys.argv[4])
path_phase = str(sys.argv[5])
pot_solver = str(sys.argv[6])
beam_div = str(sys.argv[7])
queue_name = str(sys.argv[8])

if server not in ["garnet", "nyx", "jade", "arrakis"]:
  print "ERROR: Only built for garnet, jade, arrakis, or nyx!"
  quit()

## Choose your run!
path_desc = "b"+voltage
W_offset = 100

toggleUPoffset = 0

## Choose simulation phase:
if "init" in path_phase:
  if server in ["jade", "garnet"]:
    queue_time = "4:00:00"
  elif "nyx" in server:
    queue_time = "12:00:00"
elif "1500" in path_phase:
  if server in ["jade", "garnet"]:
    queue_time = "04:00:00"
  elif "nyx" in server:
    queue_time = "24:00:00"
elif path_phase in ["EP", "IC"]:
  if server in ["jade", "garnet"]:
    queue_time = "04:00:00"
  elif "nyx" in server:
    queue_time = "24:00:00"
else:
  print "ERROR: phase needs to be init or 1500 or e"
  quit()

## Server-specific queueing params
if "nyx" in server:
  queue_ppn = "4"
elif server in ["jade", "garnet"]:
  ## Make sure you use the ENTIRE node!
  ## For Garnet this is 16 cores/node
  queue_cores = "16"
  queue_name = "AFPRD24930028"
  if "init" in path_phase:
    queue_type = "background"
  elif "1500" in path_phase:
    queue_type = "background"
elif "arrakis" in server:
  print "Skipping PBS shit for arrakis..."
else:
  print "ERROR: Can't find that server!"
  quit()


## Initialize arrays/paths
toppath = os.getcwd()
oldpath = path_letter + "-00-container"
array_files = ["oxford.dat",\
               "spec.dat",\
               "grid.unf",\
               "grid.ngp",\
               "scatter.xexe",\
               "Qen.dat",\
               "link.dat"]

## Make sure enough runs/skips occur
ii = 0

run_first = 1

if "DSD" in data_set:
  run_last = 34 # brought down from 36
  run_skip = 3
elif "DSC" in data_set:
  run_last = 12
  run_skip = 1
elif "DSB" in data_set:
  run_last = 11
  run_skip = 1
elif "DSA" in data_set:
  run_last = 9
  run_skip = 1
else:
  print "ERROR: Can't find that data set!"
  quit()

#if path_phase in ["EP", "IC"]:
#  run_last = 1

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
## DSD (aa,bb
## DSC (x,y,z)
## DSB (t-v)
if "DSD" in data_set:
  
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
    
    array_Wspec = numpy.array([10.*52,\
                               9.9*16,\
                               9.7*8,\
                               9.4*4.6,\
                               9.1*2.7,\
                               8.7*1.9,\
                               8.3*1.6,\
                               7.9*1.2,\
                               6.6*0.67,\
                               6.1*0.55,\
                               4.2*0.32,\
                               3.3*0.26])/W_offset*1e-8
  
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
    
    array_Wspec = numpy.array([10.*50,\
                               9.8*15,\
                               9.6*8.0,\
                               9.2*4.5,\
                               8.6*2.7,\
                               8.1*2.0,\
                               7.6*1.5,\
                               7.1*1.2,\
                               5.4*0.6,\
                               4.8*0.5,\
                               2.7*0.3,\
                               1.9*0.25])/W_offset*1e-8
  
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
    
    array_Wspec = numpy.array([10.*58,\
                               9.4*18,\
                               8.6*9.3,\
                               7.4*5.2,\
                               6.0*3.2,\
                               4.8*2.2,\
                               3.8*1.8,\
                               2.9*1.4,\
                               1.2*0.7,\
                               .75*0.6,\
                               .10*0.4,\
                               .031*0.3])/W_offset*1e-8
  
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

elif "DSC" in  data_set:

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

    array_Wspec = numpy.array([10.*4.5,\
                               8.3*2.2,\
                               7.2*1.6,\
                               6.3*1.1,\
                               5.6/1.1,\
                               4.7/1.5,\
                               3.9/2,\
                               3.4/2.5,\
                               3.0/3,\
                               2.5/3.7,\
                               2.2/4,\
                               1.7/5])*1e-8/W_offset # PNG

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

    array_Wspec = numpy.array([10.*6,\
                               9.5*3,\
                               9.1*2,\
                               8.6*1.3,\
                               8.1,\
                               7.3/1.2,\
                               6.5/1.5,\
                               5.9/2,\
                               5.4/2,\
                               4.7/3,\
                               4.2/3.1,\
                               3.5/3.2])*1e-8/W_offset

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

    array_Wspec = numpy.array([10.*6.5,\
                               9.7*3.5,\
                               9.3*2.5,\
                               9.0*1.5,\
                               8.6*1.2,\
                               7.9,\
                               7.3/1.5,\
                               6.8/1.8,\
                               6.3/2,\
                               5.7/2.8,\
                               5.3/2,\
                               4.6/3.1])*1e-8/W_offset #PNG tune this

  else:
    print "ERROR: Can't find input conditions for that voltage!"
    quit()

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

  array_Wspec = numpy.array([10.*10,\
                             10.*2,\
                             9.9/1.2,\
                             9.9/3,\
                             9.7/6,\
                             9.5/10,\
                             8.5/30,\
                             7.8/50,\
                             6.9/90,\
                             5.7/100,\
                             4.3/120])*1e-8/W_offset*50.0

elif "DSA" in data_set:
  
  array_I = numpy.array([17.727,\
                         17.357,\
                         17.053,\
                         16.216,\
                         15.329,\
                         14.522,\
                         13.418,\
                         12.689,\
                         8.108])*1e-9

  array_Wspec = numpy.array([10.,\
                             9.8/10,\
                             9.6/20,\
                             9.1/40,\
                             8.6/80,\
                             8.2/160,\
                             7.6/320,\
                             7.2/640,\
                             4.6/1280])*1e-8/W_offset*50.0*10.0

else:
  
  print "ERROR: Can't find that Data Set!"
  quit()


# SEE params

if "DSA" in data_set:
  
  array_G_SEE_EP = numpy.array([3.70E+09,\
                                1.48E+11,\
                                2.69E+11,\
                                6.21E+11,\
                                9.95E+11,\
                                1.36E+12,\
                                1.92E+12,\
                                2.95E+12,\
                                5.53E+12])

  array_W_SEE_EP = numpy.array([1.00*40/1000/1.25,\
                                2.69/100,\
                                2.61/50/2,\
                                4.03/28/5,\
                                5.60/48/4,\
                                9.08/80/4,\
                                8.78/128/2,\
                                8.30/192/1.2,\
                                8.78/256/1.2])*1e-12

  array_G_SEE_IC = numpy.array([4.80E+09,\
                                9.02E+10,\
                                1.54E+11,\
                                2.53E+11,\
                                3.04E+11,\
                                3.36E+11,\
                                3.65E+11,\
                                3.50E+11,\
                                1.43E+11])

  array_W_SEE_IC = numpy.array([1.00*40/1000/1.25*2.0,\
                                2.69/100,\
                                2.61/50/2,\
                                4.03/28/5/1.5,\
                                5.60/48/4/2,\
                                9.08/80/4/2.5,\
                                8.78/128/2/3,\
                                8.30/192/1.2/4,\
                                8.78/256/1.2/20])*1e-11*1.25

elif "DSB" in data_set:
  # Dummy
  
  array_G_SEE_EP = numpy.array([1.00E+09,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+12,\
                                1.00E+12,\
                                1.00E+12,\
                                1.00E+12,\
                                1.00E+12,\
                                1.00E+12])

  array_W_SEE_EP = numpy.array([1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00])*1e-12

  array_G_SEE_IC = numpy.array([1.00E+09,\
                                1.00E+10,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11,\
                                1.00E+11])

  array_W_SEE_IC = numpy.array([1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00])*1e-12

elif "DSC" in data_set:

  if voltage == "-10":
  
    array_G_SEE_EP = numpy.array([0.0284,\
                                  0.0578,\
                                  0.0872,\
                                  0.1323,\
                                  0.1884,\
                                  0.2663,\
                                  0.3921,\
                                  0.4890,\
                                  0.7859,\
                                  1.2548,\
                                  0.9327,\
                                  2.4177])*1e13

    array_W_SEE_EP = numpy.array([1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/30*1e-12

    array_G_SEE_IC = numpy.array([0.5799,\
                                  0.8603,\
                                  1.0663,\
                                  1.1908,\
                                  1.3218,\
                                  1.4684,\
                                  1.5303,\
                                  1.5441,\
                                  1.5340,\
                                  1.4344,\
                                  1.3533,\
                                  1.1688])*1e10

    array_W_SEE_IC = numpy.array([1.00*5.0,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/100/3000*1e-9

  elif voltage == "00":
  
    # Dummy

    array_G_SEE_EP = numpy.array([0.13,\
                                  0.25,\
                                  0.38,\
                                  0.53,\
                                  0.66,\
                                  0.93,\
                                  1.24,\
                                  1.50,\
                                  1.73,\
                                  2.08,\
                                  2.39,\
                                  2.83])*1e12

    array_W_SEE_EP = numpy.array([1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/30*1e-12

    array_G_SEE_IC = numpy.array([0.592,\
                                  0.86,\
                                  1.13,\
                                  1.19,\
                                  1.34,\
                                  1.50,\
                                  1.54,\
                                  1.61,\
                                  1.59,\
                                  1.43,\
                                  3.15,\
                                  3.15])*1e10

    array_W_SEE_IC = numpy.array([1.00*5.0,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/100/3000*1e-9


  elif voltage == "10":
  
    # Dummy

    array_G_SEE_EP = numpy.array([0.13,\
                                  0.25,\
                                  0.38,\
                                  0.53,\
                                  0.66,\
                                  0.93,\
                                  1.24,\
                                  1.50,\
                                  1.73,\
                                  2.08,\
                                  2.39,\
                                  2.83])*1e12

    array_W_SEE_EP = numpy.array([1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/30*1e-12

    array_G_SEE_IC = numpy.array([0.592,\
                                  0.86,\
                                  1.13,\
                                  1.19,\
                                  1.34,\
                                  1.50,\
                                  1.54,\
                                  1.61,\
                                  1.59,\
                                  1.43,\
                                  3.15,\
                                  3.15])*1e10

    array_W_SEE_IC = numpy.array([1.00*5.0,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00,\
                                  1.00])/100/3000*1e-9

elif "DSD" in data_set:
  # Dummy
  
  array_G_SEE_EP = numpy.array([0.33,\
                                0.25,\
                                0.38,\
                                0.53,\
                                0.53,\
                                0.66,\
                                0.93,\
                                1.24,\
                                1.73,\
                                2.08,\
                                2.39,\
                                2.83])*1e12

  array_W_SEE_EP = numpy.array([1.00*2,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00])/30*1e-12

  array_G_SEE_IC = numpy.array([1.32,\
                                1.77,\
                                2.09,\
                                2.45,\
                                2.50,\
                                2.86,\
                                3.05,\
                                2.97,\
                                2.97,\
                                2.66,\
                                2.65,\
                                2.35])*1e9

  array_W_SEE_IC = numpy.array([1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00,\
                                1.00])/100/3000*1e-9


# Pressures ad W_ref's
if "DSD" in data_set:
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
                         6.0E+11])*2.0/4.0 *2.0 # PNG REDUCED AGAIN

elif "DSC" in data_set:
  
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
                         2.1e+9])*10*3*3/1.25 *2.0 # PNG REDUCED AGAIN

elif "DSB" in data_set:
  
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
                         1.5E+11])*2.0 *2.0 # PNG REDUCED AGAIN

elif "DSA" in data_set:
  
  array_P = numpy.array([2.00E-03,\
                         8.06E-02,\
                         1.47E-01,\
                         3.35E-01,\
                         5.45E-01,\
                         7.46E-01,\
                         1.04E+00,\
                         1.25E+00,\
                         2.92E+00])/133.32

  array_W = numpy.array([1.0E+08,\
                         4.0E+09,\
                         7.3E+09,\
                         1.7E+10,\
                         2.7E+10,\
                         3.7E+10,\
                         5.2E+10,\
                         6.3E+10,\
                         1.5E+11])*2.0
else:
  print "ERROR: Can't find that Data Set!"
  quit()

## UP OFFSET
## Add these to the total input current!

if toggleUPoffset == 1:

  if "DSB" in data_set:

    UPoffset = numpy.array([0.0036,\
                            0.0185,\
                            0.0471,\
                            0.0983,\
                            0.2849,\
                            0.5686,\
                            1.3314,\
                            1.2109,\
                            1.0357,\
                            0.9725,\
                            0.7324])*1e-9

    array_I = array_I + UPoffset

  elif "DSC" in data_set:

    UPoffset = numpy.array([0.3766,\
                            0.4706,\
                            0.4900,\
                            0.5070,\
                            0.4852,\
                            0.4547,\
                            0.4023,\
                            0.3306,\
                            0.2769,\
                            0.2183,\
                            0.1918,\
                            0.1431])*1e-9

    array_I = array_I + UPoffset

  elif "DSD" in data_set:

    UPoffset = numpy.array([0.2812,\
                            0.7786,\
                            1.3072,\
                            1.8865,\
                            2.3040,\
                            2.2468,\
                            2.2455,\
                            1.8579,\
                            0.7133,\
                            0.4667,\
                            0.0632,\
                            0.0177])*1e-9

    array_I = array_I + UPoffset

  else:
    print "ERROR: in UP offset!"
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
        "1E-20      ! Roundoff accuracy for the grid\n",\
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
        "1E-20      ! Roundoff accuracy for the grid\n",\
        "PIC_AXI    ! Dimensionality:2D, AXI,3D\n"]

  elif path_phase in ["EP", "IC"]:
    init_text = ["",\
        "3.0e-12    ! Reference time step\n",\
        "%.1e" % array_W[ii] + "    ! 1.5e9 Reference particle weight (Nreal/Nmodel)\n",\
        "1000000     ! Number of simulation steps before sampling\n",\
        "1100000     ! Total number of simulation steps\n",\
        "5000       ! Interval: Write restart file\n",\
        "1          ! Interval: Sample particle data\n",\
        "1000       ! Interval: Evaluate macroscopic data\n",\
        "1000       ! Interval: Print output\n",\
        "100000000  ! Interval: Particle domain decompositon\n",\
        "1E-20      ! Roundoff accuracy for the grid\n",\
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
      "46900. 0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_Wspec[ii] + "  ! Xe+\n",\
      "0.     0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_W_SEE_EP[ii] + "  ! e-\n"]
  elif "1500" in path_phase:
    init_text = ["",\
      "0.     0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_ni[ii] + " %.1e" % array_Wspec[ii] + "  ! Xe+\n",\
      "0.     0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_W_SEE_EP[ii] + "  ! e-\n"]
  elif "EP" in path_phase:
    init_text = ["",\
      "0.     0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_ni[ii] + " %.1e" % array_Wspec[ii] + "  ! Xe+\n",\
      "0.     0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_W_SEE_EP[ii] + "  ! e-\n"]
  elif "IC" in path_phase:
    init_text = ["",\
      "0.     0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_nn[ii] + " 1.0 ! Xe\n",\
      "46900. 0. 0. 298. 298. 298. 298. 298. " + "%.2e" % array_ni[ii] + " %.1e" % array_Wspec[ii] + "  ! Xe+\n",\
      "0.     0. 0. 298. 298. 298. 298. 298. 0.00e+00 %.1e" % array_W_SEE_IC[ii] + "  ! e-\n"]

  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"
  return

###########################
## Write SEE.dat
##########################
def write_wall():
  filename = "wall.dat"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")
 
  if "EP" in path_phase:
    init_text = ["",\
      "300.0 1.0 0.0 1 ! EP\n",\
      "300.0 1.0 0.0 0 ! IC\n",\
      "300.0 1.0 0.0 0 ! UP\n"]
  elif "IC" in path_phase:
    init_text = ["",\
      "300.0 1.0 0.0 0 ! EP\n",\
      "300.0 1.0 0.0 1 ! IC\n",\
      "300.0 1.0 0.0 0 ! UP\n"]
  else:
    init_text = ["",\
      "300.0 1.0 0.0 0 ! EP\n",\
      "300.0 1.0 0.0 0 ! IC\n",\
      "300.0 1.0 0.0 0 ! UP\n"]

  FILE.writelines(init_text)
  FILE.close()
  print filename + " created!"
  return

###########################
## Write SEE.dat
##########################
def write_SEE():
  filename = "SEE.dat"

  PATH = mypath + "/" + filename
  FILE = open(PATH,"w")
 
  if "EP" in path_phase:
    init_text = ["",\
      "1 0.0\n",\
      "2 0.0\n",\
      "3 " + "%.2e" % array_G_SEE_EP[ii] + "\n"]
  elif "IC" in path_phase:
    init_text = ["",\
      "1 0.0\n",\
      "2 0.0\n",\
      "3 " + "%.2e" % array_G_SEE_IC[ii] + "\n"]
  else:
    print "ERROR: SEE.dat should only be called for e run!"
    quit()

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
        "mpirun monaco_test_double\n",\
        "\n"]
    elif server in ["jade", "garnet"]:
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
        "aprun -n "+queue_cores+" monaco_test_double\n",\
        "\n"]
    elif "arrakis" in server:
      print "skipped!"
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
        "mpirun monaco_test_double\n",\
        "\n"]
    elif server in ["jade", "garnet"]:
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
        "aprun -n "+queue_cores+" monaco_test_double\n",\
        "\n"]
    elif "arrakis" in server:
      print "skipped!"
    else:
      print "ERROR: Can't write pbs.sh for that server!"
      quit()
  elif path_phase in ["EP", "IC"]:
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
        "mpirun monaco_test_double\n",\
        "\n"]
    elif server in ["jade", "garnet"]:
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
        "aprun -n "+queue_cores+" monaco_test_double\n",\
        "\n"]
    elif "arrakis" in server:
      print "skipped!"
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
        "-1 1 0.0 0	0.0	0	0.0	! EP \n",\
        "-1 1 "+voltage+".0 0	0.0	0	0.0	! IC\n",\
        "-1 1 0.0 0	0.0	0	0.0	! UP\n",\
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
        ""+pot_solver+"                 ! e-method = 0: Boltzmann, 2: detailed model\n",\
        "\n",\
        "$BEGIN_APPLY_E\n",\
        "600000               ! E_begin: after this step, electricity field is applied\n",\
        "\n",\
        "$BEAM_DIVERGENCE\n",\
        ""+beam_div+" 2 1.27e-3         ! divergence angle, 2=y-axis, variation height(inlet)\n",\
        "\n",\
        "$END\n"]
    FILE.writelines(init_text)
    FILE.close()
    print filename + " created!"
  elif path_phase in ["1500", "EP", "IC"]:
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
  elif path_phase in ["1500", "EP", "IC"]:
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
    elif path_phase in ["EP", "IC"]:
      print "Copying 1500 version..."
      subprocess.call("cp -r " + path_letter + \
                      "-" + path_desc + \
                      "-1500-" + "R" + str(path_run).zfill(2) + \
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
  write_wall()
  
  if server in ["jade", "garnet", "nyx"]:
    write_pbs()

  if path_phase in ["EP", "IC"]:
    write_SEE()
  
  write_pic()
  copy_files()
  
  os.chdir(mypath)
  
  if server in ["jade", "garnet", "nyx"]:
    subprocess.call("qsub pbs.sh", shell=True)
  #elif "arrakis" in server:
  # Just wait and call it later!
  #  subprocess.call("mpirun -n 2 monaco", shell=True)
  
  os.chdir(toppath)

  ii += 1
  print ""


