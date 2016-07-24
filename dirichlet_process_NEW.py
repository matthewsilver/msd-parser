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

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

#column-wise mean of list of lists
def mean(a):
    return sum(a) / len(a)

'''This code computes the frequency of chord changes in each electronic song and runs the dirichlet process on it '''

basedir = './../../scratch/network/mssilver/mssilver/msd_data_full/data/' + str(sys.argv[1]) 
ext = '.h5'

target_genres = ['house','techno','drum and bass','drum n bass','drum\'n\'bass',\
'drumnbass','drum \'n\' bass','jungle','breakbeat','trance','dubstep','trap','downtempo',\
'industrial','synthpop','idm','idm - intelligent dance music','8-bit','ambient',
'dance and electronica','electronic']

# relevant metadata for all EDM songs found in the MSD 
all_song_data = {}
pitch_segs_data = []
count = 0
start_time = time.time()

''' preprocessing before actually running the dirichlet process takes much more time 
than running the dirichlet process on data '''

for root, dirs, files in os.walk(basedir):
    files = glob.glob(os.path.join(root,'*'+ext))
    for f in files:
        h5 = hdf5_getters.open_h5_file_read(f)
        # if year unknown, throw out sample
        if hdf5_getters.get_year(h5) == 0: 
            h5.close()
            continue
        if any(tag in str(hdf5_getters.get_artist_mbtags(h5)) for tag in target_genres): 
            print 'found electronic music song at {0} seconds'.format(time.time()-start_time)
            count += 1  
            chord_changes = [0 for i in range(0,192)]
            segments_pitches_old = hdf5_getters.get_segments_pitches(h5)
            segments_pitches_old_smoothed = []
            smoothing_factor = max(3,round(len(segments_pitches_old) * 60.0 / (hdf5_getters.get_tempo(h5) * hdf5_getters.get_duration(h5))))
            for i in range(0,int(math.floor(len(segments_pitches_old))/smoothing_factor)):
                segments = segments_pitches_old[(smoothing_factor*i):(smoothing_factor*i+smoothing_factor)]
                # calculate mean frequency of each note over a block of 5 time segments
                segments_mean = map(mean, zip(*segments))
                segments_pitches_old_smoothed.append(segments_mean)
            most_likely_chords = [msd_utils.find_most_likely_chord(seg) for seg in segments_pitches_old_smoothed]
            print 'found most likely chords at {0} seconds'.format(time.time()-start_time)
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
                # print ('chord shift: {0}'.format(chord_shift))
            pitch_segs_data.append(chord_changes)
            '''Now smooth out the timbre segments based on BPM'''
            segments_timbre_old = hdf5_getters.get_segments_timbre(h5)
            segments_timbre_smoothed = []
            for i in range(0,int(math.floor(len(timbre_pitches_old))/smoothing_factor)):
                segments = segments_timbre_old[(smoothing_factor*i):(smoothing_factor*(i+1))]
                # calculate mean frequency of each note over a block of 5 time segments
                segments_mean = map(mean, zip(*segments))
                segments_timbre_smoothed.append(segments_mean)
            print ('song count: {0}'.format(count+1))
            h5_subdict = dict()
            h5_subdict['title'] = hdf5_getters.get_title(h5)
            h5_subdict['artist_name'] = hdf5_getters.get_artist_name(h5)
            h5_subdict['year'] = hdf5_getters.get_year(h5)
            h5_subdict['chord_changes'] = chord_changes
            h5_subdict['duration'] = hdf5_getters.get_duration(h5)
            h5_subdict['timbre'] = segments_timbre_smoothed
            track_id = hdf5_getters.get_track_id(h5)
            all_song_data[track_id] = h5_subdict
            print('Song {0} finished processing. Total time elapsed: {1} seconds'.format(count,str(time.time() - start_time)))
        h5.close() 

all_song_data_sorted = dict(sorted(all_song_data.items(), key=lambda k: k[1]['year'])) 
sortedpitchdata = 'output/msd_EDM_sortedpitchdata_' + re.sub('/','',sys.argv[1]) + '.txt'
with open(sortedpitchdata, 'w') as text_file:
    text_file.write(str(all_song_data_sorted))
