# Permutate notes -> 'destroys melody''

import music21
import numpy as np



sBach = music21.corpus.parse('schumann/dichterliebe_no2.xml')
s1 = sBach.parts[0]

allTimeSignatures = music21.meter.bestTimeSignature(
    s1.flat.getElementsByClass(music21.stream.Measure)[0])
print(allTimeSignatures)
