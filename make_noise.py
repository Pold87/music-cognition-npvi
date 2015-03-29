import nPVIchanger_noflat
import music21
from os import path, listdir
import numpy as np
from random import randint


base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/overlay15s"

songs = listdir(base_path)

for song in songs:
    parsed_song = music21.converter.parse(path.join(base_path, song))
    song_changer = nPVIchanger_noflat.nPVI_changer(parsed_song)

    song_changer.find_by_permutation(goal = 100, eps = 100, n = 1)
    song_changer.add_gaussian_noise(0.15)

    song_changer.new_song.write('xml',
                               path.join('noisy2',
                               song +
                               "_" +
                               str(np.around(song_changer.get_new_nPVI(), 0)) +
                               ".xml"))

    print(song_changer.get_new_nPVI())

# song_changer.new_song.show()
