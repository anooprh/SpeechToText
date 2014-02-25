import scipy as sp
import scipy
import numpy as np
from record_speech import record_to_file
from mfcc_features import MelFeatures
from dtw_Node import DTW_Node

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

template_features = []
FILE_NAME = 'test_speak.wav'
print("please speak a word into the microphone")
record_to_file(FILE_NAME)
print("done - result written to " + FILE_NAME)

print "Calculating MEL features..."
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features = MelFeat.calcMelFeatures(raw_data)
mfcc_features = np.hstack((np.zeros((39, 1)), mfcc_features))

for file in wavfiles:
    template_features.append(scipy.io.loadmat(file + '.mat').get('data'))

dtw_nodes = []


def get_predecessor_nodes(i, k):
    predecessor_nodes = []
    if i == 0:
        return predecessor_nodes
    predecessor_nodes.append(dtw_nodes[i - 1][k])
    if k == 0:
        return predecessor_nodes
    predecessor_nodes.append(dtw_nodes[i - 1][k - 1])
    if k == 1:
        return predecessor_nodes
    predecessor_nodes.append(dtw_nodes[i - 1][k - 2])
    pass


for i in range(0, mfcc_features.shape[1]):
    dtw_nodes.append([])

    for k in range(0, template_features[0].shape[1] + 1):
        template_features[0] = np.hstack((np.zeros((39, 1)), template_features[0]))
        node = DTW_Node()
        node.time = i
        node.templateIndex = k

        if (i == 0):
            node.cost = k
            dtw_nodes[i].append(node)
            break
        if (k == 0):
            node.cost = i
            dtw_nodes[i].append(node)
            break

        distance = sp.spatial.distance.euclidean(mfcc_features[:, i], template_features[0][:, k])

        predecessor_node_list = get_predecessor_nodes(i, k)

        if len(predecessor_node_list) == 0:
            prev_cost = 0
        if len(predecessor_node_list) == 1:
            prev_cost = predecessor_node_list[0].cost
        if len(predecessor_node_list) == 2:
            min(predecessor_node_list[0].cost, predecessor_node_list[1].cost)
        if len(predecessor_node_list) > 2:
            prev_cost = min(predecessor_node_list[0].cost, predecessor_node_list[1].cost, predecessor_node_list[2].cost)
        node.cost = prev_cost + distance

        dtw_nodes[i].append(node)


# for i in range(0, mfcc_features.shape[1]):
#     dtw_nodes.append([])
#     for j in range(0, len(template_features)):
#         for k in range(0, template_features[j].shape[1]):
#             dtw_nodes[i].append(DTW_Node())
#             # print 'i --> ' + str(i)
#             # print 'j --> ' + str(j)
#             # print 'k --> ' + str(k)
#             # print 'j+k --> ' + str(j+k)

pass