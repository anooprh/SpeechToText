#Step 1, Initialization
import pocketsphinx as ps

decoder = ps.Decoder(jsgf='/path/to/your/jsgf/grammar.jsgf',samprate='8000')
# Step 2, open the audio file.
fh = open('myrecording.wav', 'rb')
nsamp = decoder.decode_raw(fh)
# Step 3, get the result
hyp, uttid, score = decoder.get_hyp()
print 'Got result %s %d' % (hyp, score)