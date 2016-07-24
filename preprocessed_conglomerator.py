''' preprocessed_conglomerator.py 
Takes the preprocessed msd files, then adds them together and sorts by year so that
it can be fed into the dirichlet process'''

from __future__ import division
import hdf5_getters #not on adroit
import msd_utils #not on adroit
import os
import sys
import re
import time
import json
import glob 
import sklearn.mixture
import math
import numpy as np
import collections
from string import ascii_uppercase
import ast
import matplotlib.pyplot as plt
import operator

basedir = '../../../scratch/network/mssilver/mssilver/'
edm_textfile_everything_sorted = basedir + 'msd_datapreprocessed_EVERYTHINGSORTED.txt'
time_start = time.time()

all_song_data = []
for l1 in ascii_uppercase:
    for l2 in ascii_uppercase:
    	infile = basedir + 'msd_datapreprocessed_' + l1 + l2 + '.txt'
    	json_contents = open(infile,'r').read()
    	for json_object in ast.literal_eval(json_contents):
    		all_song_data.append(json_object)
    	print 'file {0} finished at time {1}'.format(infile,time.time()-time_start)

all_song_data_sorted = sorted(all_song_data, key=lambda k: k['year'])
all_song_data_sorted.pop(0) #the first song doesn't appear to be electronic
with open(edm_textfile_everything_sorted, 'w') as f:
    f.write(str(all_song_data_sorted))
