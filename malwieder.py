from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy


base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs/"

song = m21.converter.parse(base_path + 'Tetris_Type_A_-_Korobeiniki.xml')

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
song_changer = changer.nPVI_changer(song)

# Find highest nPVI by intercepting note durations (short - long, short - long)

# song_changer.add_gaussian_noise(sd = 0.01)
# song_changer.find_lowest()

song_changer.find_by_permutation(30, 5, min_sd=0.035)


print("nPVI is: ")
print(song_changer.get_new_nPVI())

song_changer.new_song.write("midi", "/home/pold/npvi/tetris30.mid")

#Test
#song_changer.new_song.show()
extension = "xml"
#file = "/home/pold/npvi/tmp." + extension
#song_changer.new_song.write(extension, file)
#song2 = m21.converter.parseFile(file)
#print("read nPVI is")
#print(m21.analysis.patel.nPVI(song2.flat.notesAndRests))

song_changer.get_metricness("/home/pold/npvi/tetris30.mid")

# song2.show()


# song_changer.new_song.show()

