import music21
import numpy as np
import copy


sBach = music21.corpus.parse('schumann/dichterliebe_no2.xml')
s1 = sBach.parts[0].flat.notesAndRests

print("Original nPVI")
print(music21.analysis.patel.nPVI(s1))

notes = np.array([note for note in s1 if note.isNote or note.isRest])
notes_durations = np.array([note.quarterLength
                            for note in s1
                            if note.isNote or note.isRest])



noise = np.random.beta(1, 1, len(notes_durations))

print(noise)

# Add random noise
new_notes_duration = notes_durations + noise

print(new_notes_duration)

stream_new_nPVI = music21.stream.Stream()
for n, d in zip(notes, new_notes_duration):
    new_n = copy.deepcopy(n)
    new_n.quarterLength = d
    stream_new_nPVI.append(new_n)

print("Modified nPVI")
new_nPVI = music21.analysis.patel.nPVI(stream_new_nPVI)
print(new_nPVI)

print("Found nPVI: ")
print(new_nPVI)
stream_new_nPVI.show()
