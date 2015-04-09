from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy

output = "/home/pold/npvi/jap20nonmetrical.mid"

base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs/"

song = m21.converter.parse(base_path + 'Japanese_folk_song.xml')

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
song_changer = changer.nPVI_changer(song, tmp_midi_file="/home/pold/npvi/tmjappa.mid")

# Find highest nPVI by intercepting note durations (short - long, short - long)

# song_changer.add_gaussian_noise(sd = 0.01)

song_changer.find_incrementally_from_lowest(20, eps=3, min_sd=0.2)

print("nPVI is: ")
print(song_changer.get_new_nPVI())
song_changer.new_song.write("midi", output)
