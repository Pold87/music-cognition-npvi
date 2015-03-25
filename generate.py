from music21 import *


n1 = note.Note('e4')
n1.duration.type = 'whole'
n2 = note.Note('d4')
n2.duration.type = 'whole'
m1 = stream.Measure()
m2 = stream.Measure()
m1.append(n1)
m2.append(n2)
partLower = stream.Part()
partLower.append(m1)
partLower.append(m2)

data1 = [('g4', 'quarter'),
         ('a4', 'quarter'),
         ('b4', 'quarter'),
         ('c#5', 'quarter')]

data2 = [('d5', 'whole')]

data = [data1, data2]

partUpper = stream.Part()

for mData in data:
    m = stream.Measure()
    for pitchName, durType in mData:
        n = note.Note(pitchName)
        n.duration.type = durType
        m.append(n)
    partUpper.append(m)

sCadence = stream.Score()
sCadence.insert(0, partUpper)
sCadence.insert(0, partLower)
sCadence.show()
