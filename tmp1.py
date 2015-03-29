import music21 as m21
import nPVIchanger_noflat as changer

base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/"

# Parse a Music XML file with music21
song = m21.converter.parse(base_path + "experiment/mm_25_1_1.xml")

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
mychanger = changer.nPVI_changer(song)
print("nPVI is: ", mychanger.get_new_nPVI())
# Reverse the note durations of this 15s piece
mychanger.reverse_durations()
# The nPVI stays exactly the same
print("nPVI is: ", mychanger.get_new_nPVI())
mychanger.new_song.write('xml', 'mm_0_1_2.xml')