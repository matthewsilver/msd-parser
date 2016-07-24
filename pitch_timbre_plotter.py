import json
import re
import ast
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import operator
import time
import collections 

''' Read dirichlet-clustering results from a text file and pair up songs and categories '''

# prevents output from showing ellipses when printed
np.set_printoptions(threshold=np.nan)

basedir = '../../../scratch/network/mssilver/mssilver/'
datafile = basedir + 'msd_datapreprocessed_EVERYTHINGSORTED.txt'
clusterfile = './output/msd_fit_categories0.05.txt'

time_start = time.time()

metadata = open(datafile).read()
# json_contents = ast.literal_eval(metadata)
print 'finished converting everything to dictionary objects at time {0}'.format(time.time()-time_start)
clusters = [int(x) for x in open(clusterfile).read()[1:-1].split()]
cluster_dict = collections.OrderedDict(collections.Counter(clusters))

chordchange_total = [[0 for j in range(0,192)] for i in range(0,50)]
timbre_total = [[0 for j in range(0,46)] for i in range(0,50)]
count = 0
all_titles = []
blacklist_artists = ['melanie','japan','the emotions','spark','yes','bonnie tyler','electric light orchestra','melanie safka','sparks','ben watt','nelson riddle','Nelson Riddle;Yves Montand;Barbra Streisand','donna summer','daniel johnston','jackson sisters']
for json_object_str in re.finditer('{.*?}',metadata):
    json_object = ast.literal_eval(json_object_str.group(0))
    s = json_object['artist_name']+json_object['title']
    if not json_object['artist_name'].lower() in blacklist_artists and int(json_object['year']) >= 1970 and not s in all_titles:
        cluster = clusters[count]
        chord_changes = json_object['chord_changes']
        timbre_cats = json_object['timbre_cat_counts']
        for i in range(0,46):
            timbre_total[cluster][i] = timbre_total[cluster][i] + timbre_cats[i]       
        for i in range(0,192):
            chordchange_total[cluster][i] = chordchange_total[cluster][i] + chord_changes[i]
        all_titles.append(json_object['artist_name']+json_object['title'])
        count += 1

chordchange_averages = [[0 for j in range(0,192)] for i in range(0,50)]
timbre_averages = [[0 for j in range(0,46)] for i in range(0,50)]

for key in cluster_dict:
    for i in range(0,46):
        timbre_averages[key][i] = timbre_total[key][i]/float(cluster_dict[key])      
    for i in range(0,192):
        chordchange_averages[key][i] = chordchange_total[key][i]/float(cluster_dict[key])  


''''''

for idx, (seg1,seg2) in enumerate(zip(chordchange_averages,timbre_averages)):
    if sum(seg1) > 0.0:
        # plt.subplot(5,5,idx)
        plt.plot(np.array(seg1))
        plt.plot(np.array(seg2))
        plt.title('Cluster {}'.format(idx))
        count += 1
        plt.savefig('output/timbre_averages' + str(idx) + '_0.05.png',dpi=400)
        plt.close()






    


