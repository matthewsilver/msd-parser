'''timbre_mover.py'''

from __future__ import division
import os
import sys
import re
import time
import json
import glob 
import hdf5_getters #not on adroit
import sklearn.mixture
import msd_utils #not on adroit
import math
import numpy as np
import collections
from string import ascii_uppercase
import ast
import matplotlib.pyplot as plt
import operator
from collections import defaultdict

time_start = time.time()
year_count = defaultdict(int)
orig_dir = './../../scratch/network/mssilver/mssilver/'
json_pattern = re.compile('{\'title.*?}',re.DOTALL)
# orig_dir = '.'
for l1 in ascii_uppercase:
    for l2 in ascii_uppercase:
        edm_textfile = orig_dir + 'msd_dataraw_' + l1 + l2 + '.txt'
        json_contents = open(edm_textfile,'r').read()
        for json_object_str in re.findall(json_pattern,json_contents):
            json_object = ast.literal_eval(json_object_str)
            year_count[json_object['year']] += 1
        print 'finished file {0} {1} seconds after start of program'.format(edm_textfile,time.time()-time_start)
        print 'song distribution: {0}'.format(year_count)

print 'number of songs from each year:\n {0}'.format(year_count)

# json_contents = open(edm_textfile,'r').read()     
# count = 0
# for json_object_str in re.finditer('{.*?}',json_contents):
#     print json_object_str.group(0)
#     json_object = ast.literal_eval(json_object_str.group(0))
#     classification = edm_classifications[count]
#     classification_arrays[classification].append((json_object['chord_changes'],json_object['duration']))
#     classifications_artistsong[classification].append((json_object['artist_name'],json_object['title']))
#     count += 1