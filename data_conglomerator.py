''' data_conglomerator.py 
This program takes the pitch/timbre/etc. data from each file, combines them all into one dataset, 
and then runs the dirichlet process on everything '''

import hdf5_getters #not on adroit
import msd_utils #not on adroit
from __future__ import division
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

scratch_dir = './../../../../scratch/network/mssilver/mssilver/'
edm_textfile_everything = scratch_dir + 'msd_EDM_dataraw_EVERYTHING.txt'
edm_textfile_everything_sorted = scratch_dir + 'msd_EDM_dataraw_EVERYTHING_SORTED.txt'

# first put everything in the same text file
with open(edm_textfile_everything,'a') as f:
    f.write('{')
    for l1 in ascii_uppercase:
        for l2 in ascii_uppercase:
            directory = l1 + l2
            edm_textfile = scratch_dir + 'msd_dataraw_' + directory + '.txt'
            print 'looking at file {0} at time {1}'.format(edm_textfile,time.time())
            with open(edm_textfile,'r') as f2:
                json_contents = f2.read().strip()[1:-1]
                f.write(json_contents)
                #don't insert comma after last file
                if not directory is 'ZZ':
                    f.write(', ')
    f.write('}')
print 'file merging complete at time {0}'.format(time.time())

# then sort the songs in the mega text file by year 
print 'reading all data and appending to a data structure at time {0}'.format(time.time())
json_contents = open(edm_textfile_everything,'r').read()

all_song_data = [] 
time_start = time.time()
count = 0
for json_object_str in re.finditer('{\'title.*?}',json_contents):
    json_object_str = str(json_object_str.group(0))
    json_object_str = json_object_str.replace('\'title\':', '\"title\":')
    json_object_str = json_object_str.replace('\'timbre\':', '\"timbre\":')
    json_object_str = json_object_str.replace('\'pitches\':', '\"pitches\":')
    json_object_str = json_object_str.replace('\'artist_name\':', '\"artist_name\":')
    json_object_str = json_object_str.replace('\'year\':', '\"year\":')
    json_object_str = json_object_str.replace('\'duration\':', '\"duration\":')
    # json_object_str = re.sub('(\')(title)(\'): (\')(.*)(\'),', r'"\2": "\5",', json_object_str)
    # json_object_str = re.sub('(\')(artist_name)(\'): (\')(.*)(\'),', r'"\2": "\5",', json_object_str)
    # json_object = json.loads(json_object_str)
    json_object = ast.literal_eval(json_object_str)
    all_song_data.append(json_object)
    count += 1
    print 'appended song {0} at {1} seconds after start'.format(count,time.time() - time_start)

print 'beginning sorting of song data at time {0}'.format(time.time())
all_song_data_sorted = sorted(all_song_data, key=lambda k: k['year'], reverse=True)
with open(edm_textfile_everything_sorted, 'w') as f:
    f.write(str(all_song_data_sorted))
# then feed it all into the dirichlet process

















