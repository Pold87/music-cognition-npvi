from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy

original_song = 'Tetris_Type_A_-_Korobeiniki.xml'
file_name = original_song.split('_')[0]

desired_npvi = 40
metrical = True

if metrical:
    namepart = "metrical"
    max_sd = 0.05
    min_sd = 0
else:
    namepart = "nonmetrical"
    max_sd = 1
    min_sd = 0.20

output = "/home/pold/npvi/" + file_name + str(desired_npvi) + "_" + namepart + ".mid"

base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs/"

song = m21.converter.parse(base_path + original_song)

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
song_changer = changer.nPVI_changer(song)
nPVI= song_changer.get_new_nPVI()
print('nPVI', nPVI)
#lowest_nPVI = song_changer.find_lowest(True)
#print('lowest', song_changer.get_new_nPVI())
#highest_nPVI = song_changer.find_highest(True)
#print('highest', song_changer.get_new_nPVI())
# Find highest nPVI by intercepting note durations (short - long, short - long)
# song_changer.add_gaussian_noise(sd = 0.01)

song_changer.find_incrementally_from_lowest(desired_npvi, 2, min_sd=min_sd, max_sd=max_sd)

print("nPVI is: ")
print(song_changer.get_new_nPVI())
song_changer.new_song.write("midi", output)
print("Wrote to", output)
