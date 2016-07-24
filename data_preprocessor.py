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

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

all_song_data = [] 

edm_textfile_everything = './output/msd_EDM_sortedpitchdata_EVERYTHING.txt'
edm_textfile_everything_sorted = './output/msd_EDM_sortedpitchdata_EVERYTHING_SORTED.txt'

# first put everything in the same text file
with open(edm_textfile_everything,'a') as f:
    f.write('{')
    for l1 in ascii_uppercase:
        for l2 in ascii_uppercase:
            directory = l1 + l2
            edm_textfile = './output/msd_EDM_sortedpitchdata_' + directory + '.txt'
            print 'looking at file {0} at time {1}'.format(edm_textfile,time.time())
            with open(edm_textfile,'r') as f2:
                json_contents = f2.read().strip()[1:-1]
                f.write(json_contents)
                #don't insert comma after last file
                if not directory is 'ZZ':
                    f.write(', ')
    f.write('}')
print 'file merging complete at time {0}'.format(time.time())
