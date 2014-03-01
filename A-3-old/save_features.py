import scipy.io as sio
from mfcc_features import MelFeatures
wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

for file in wavfiles:
    fileName = file + '.wav'
    print "Calculating MEL features..."
    MelFeat = MelFeatures()
    raw_data = MelFeat.loadWAVfile(fileName)
    mfcc_features   = MelFeat.calcMelFeatures(raw_data)
    sio.savemat(file, {'data': mfcc_features})

