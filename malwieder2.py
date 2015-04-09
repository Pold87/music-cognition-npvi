from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy
import numpy as np

songpath = "/home/pold/npvi/dragon20metrical.mid"
song = m21.converter.parse(songpath)


song_changer = changer.nPVI_changer(song)


song_changer.get_metricness(songpath, do_print=True)

# song2.show()

diff = np.diff(np.genfromtxt("/home/pold/npvi/dragon20m.csv", delimiter='\n'))

print(diff)

print(np.std(diff))

# song_changer.new_song.show()

