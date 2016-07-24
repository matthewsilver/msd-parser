'''tiny_dirichlet.py'''

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
from collections import defaultdict

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

basedir = '../../../scratch/network/mssilver/mssilver/'
infile = basedir + 'msd_datapreprocessed_EVERYTHINGSORTED.txt'

time_start = time.time()

metadata = open(infile).read()
json_contents = ast.literal_eval(metadata)
print 'finished converting everything to dictionary objects at time {0}'.format(time.time()-time_start)

count = 0
all_data = []
artist_song_year = []
all_titles = []
blacklist_artists = ['melanie','japan','the emotions','spark','yes','bonnie tyler','electric light orchestra','melanie safka','sparks','ben watt','nelson riddle','Nelson Riddle;Yves Montand;Barbra Streisand','donna summer','daniel johnston','jackson sisters']
for json_object in json_contents:
    s = json_object['artist_name']+json_object['title']
    if not json_object['artist_name'].lower() in blacklist_artists and int(json_object['year']) >= 1970 and not s in all_titles:
        all_data.append(json_object['chord_changes'] + json_object['timbre_cat_counts']*3)
        artist_song_year.append((json_object['artist_name'],json_object['title'],json_object['year']))
        all_titles.append(json_object['artist_name']+json_object['title'])
        count += 1

# count = 0
# all_data = []
# artist_song_year = []
# blacklist_artists = ['melanie','japan','the emotions','spark','yes','bonnie tyler','electric light orchestra','melanie safka','sparks']
# for json_object in json_contents:
#     if not json_object['artist_name'].lower() in blacklist_artists:
#         all_data.append(json_object['timbre_cat_counts'])
#         artist_song_year.append((json_object['artist_name'],json_object['title'],json_object['year']))
#         count += 1        

all_data_big = [[10*a for a in l] for l in all_data]

powers = xrange(0,21)
alphas = [0.1*pow(2,i) for i in powers]
components = [100]
bic_vals = [0 for row in range(0,len(alphas))]
min_b = float("inf")
min_a = 0
# bic_vals = [0 for i in xrange(0,len(components))]

# m = sklearn.mixture.DPGMM(n_components=20,alpha=100)
# fit = m.fit_predict(all_data_big)
# bic_val = m.bic(np.array(all_data_big))

for idx, a in enumerate(alphas):
    print 'looking at alpha={0}'.format(a)
    m = sklearn.mixture.DPGMM(n_components=50, alpha=a)
    fit = m.fit_predict(all_data_big)
    b = m.bic(np.array(all_data_big))
    print 'bic for alpha={0}: {1}'.format(a,b)
    bic_vals[idx] = b
    if b < min_b:
        min_b = b
        min_a = a
        print 'new min values: a={0}, b={1}'.format(str(a),str(b))

print 'overall min values with a={0}: b={1}'.format(str(min_a),str(min_b))
#so far: c=27, a=819.2, b=67526734.0439

d = defaultdict()
for f in fit: 
    d[f] = []
for (f,a) in zip(fit,artist_song_year): 
    d[f].append(a)
with open('output/song_groupings0.5.txt','w') as f:
    f.write(str(d))



fit_filename = 'output/msd_fit_categories0.5.txt'
freq_filename = 'output/msd_frequency_counts0.5.txt'
with open(fit_filename,'w') as text_file:
    text_file.write(str(fit))
counter=collections.Counter(fit)
with open(freq_filename,'w') as text_file:
   text_file.write(str(counter.values()))