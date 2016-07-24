'''quick_dirichlet.py'''
from __future__ import division
import os
import re
import time
import json
import glob
import hdf5_getters
import sklearn.mixture
import msd_utils
import math
import numpy as np
import collections
import ast

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan) 

infile = './output/msd_EDM_sortedpitchdata_EVERYTHING_SORTED.txt'
dicts = []

json_contents = open(infile,'r').read()
for json_object_str in re.finditer('{.*?}',json_contents):
    song_metadata = ast.literal_eval(json_object_str.group(0))
    print('metadata: {}'.format(song_metadata))
    dicts.append(song_metadata)

print('dictionaries successfully created...')
print('dictionaries: {}'.format(dicts))

pitch_segs_data = []
m = sklearn.mixture.DPGMM(n_components=15, n_iter=10000, alpha=.005)
for d in dicts:
	print 'dictionary: {}'.format(d)
	pitch_segs_data.append(d['chord_changes'])
fit = m.fit_predict(pitch_segs_data)
print('fit categories: {0}'.format(fit))
counter=collections.Counter(fit)
print('frequency counts: {0}'.format(counter.values()))