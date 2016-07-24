import json
import ast
import re
import time

'''quicksorter.py'''

infile = './output/msd_EDM_sortedpitchdata_EVERYTHING.txt'
outfile = './output/msd_EDM_sortedpitchdata_EVERYTHING_SORTED.txt'
all_song_data = dict()

print 'reading all data and appending to a data structure at time {0}'.format(time.time())
json_contents = open(infile,'r').read()
for json_object_str in re.finditer('\'(TR.*?)\':(.*?})',json_contents):
    # print 'track: {0}'.format(json_object_str.group(1))
    # print 'json object: {0}'.format(json_object_str.group(2))
    json_object = ast.literal_eval(json_object_str.group(2).strip())
    track = str(json_object_str.group(1))
    all_song_data[track] = json_object
print 'beginning sorting of song data at time {0}'.format(time.time())
all_song_data_sorted = sorted(all_song_data.items(), key=lambda k: k[1]['year'])
with open(outfile, 'w') as f:
    f.write(str(all_song_data_sorted))
print 'sorting finished at time {0}'.format(time.time())
# then feed it all into the dirichlet process
