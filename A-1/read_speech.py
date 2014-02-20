from math import log10
import pyaudio
import wave
import numpy as np

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

MAX_RECORD_SECONDS = 20
THRESHOLD_DB  = 80
WAVE_OUTPUT_FILENAME = "output.wav"

def energy(samples):
    return 10*log10(np.sum([sample ** 2 for sample in samples]))

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
energy_signal = []
started_speaking = False;

for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
    if i < 100:
        continue
    data = stream.read(CHUNK)
    signal_chunk = np.fromstring(data, 'Int16')
    energy_in_chunk = energy(signal_chunk)
    if started_speaking==True and (energy_in_chunk < THRESHOLD_DB):
        break
    if energy_in_chunk > THRESHOLD_DB:
        started_speaking = True
    print i , energy_in_chunk
    frames.append(data)

print("* done recording")

stream.stop_stream()
p.close(stream)
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
