from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy


base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs/"

extension = "xml"
f = "/home/pold/npvi/tmp." + extension

song2 = m21.converter.parseFile(f)

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
song_changer = changer.nPVI_changer(song2)


print("nPVI is: ")
print(song_changer.get_new_nPVI())

print("read nPVI is")
print(m21.analysis.patel.nPVI(song2.flat.notesAndRests))

for n in song2.flat.notesAndRests:
    print(n)
    print(n.offset)


# song2.show()


# song_changer.new_song.show()

