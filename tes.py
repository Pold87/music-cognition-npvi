# Permutate notes -> 'destroys melody''

import music21
import numpy as np

sBach = music21.corpus.parse('schumann/dichterliebe_no2.xml')
s1 = sBach.parts[0].flat.notesAndRests

print("Original nPVI")
print(music21.analysis.patel.nPVI(s1))

notes = np.array([note for note in s1 if note.isNote or note.isRest])

while True:
    new_notes = np.random.permutation(notes)
    stream_new_nPVI = music21.stream.Stream()
    for n in new_notes:
        stream_new_nPVI.append(n)

    print("Modified nPVI")
    new_nPVI = music21.analysis.patel.nPVI(stream_new_nPVI)
    print(new_nPVI)
    if new_nPVI > 65:
        break

print("Found nPVI: ")
print(new_nPVI)
stream_new_nPVI.show()
