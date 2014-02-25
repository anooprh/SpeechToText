import scipy.io as sio
from record_speech import record_to_file
from mfcc_features import MelFeatures

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


template_features = []
FILE_NAME = 'test_speak.wav'
print("please speak a word into the microphone")
record_to_file(FILE_NAME)
print("done - result written to " + FILE_NAME)

print "Calculating MEL features..."
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features   = MelFeat.calcMelFeatures(raw_data)

for file in wavfiles:
    template_features.append(sio.loadmat(file+'.mat').get('data'))

pass