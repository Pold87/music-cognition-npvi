import nPVIchanger
import music21
import os

fp = "/home/pold/Downloads/ALittleMoreTimeonYou.mid"
mf = music21.midi.MidiFile()
mf.open(fp)
mf.read()
mf.close()
print(len(mf.tracks))

song2 = music21.midi.translate.midiFileToStream(mf)
song2

len(song2.flat.notesAndRests)

song = music21.corpus.parse('schumann/dichterliebe_no2.xml')

dichterliebe_changer = nPVIchanger.nPVI_changer(song)

#low_nPVI = dichterliebe_changer.find_lowest()
#high_nPVI = dichterliebe_changer.find_highest()
#noisy = dichterliebe_changer.add_noise()
#find25 = dichterliebe_changer.find_by_permutation(25, eps=3)

#print(music21.analysis.patel.nPVI(low_nPVI))
#print(music21.analysis.patel.nPVI(high_nPVI))
#print(music21.analysis.patel.nPVI(noisy))
#print(music21.analysis.patel.nPVI(find25))
#print(dichterliebe_changer.get_old_nPVI())


print(dichterliebe_changer.get_old_nPVI())
# dichterliebe_changer.old_song.show()


dichterliebe_changer.reverse_durations()

print(dichterliebe_changer.get_new_nPVI())

for n in song.flat:
    print(n)


def nPVI(s):
    totalElements = len(s)

    print(totalElements)
    
    summation = 0
    prevQL = s[0].quarterLength
    for i in range(1, totalElements):

        thisQL = s[i].quarterLength

        if thisQL > 0 and prevQL > 0:
            summation += abs(thisQL - prevQL)/((thisQL + prevQL)/2.0)
        else:
            pass
        prevQL = thisQL

    final = summation * 100.0/(totalElements - 1)
    return final

    
# dichterliebe_changer.find_lowest()

# print(nPVI(song.flat.notesAndRests))
    # print(nPVI(dichterliebe_changer.new_song))