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

#basedir = '/Volumes/Seagate Backup Plus Drive/msd_data_full'
basedir = './../../scratch/network/mssilver/mssilver/msd_data_full/data/' + str(sys.argv[1]) 
# basedir = '~/data' #for Adroit, for example
ext = '.h5'

#json_flat_file_metadata_name = '/Users/matthewsilver/Documents/MATLAB/msd_song_metadata.txt'
# debug_file = 'dirichlet_debug.txt' #debug intermediate steps
# json_flat_file_name = 'lastfm_subset_flatfile.txt'
# json_edm_pitch_data_sorted_file = 'msd_EDM_sortedpitchdata.txt'
# json_contents = (open(json_flat_file_name,'r')).read()

target_genres = ['house','techno','drum and bass','drum n bass','drum\'n\'bass',\
'drumnbass','drum \'n\' bass','jungle','breakbeat','trance','dubstep','trap','downtempo','disco',\
'industrial','synthpop','idm','idm - intelligent dance music','8-bit','hip-hop','hip hop','ambient',
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
        # print 'tags are {0}'.format(tags)
        if any(tag in str(hdf5_getters.get_artist_mbtags(h5)) for tag in target_genres): 
            print 'found electronic music song at {0} seconds'.format(time.time()-start_time)
            count += 1  
            chord_changes = [0 for i in range(0,192)]
            ''' transpose the pitches so they all match with C major/minor '''  
            #key = hdf5_getters.get_key(h5)
            #confidence = hdf5_getters.get_key_confidence(h5)
            segments_pitches_old = hdf5_getters.get_segments_pitches(h5)
            # segments_pitches_new = msd_utils.normalize_pitches(h5)
            segments_pitches_old_smoothed = []
            # based on time signature and BPM, estimate length of measure and use that
            # as unit of time to smooth pitches upon
            smoothing_factor = max(3,round(len(segments_pitches_old) * 60.0 / (hdf5_getters.get_tempo(h5) * hdf5_getters.get_duration(h5))))
            for i in range(0,int(math.floor(len(segments_pitches_old))/smoothing_factor)):
                segments = segments_pitches_old[(smoothing_factor*i):(smoothing_factor*i+smoothing_factor)]
                # calculate mean frequency of each note over a block of 5 time segments
                segments_mean = map(mean, zip(*segments))
                segments_pitches_old_smoothed.append(segments_mean)
            # for idx,seg in enumerate(segments_pitches_old_smoothed):
            #     chord = msd_utils.find_most_likely_chord(seg)
            #     most_likely_chords.append(chord)
            most_likely_chords = [msd_utils.find_most_likely_chord(seg) for seg in segments_pitches_old_smoothed]
            print 'found most likely chords at {0} seconds'.format(time.time()-start_time)
                # print('most likely chord: {0}'.format(chord))
            #smooth out most likely chords by taking the most common 
            # most_likely_chords_smoothed = []
            # for i in range(0,int(math.floor(len(segments_pitches_old))/5)):
            #   chords = most_likely_chords[(5*i):(5*i+5)]
            #   lst1 = [x[0] for x in chords]
            #   lst2 = [x[1] for x in chords]
            #   chord_type = max(set(lst1), key=lst1.count)
            #   key = max(set(lst2), key=lst2.count)
            #   most_likely_chords.append((chord_type,key))
                # print('smoothed results: {0}'.format((chord_type,key)))
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
            print ('song count: {0}'.format(count+1))
            # best_tag = ''
            # for t in [tag[0].lower() for tag in json_object[track_id]]:
            #     if t in target_genres:
            #         best_tag = t
            # if best_tag == '':
            #     best_tag = 'other'  
            h5_subdict = dict()
            h5_subdict['title'] = hdf5_getters.get_title(h5)
            h5_subdict['artist_name'] = hdf5_getters.get_artist_name(h5)
            h5_subdict['year'] = hdf5_getters.get_year(h5)
            h5_subdict['chord_changes'] = chord_changes
            # h5_subdict['best_tag'] = best_tag
            h5_subdict['duration'] = hdf5_getters.get_duration(h5)
            track_id = hdf5_getters.get_track_id(h5)
            all_song_data[track_id] = h5_subdict
            print('Song {0} finished processing. Total time elapsed: {1} seconds'.format(count,str(time.time() - start_time)))
        h5.close() 

all_song_data_sorted = dict(sorted(all_song_data.items(), key=lambda k: k[1]['year'])) 
sortedpitchdata = 'output/msd_EDM_sortedpitchdata_' + re.sub('/','',sys.argv[1]) + '.txt'
with open(sortedpitchdata, 'w') as text_file:
    text_file.write(str(all_song_data_sorted))

# print(pitch_segs_data)
# m = sklearn.mixture.DPGMM(n_components=2, n_iter=10000, alpha=.005)
# pitch_segs_data = [value['chord_changes'] for key, value in all_song_data_sorted.iteritems()]
# fit = m.fit_predict(pitch_segs_data)
# fit_filename = 'output/msd_fit_categories_' + re.sub('/','',sys.argv[1]) + '.txt'
# freq_filename = 'output/msd_frequency_counts_' + re.sub('/','',sys.argv[1]) + '.txt'
# with open(fit_filename,'w') as text_file:
#     text_file.write(str(fit))
# counter=collections.Counter(fit)
#with open(freq_filename,'w') as text_file:
#    text_file.write(str(counter.values()))
