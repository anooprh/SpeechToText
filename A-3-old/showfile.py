import numpy as np
import wave
import sys

import matplotlib.pyplot as plt


FILE_NAME = 'anoop_speak.wav'
# FILE_NAME = sys.argv[1]

spf = wave.open(FILE_NAME,'r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

#If Stereo
if spf.getnchannels() == 2:
    print ('Just mono files')
    sys.exit(0)


Time=np.linspace(0, len(signal)/float(fs), num=len(signal))

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(Time,signal)
plt.show()
