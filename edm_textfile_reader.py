import json
import re
import ast
import numpy as np
import matplotlib.pyplot as plt
import operator

''' Read dirichlet-clustering results from a text file and pair up songs and categories '''

edm_textfile = './output/msd_EDM_sortedpitchdata_EVERYTHING_SORTED.txt'
edm_classifications_textfile = './output/msd_EDM_classifications.txt'
edm_classifications = [int(x) for x in open(edm_classifications_textfile,'r').read().split()]
classifications_artistsong = [[] for i in range(0,20)]
classification_arrays = [[] for i in range(0,20)]
json_contents = open(edm_textfile,'r').read()
count = 0
for json_object_str in re.finditer('{.*?}',json_contents):
    print json_object_str.group(0)
    json_object = ast.literal_eval(json_object_str.group(0))
    classification = edm_classifications[count]
    classification_arrays[classification].append((json_object['chord_changes'],json_object['duration']))
    classifications_artistsong[classification].append((json_object['artist_name'],json_object['title']))
    count += 1

for g in range(0,len(classifications_artistsong)):
    print ('Group {0}:\n{1}'.format(g, classifications_artistsong[g]))

count = 0
classification_arrays_averages = []
for i in range(0,len(classification_arrays)):
    if len(classification_arrays[i]) == 0:
        continue
    avg_array = [0 for x in range(192)]
    for j in range(0,192):
        change_total = 0
        for k in range(0,len(classification_arrays[i])):
            # normalize array by duration of song
            change_total += classification_arrays[i][k][0][j]/(1.0*float(classification_arrays[i][k][1]))
        change_avg = 1.0 * change_total / len(classification_arrays[i])
        avg_array[j] = change_avg
    count += len(classification_arrays[i])
    classification_arrays_averages.append(avg_array)

for idx, c in enumerate(classification_arrays_averages):
    most_common_chordchanges = sorted(range(len(c)), key=lambda k: c[k], reverse=True)
    mcc_short = most_common_chordchanges[:5]
    print 'Group {0} most common changes and frequencies: {1}\n{2}'.format(idx,mcc_short,[c[i] for i in mcc_short])
    plt.subplot(5,5,idx)
    plt.plot(c)
    plt.title('Group {}'.format(idx), y=1.08)
    plt.tight_layout()

plt.show()





    


