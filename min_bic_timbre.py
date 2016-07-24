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
from string import ascii_uppercase
import ast
import matplotlib.pyplot as plt
import operator
from collections import defaultdict
import random

timbre_data = []
# f = './../../scratch/network/mssilver/mssilver/timbre_frames_all.txt'
f = 'timbre_frames_all.txt'
with open(f,'r') as t:
	timbre_data = json.loads(list(t)[0])

powers = xrange(0,21)
alphas = [0.001*pow(2,i) for i in powers]
components = xrange(10,100)
bic_vals = [[0 for col in xrange(0,len(components))] for row in range(0,len(alphas))]
min_b = float("inf")
min_a = 0
min_c = 0
bic_vals = [0 for i in xrange(0,len(components))]

for c in components:
	m = sklearn.mixture.GMM(n_components=c, n_iter=10000)
	fit = m.fit_predict(timbre_data)
	b = m.bic(np.array(timbre_data))
	print 'bic for components={0}: {1}'.format(c,b)
	bic_vals[c] = b
	if b < min_b:
		min_b = b
		min_c = c
		print 'new min values: c={0}: b={1}'.format(str(c),str(b))

print 'overall min values: c={0}: b={1}'.format(str(min_c),str(min_b))



