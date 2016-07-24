# Playing around with Million Song Dataset

'''
import sys
sys.path.insert(0, './PythonSrc')
import hdf5_getters
h5 = hdf5_getters.open_h5_file_read('.')
duration = hdf5_getters.get_duration(h5)
h5.close()
'''

import os
import re
import json
import glob
import hdf5_getters
import time

''' Code to dump contents from each directory into a single flat file'''
# electronic_count = 0
#
# rootdir = '/Users/matthewsilver/Documents/MATLAB/lastfm_train/'
# with open('/Users/matthewsilver/Documents/MATLAB/lastfm_train_flatfile.txt','w') as outfile:
# 	for root, subFolders, files in os.walk(rootdir):
# 			for filename in files:
# 				if '.json' in filename:
# 					json_data = json.loads(open(root + '/' + filename, 'r').read()) 
# 					if 'electronic' in (tag[0].lower() for tag in json_data['tags']):
# 						electronic_count += 1
# 						print electronic_count
# 						json.dump(json_data,outfile)

# electronic_count = 0

# rootdir = '/Users/matthewsilver/Documents/MATLAB/lastfm_subset/'
# with open('/Users/matthewsilver/Documents/MATLAB/lastfm_subset_flatfile.txt','w') as outfile:
# 	for root, subFolders, files in os.walk(rootdir):
# 			for filename in files:
# 				if '.json' in filename:
# 					json_data = json.loads(open(root + '/' + filename, 'r').read()) 
# 					if 'electronic' in (tag[0].lower() for tag in json_data['tags']):
# 						electronic_count += 1
# 						print electronic_count
# 						d = dict()
# 						d[json_data['track_id']] = json_data['tags']
# 						json.dump(d,outfile)

''' Code to read flat JSON file and parse contents '''
# tags = set()
# target_genres = ['house','techno','drum and bass','drum n bass','drum\'n\'bass',\
# 'drumnbass','drum \'n\' bass','jungle','breakbeat','trance','dubstep','trap','downtempo','disco',\
# 'industrial','synthpop','idm','idm - intelligent dance music']

# json_flat_file_name = '/Users/matthewsilver/Documents/MATLAB/lastfm_train_flatfile.txt'
# track_ids = []
# artists = []
# json_contents = open(json_flat_file_name,'r')
# json_contents = json_contents.read()
# json_objects = re.findall('{.*?}',json_contents)
# for obj in json_objects:
# 	json_obj = json.loads(obj)
# 	for tag in json_obj['tags']:
# 		if any(x in tag for x in target_genres):
# 			track_ids.append(json_obj['track_id'])
# 			artists.append(json_obj['artist'])

# track_ids = set(track_ids)
# artists = sorted(set(artists))

# for a in artists: print a

# print len(tags)


''' Code to merge desired MSD metadata with last.fm song tags '''
# json_flat_file_name = '/Users/matthewsilver/Documents/MATLAB/lastfm_train_flatfile.txt'
# track_ids = []
# artists = []
# json_contents = open(json_flat_file_name,'r')
# json_contents = json_contents.read()

# json_objects = re.findall('{.*?}',json_contents)
# for obj in json_objects:
# 	json_obj = json.loads(obj)
# 	for tag in json_obj['tags']:
# 		if any(x in tag for x in target_genres):
# 			track_ids.append(json_obj['track_id'])
# 			artists.append(json_obj['artist'])


target_genres = ['house','techno','drum and bass','drum n bass','drum\'n\'bass',\
'drumnbass','drum \'n\' bass','jungle','breakbeat','trance','dubstep','trap','downtempo','disco',\
'industrial','synthpop','idm','idm - intelligent dance music','8-bit','hip-hop','hip hop','ambient','pop']

json_flat_file_metadata_name = '/Users/matthewsilver/Documents/MATLAB/msd_song_metadata.txt'
json_flat_file_name = '/Users/matthewsilver/Documents/MATLAB/lastfm_subset_flatfile.txt'
json_contents = (open(json_flat_file_name,'r')).read()

start_time = time.time()
song_count = 0
song_dict = dict()
basedir = '/Users/matthewsilver/Documents/MATLAB/MillionSongSubset/data/'
for root, dirs, files in os.walk(basedir):
	for f in files:
		if f[-3:] == '.h5':
			h5 = hdf5_getters.open_h5_file_read(root + '/' + f)
			track_id = hdf5_getters.get_track_id(h5)
			track_id_name = '\"track_id\": \"{0}\"'.format(track_id)
			if track_id in json_contents:
				song_count += 1
				print 'song {0}: {1}'.format(str(song_count),f)

				# stupidly hacky way to get a json object from a regex search 
				# but I haven't figured out how to do it quicker 
				json_object = re.search('{\"%s\".*?}' % track_id,json_contents).group(0)
				json_object = json.loads(json_object)

				best_tag = ''
				for t in [tag[0].lower() for tag in json_object[track_id]]:
					if t in target_genres:
						best_tag = t

				if best_tag == '':
					best_tag = 'other'	

				# print best_tag

				h5_dict = dict()
				h5_dict['title'] = hdf5_getters.get_title(h5)
				h5_dict['artist_name'] = hdf5_getters.get_artist_name(h5)
				h5_dict['year'] = hdf5_getters.get_year(h5)
				h5_dict['beats_confidence'] = hdf5_getters.get_beats_confidence(h5)
				h5_dict['beats_start'] = hdf5_getters.get_beats_start(h5)
				h5_dict['tempo'] = hdf5_getters.get_tempo(h5)
				h5_dict['time_signature'] = hdf5_getters.get_time_signature(h5)
				h5_dict['segments_timbre'] = hdf5_getters.get_segments_timbre(h5)
				h5_dict['segments_loudness_max'] = hdf5_getters.get_segments_loudness_max(h5)
				h5_dict['segments_loudness_max_time'] = hdf5_getters.get_segments_loudness_max_time(h5)
				h5_dict['segments_loudness_start'] = hdf5_getters.get_segments_loudness_start(h5)
				h5_dict['best_tag'] = best_tag

				song_dict[track_id] = h5_dict
			
			h5.close() 

with open(json_flat_file_metadata_name, 'w') as text_file:
    text_file.write('{}'.format(song_dict))

print 'Time elapsed: {0} seconds'.format(str(time.time() - start_time)) 



