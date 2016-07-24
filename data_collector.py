from __future__ import division
import os
import sys
import time
import glob 
import hdf5_getters #not on adroit

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

'''This code computes the frequency of chord changes in each electronic song and runs the dirichlet process on it '''

basedir = './../../scratch/network/mssilver/mssilver/msd_data_full/data/' + str(sys.argv[1]) 
ext = '.h5'

target_genres = ['house','techno','drum and bass','drum n bass','drum\'n\'bass',\
'drumnbass','drum \'n\' bass','jungle','breakbeat','trance','dubstep','trap','downtempo',\
'industrial','synthpop','idm','idm - intelligent dance music','8-bit','ambient',
'dance and electronica','electronic']

# relevant metadata for all EM songs found in the MSD 
all_song_data = {}
pitch_segs_data = []
count = 0
start_time = time.time()

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
            print ('song count: {0}'.format(count+1))
            h5_subdict = dict()
            h5_subdict['title'] = hdf5_getters.get_title(h5).item()
            h5_subdict['artist_name'] = hdf5_getters.get_artist_name(h5).item()
            h5_subdict['year'] = hdf5_getters.get_year(h5).item()
            h5_subdict['duration'] = hdf5_getters.get_duration(h5).item()
            h5_subdict['timbre'] = hdf5_getters.get_segments_timbre(h5).tolist()
            h5_subdict['pitches'] = hdf5_getters.get_segments_pitches(h5).tolist()
            track_id = hdf5_getters.get_track_id(h5).item()
            all_song_data[track_id] = h5_subdict
            print('Song {0} finished processing. Total time elapsed: {1} seconds'.format(count,str(time.time() - start_time)))
        h5.close() 

all_song_data_sorted = dict(sorted(all_song_data.items(), key=lambda k: k[1]['year'])) 
sortedpitchdata = './../../scratch/network/mssilver/mssilver/msd_dataraw_' + re.sub('/','',sys.argv[1]) + '.txt'
with open(sortedpitchdata, 'w') as text_file:
    text_file.write(str(all_song_data_sorted))
