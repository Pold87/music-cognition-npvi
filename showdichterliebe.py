import music21

sBach = music21.corpus.parse('schumann/dichterliebe_no2.xml')
s1 = sBach.parts[0].flat.notesAndRests
s1.show()
