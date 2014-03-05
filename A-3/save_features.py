import scipy.io as sio
import sys
from mfcc_features import MelFeatures

file_name = sys.argv[1]
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(file_name + '.wav')
mfcc_features = MelFeat.calcMelFeatures(raw_data)
sio.savemat(file_name, {'data': mfcc_features})


wavfiles_templates = [
    ['zero_template', 'zero_template_1', 'zero_template_2', 'zero_template_3', 'zero_template_4'],
    ['one_template', 'one_template_1', 'one_template_2', 'one_template_3', 'one_template_4'],
    ['two_template', 'two_template_1', 'two_template_2', 'two_template_3', 'two_template_4' ],
    ['three_template', 'three_template_1', 'three_template_2', 'three_template_3', 'three_template_4'],
    ['four_template', 'four_template_1', 'four_template_2', 'four_template_3', 'four_template_4'],
    ['five_template', 'five_template_1', 'five_template_2', 'five_template_3', 'five_template_4'],
    ['six_template', 'six_template_1', 'six_template_2', 'six_template_3', 'six_template_4'],
    ['seven_template', 'seven_template_1', 'seven_template_2', 'seven_template_3', 'seven_template_4'],
    ['eight_template', 'eight_template_1', 'eight_template_2', 'eight_template_3', 'eight_template_4'],
    ['nine_template', 'nine_template_1', 'nine_template_2', 'nine_template_3', 'nine_template_4'],
]
for file_list in wavfiles_templates:
    for file in file_list:
        fileName = file + '.wav'
        print "Calculating MEL features..."
        MelFeat = MelFeatures()
        raw_data = MelFeat.loadWAVfile(fileName)
        print(fileName)
        mfcc_features = MelFeat.calcMelFeatures(raw_data)
        sio.savemat(file, {'data': mfcc_features})

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
for file in wavfiles:
    for i in range(1, 6):
        fileName = file + '_%d' % i + '.wav'
        print "Calculating MEL features..."
        MelFeat = MelFeatures()
        raw_data = MelFeat.loadWAVfile(fileName)
        mfcc_features = MelFeat.calcMelFeatures(raw_data)
        sio.savemat(file + '_%d' % i, {'data': mfcc_features})