import sys
import math
from record_speech import record_to_file
from mfcc_features import MelFeatures
import numpy as np
import scipy
__author__ = 'anoop'

# FILE_NAME = sys.argv[1]
FILE_NAME = 'nine.wav'

NUMBER_OF_SEGMENTS = 3
NUMBER_OF_TRIALS = 1

def distance_between_vectors(vector1, vector2):
    return scipy.spatial.distance.euclidean(vector1, vector2)

template_vector0 = np.array([])
template_vector1 = np.array([])
template_vector2 = np.array([])

print("please speak a word into the microphone")
record_to_file(FILE_NAME)
print("done - result written to " + FILE_NAME)

print "Calculating MEL features..."
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features   = MelFeat.calcMelFeatures(raw_data)

# mfcc_features_transpose = mfcc_features.transpose()
#
# (num_samples, num_features) = mfcc_features_transpose.shape
#
# num_vectors_in_segment = num_samples / NUMBER_OF_SEGMENTS
#
#
# to_remove = num_samples % NUMBER_OF_SEGMENTS
# mfcc_features_transpose = mfcc_features_transpose[0:-to_remove][:]
#
# signal_segments = np.split(mfcc_features_transpose, NUMBER_OF_SEGMENTS)
# template_vector0 = np.append(template_vector0, signal_segments[0])
# template_vector1 = np.append(template_vector1, signal_segments[1])
# template_vector2 = np.append(template_vector2, signal_segments[2])

