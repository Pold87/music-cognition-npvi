from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from copy import deepcopy

base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/"

# Parse a Music XML file with music21
song = m21.converter.parse(base_path + "/" + "noisy/Ye_Jacobites.xml_103.0.xml")

# Create a changer object
# Changer objects can manipulate the nPVI of songs
# They are constructed by passing a song (the 'old song') and
# create a 'new song' based on the chosen modifications
changer_s_bach = changer.nPVI_changer(song)

# Get a 15s piece of the melody of the original song
print("nPVI is: ", changer_s_bach.get_old_nPVI())
print(changer_s_bach.get_durations(song))


# Reverse the note durations of this 15s piece
changer_s_bach.reverse_durations()
# The nPVI stays exactly the same
print("nPVI is: ", changer_s_bach.get_new_nPVI())

# The modifications have been applied to the 'new_song', while the old_song stays the same

# Find lowest nPVI for this song (by sorting note durations)
changer_s_bach.find_lowest()
print("nPVI is: ", changer_s_bach.get_new_nPVI())

# Find highest nPVI by intercepting note durations (short - long, short - long)
changer_s_bach.find_highest()
print("nPVI is: ", changer_s_bach.get_new_nPVI())
# 'Save' the current modification
changer_s_bach_copied = deepcopy(changer_s_bach)

# In my opinion, none of the used modifications 'destroys' the meter

# Add noise to the latest modification (i.e. the highest nPVI with 58)
changer_s_bach.add_uniform_noise(low = -0.1, high=0.1)
print("nPVI is: ", changer_s_bach.get_new_nPVI())

# The same with Gaussian noise
# (we had to copy the changer before, otherwise we would add uniform AND Gaussian noise)
# Normally, this increases the nPVI quite a lot
changer_s_bach_copied.add_gaussian_noise(sd = 0.15) # mean is 0
print("nPVI is: ", changer_s_bach_copied.get_new_nPVI())

# Find a certain nPVI value
# goal: the desired nPVI value
# eps: the allowed error (i.e. an nPVI of 48 would also be allowed)
# n: the iterations to find the nPVI
changer_s_bach.find_by_permutation(goal = 45, eps=30, n=100000)
print("nPVI is: ", changer_s_bach.get_new_nPVI())


# Remove the melody (i.e. play only Cs)
changer_s_bach.remove_melody()
# nPVI stays the same
print("nPVI is: ", changer_s_bach.get_new_nPVI())


# Use pitches from another song but keep note durations (i.e. create overlay)
# Create another changer (to get the original state again)
changer2 = changer.nPVI_changer(song)
other_song = m21.corpus.parse('ryansMammoth/MoneyMuskReel.abc')
changer2.overlay_with_other_song(other_song)
# nPVI is the same as in the beginning but the melody is different
print("nPVI is: ", changer2.get_new_nPVI())

# And finally listen to 15s of the original Money Musk Reel
changer_money = changer.nPVI_changer(other_song)
# nPVI is 0.57 in it's original version!
print("nPVI is: ", changer_money.get_old_nPVI())