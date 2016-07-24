'''timbre_chord_calculator.py'''

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
import ast

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

#column-wise mean of list of lists
def mean(a):
    return sum(a) / len(a)

'''This code computes the frequency of chord changes in each electronic song and runs the dirichlet process on it '''

basedir = './../../scratch/network/mssilver/mssilver/'
input_file = basedir + 'msd_dataraw_' + str(sys.argv[1]) + '.txt'
output_file = basedir + 'msd_datapreprocessed_' + str(sys.argv[1]) + '.txt'

json_contents = open(input_file,'r').read()

all_song_data = [] 
time_start = time.time()
count = 0
for json_object_str in re.finditer('{\'title.*?}',json_contents):
    json_object_str = str(json_object_str.group(0))
    json_object = ast.literal_eval(json_object_str)
    json_object_new = {}

    json_object_new['title'] = json_object['title']
    json_object_new['artist_name'] = json_object['artist_name']
    json_object_new['year'] = json_object['year']
    json_object_new['duration'] = json_object['duration']

    segments_pitches_old = json_object['pitches']
    segments_timbre_old = json_object['timbre']
    segments_pitches_old_smoothed = []
    segments_timbre_old_smoothed = []
    chord_changes = [0 for i in range(0,192)]
    # based on time signature and BPM, estimate length of measure and use that
    # as unit of time to smooth pitches upon
    # smoothing_factor = max(3,round(len(segments_pitches_old) * 60.0 / (hdf5_getters.get_tempo(h5) * hdf5_getters.get_duration(h5))))
    smoothing_factor = 4
    for i in range(0,int(math.floor(len(segments_pitches_old))/smoothing_factor)):
        segments = segments_pitches_old[(smoothing_factor*i):(smoothing_factor*i+smoothing_factor)]
        # calculate mean frequency of each note over a block of 5 time segments
        segments_mean = map(mean, zip(*segments))
        segments_pitches_old_smoothed.append(segments_mean)
    most_likely_chords = [msd_utils.find_most_likely_chord(seg) for seg in segments_pitches_old_smoothed]
    print 'found most likely chords at {0} seconds'.format(time.time()-time_start)
    #calculate chord changes
    for i in range(0,len(most_likely_chords)-1):
        c1 = most_likely_chords[i]
        c2 = most_likely_chords[i+1]
        if (c1[1] == c2[1]):
            note_shift = 0
        elif (c1[1] < c2[1]):
            note_shift = c2[1] - c1[1]
        else:
            note_shift = 12 - c1[1] + c2[1]
        key_shift = 4*(c1[0]-1) + c2[0]
        # convert note_shift (0 through 11) and key_shift (1 to 16)
        # to one of 196 categories for a chord shift
        chord_shift = 12*(key_shift - 1) + note_shift
        chord_changes[chord_shift] += 1
    json_object_new['chord_changes'] = [c/json_object['duration'] for c in chord_changes]
    print 'calculated chord changes at {0} seconds'.format(time.time()-time_start)
        
    for i in range(0,int(math.floor(len(segments_timbre_old))/smoothing_factor)):
        segments = segments_timbre_old[(smoothing_factor*i):(smoothing_factor*i+smoothing_factor)]
        # calculate mean frequency of each note over a block of 5 time segments
        segments_mean = map(mean, zip(*segments))
        segments_timbre_old_smoothed.append(segments_mean)
    print 'found most likely timbre categories at {0} seconds'.format(time.time()-time_start)
    timbre_cats = [msd_utils.find_most_likely_timbre_category(seg) for seg in segments_timbre_old_smoothed]
    timbre_cat_counts = [timbre_cats.count(i) for i in xrange(0,46)]
    json_object_new['timbre_cat_counts'] = [t/json_object['duration'] for t in timbre_cat_counts]
    all_song_data.append(json_object_new)
    count += 1

print 'preprocessing finished, writing results to file at time {0}'.format(time.time()-time_start)
with open(output_file,'w') as f:
    f.write(str(all_song_data))

print 'file merging complete at time {0}'.format(time.time()-time_start)