# Permutate notes -> 'destroys melody''

import music21
import numpy as np

sBach = music21.corpus.parse('schumann/dichterliebe_no2.xml')
s1 = sBach.parts[0].flat.notesAndRests

print(sBach.show("text"))

print("Original nPVI")
print(music21.analysis.patel.nPVI(s1))

notes = np.array([note for note in s1 if note.isNote or note.isRest])
notes_durations = np.array([note.quarterLength
                            for note in s1
                            if note.isNote or note.isRest])

while True:
    new_notes_duration = np.sort(notes_durations)

    stream_new_nPVI = music21.stream.Stream()
    for n, d in zip(notes, new_notes_duration):
        new_n = music21.note.Note('C4')
        new_n.quarterLength = d
        stream_new_nPVI.append(new_n)

    print("Modified nPVI")
    new_nPVI = music21.analysis.patel.nPVI(stream_new_nPVI)
    print(new_nPVI)
    break

print("Found nPVI: ")
print(new_nPVI)

measure = music21.stream.Measure()

for el in stream_new_nPVI:
    measure.insert(el.offset, el)

new_measure = measure.flat.getElementsNotOfClass(music21.meter.TimeSignature)
new_measure.insert(0, music21.meter.TimeSignature('4/8'))

new_measure_fixed = new_measure.makeNotation()
new_measure_fixed.show()
