'''timbre_random_selector.py'''

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
import random

timbre_all = []
N = 20 #number of samples to get from each year
year_counts = dict({1956: 2, 1965: 4, 1968: 3, 1969: 5, 1970: 23, 1971: 25, 1972: 26, 1973: 37, 1974: 35, 1975: 29, 1976: 28, 1977: 64, 1978: 77, 1979: 111, 1980: 131, 1981: 171, 1982: 199, 1983: 272, 1984: 190, 1985: 189, 1986: 200, 1987: 224, 1988: 205, 1989: 272, 1990: 358, 1991: 348, 1992: 538, 1993: 610, 1994: 658, 1995: 764, 1996: 809, 1997: 930, 1998: 872, 1999: 983, 2000: 1031, 2001: 1230, 2002: 1323, 2003: 1563, 2004: 1508, 2005: 1995, 2006: 1892, 2007: 2175, 2008: 1950, 2009: 1782, 2010: 742})

time_start = time.time()
year_count = defaultdict(int)
orig_dir = './../../scratch/network/mssilver/mssilver/'
# orig_dir = './'
json_pattern = re.compile('{\'title.*?}',re.DOTALL)
N = 20 #number of songs to sample from each year
k = 20 #number of frames to select from each song
for l1 in ascii_uppercase:
    for l2 in ascii_uppercase:
        edm_textfile = orig_dir + 'msd_dataraw_' + l1 + l2 + '.txt'
        json_contents = open(edm_textfile,'r').read()
        for json_object_str in re.findall(json_pattern,json_contents):
            json_object = ast.literal_eval(json_object_str)
            year = int(json_object['year'])
            prob = 1.0 if 1.0*N/year_counts[year] > 1.0 else 1.0*N/year_counts[year]
            if random.random() < prob:
                print 'getting timbre frames for song in directory {0} {1} seconds after start of program'.format(edm_textfile,time.time()-time_start)
                duration = float(json_object['duration'])
                timbre = [[t/duration for t in l] for l in json_object['timbre']]
                try: 
                    indices = random.sample(xrange(0,len(timbre)),k)
                except:
                    indices = xrange(0,len(timbre))
                timbre_frames = [timbre[i] for i in indices]
                appended_timbre = [timbre_all.append(l) for l in timbre_frames]
        print 'finished file {0} {1} seconds after start of program'.format(edm_textfile,time.time()-time_start)

with(open('timbre_frames_all.txt','w')) as f:
    f.write(str(timbre_all))