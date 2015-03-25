import nPVIchanger_noflat
import music21
import os

fp = "/home/pold/Downloads/ALittleMoreTimeonYou.mid"
mf = music21.midi.MidiFile()
mf.open(fp)
mf.read()
mf.close()
print(len(mf.tracks))

bachChorale = music21.corpus.parse('bwv66.6')[1]
song2 = music21.midi.translate.midiFileToStream(mf)


# Create nPVI changer for this song
timeonyou_changer = nPVIchanger_noflat.nPVI_changer(song2)
timeonyou_changer.new_song.write('xml', 'original.xml')

timeonyou_changer.overlay_with_other_song(bachChorale)
timeonyou_changer.new_song.write('xml', 'overlayed.xml')


#timeonyou_changer.add_noise()
#timeonyou_changer.new_song.write('midi', 'addednoise.mid')

#timeonyou_changer.new_song.write('xml', 'addednoise.xml')



timeonyou_changer.new_song.show()

