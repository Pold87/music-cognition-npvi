import nPVIchanger_noflat
import music21
from os import path, listdir
import numpy as np


base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs"

songs = listdir(base_path)

for song in songs:
    parsed_song = music21.converter.parse(path.join(base_path, song))
    song_changer = nPVIchanger_noflat.nPVI_changer(parsed_song)

    print(song_changer.get_new_nPVI())

    song_changer.reverse_durations()

    print(song)

    song_changer.new_song.write('xml',
                               path.join('reversed15s',
                               song +
                               "_" +
                               "_rev_" +         
                               str(np.around(song_changer.get_new_nPVI(), 0)) +
                               ".xml"))

    print(song_changer.get_new_nPVI())

# song_changer.new_song.show()
