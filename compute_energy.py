import wave
import numpy as np

FRAME_LENGTH_IN_MS = 20

WAVE_OUTPUT_FILENAME = "output.wav"
RATE = 16000
i = 0
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
FRAME_LENGTH_IN_BYTES = (RATE/1000 )* FRAME_LENGTH_IN_MS
while(1):
    x = wf.readframes(FRAME_LENGTH_IN_BYTES)
    i=i+1
    if i <= 1:
        continue
    values = np.fromstring(x, 'Int16')
    # if not x:
    #     break
    for index in range(len(values)):
        values[index] = values[index] * values[index];
    # print(i)
    # print(x)
    avg_energy_in_frame = np.sum(values)/len(values)
    print i , avg_energy_in_frame
wf.close()
