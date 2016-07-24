'''timbre_dirichlet.py'''

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

m = sklearn.mixture.GMM(n_components=46, n_iter=10000)
fit = m.fit_predict(timbre_data)
m.means_