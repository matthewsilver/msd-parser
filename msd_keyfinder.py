import os
import re
import json
import glob
import hdf5_getters
import time
import msd_utils

'''This code finds the key of each electronic song and the associated confidence with it'''

#basedir = '/Volumes/Seagate Backup Plus Drive/msd_data_full'
basedir = '/Users/matthewsilver/Documents/MATLAB/MillionSongSubset'
ext = '.h5'

json_flat_file_metadata_name = '/Users/matthewsilver/Documents/MATLAB/msd_song_metadata.txt'
json_flat_file_name = '/Users/matthewsilver/Documents/MATLAB/lastfm_subset_flatfile.txt'
json_contents = (open(json_flat_file_name,'r')).read()

for root, dirs, files in os.walk(basedir):
	files = glob.glob(os.path.join(root,'*'+ext))
	for f in files:

		h5 = hdf5_getters.open_h5_file_read(f)
		track_id = hdf5_getters.get_track_id(h5)
		if track_id in json_contents:

			json_object = re.search('{\"%s\".*?}' % track_id,json_contents).group(0)
			json_object = json.loads(json_object)
			if 'electronic' in [t[0].lower() for t in json_object[track_id]]:		
				key = hdf5_getters.get_key(h5)
				confidence = hdf5_getters.get_key_confidence(h5)
				segments_pitches_old = hdf5_getters.get_segments_pitches(h5)
				segments_pitches_old = segments_pitches_old[:1]
				segments_pitches_new = msd_utils.normalize_pitches(h5)
				segments_pitches_new = segments_pitches_new[:1]

		h5.close() 
