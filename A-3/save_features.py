import scipy.io as sio
from mfcc_features import MelFeatures

wavfiles = ['zero_template', 'one_template', 'two_template', 'three_template', 'four_template','five_template', 'six_template', 'seven_template', 'eight_template', 'nine_template']

for file in wavfiles:
    fileName = file + '.wav'
    print "Calculating MEL features..."
    MelFeat = MelFeatures()
    raw_data = MelFeat.loadWAVfile(fileName)
    mfcc_features   = MelFeat.calcMelFeatures(raw_data)
    sio.savemat(file, {'data': mfcc_features})

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
for file in wavfiles:
    for i in range(1,6):
        fileName = file + '_%d'%i + '.wav'
        print "Calculating MEL features..."
        MelFeat = MelFeatures()
        raw_data = MelFeat.loadWAVfile(fileName)
        mfcc_features   = MelFeat.calcMelFeatures(raw_data)
        sio.savemat(file+ '_%d'%i, {'data': mfcc_features})