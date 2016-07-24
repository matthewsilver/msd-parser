import json
import re
import ast
import numpy as np
import matplotlib.pyplot as plt
import operator
import collections

json_contents = open('output/msd_fit_categories0.2.txt','r').read()[1:-1]
json_contents_split = [int(a) for a in json_contents.split()]
cluster_sizes = sorted(collections.Counter(json_contents_split).items())

cluster_years = collections.defaultdict(list)
json_contents = open('output/song_groupings0.2.txt','r').read()
for g in re.finditer('(\d{1,2}): \[.*?(\)\])',json_contents):
    cluster_num = g.group(1)
    for year in re.finditer(', (\d{4})\),',g.group(0)):
        cluster_years[cluster_num].append(int(year.group(1)))

all_song_dists = {}
all_song_nums = {}
for key in cluster_years.keys():
    song_dist = cluster_years[key]
    all_songs_dists_raw = sorted(collections.Counter(song_dist).items())
    total_songs_num = sum([tup[1] for tup in all_songs_dists_raw])
    all_song_nums[key] = total_songs_num
    all_song_dists[key] = [(tup[0],float(tup[1])/total_songs_num) for tup in all_songs_dists_raw]

plt.switch_backend('agg')
for idx, key in enumerate(cluster_years):
    plt.xlim([1970,2010])
    plt.hist(cluster_years[key])
    plt.title('Group {}'.format(key))
    plt.savefig('output/songdist_group' + str(key) + '_0.2.png')
    plt.close()
