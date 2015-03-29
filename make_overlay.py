import nPVIchanger_noflat
import music21 as m21
from os import path, listdir
import numpy as np
from random import randint


base_path = "/home/pold/Dropbox/Uni/Radboud/Music_Cognition/nPVI/songs"

songs = listdir(base_path)

other_songs = m21.corpus.getComposer('ryansMammoth')

for song in songs:
    parsed_song = m21.converter.parse(path.join(base_path, song))
    song_changer = nPVIchanger_noflat.nPVI_changer(parsed_song)

    other_song = other_songs[randint(0, len(other_songs) - 1)]
    parsed_other_song = m21.converter.parse(other_song)

    song_changer.overlay_with_other_song(parsed_other_song).notes

    song_changer.new_song.write('xml',
                               path.join('overlay15s',
                               song +
                               "_" +
                               path.splitext(path.basename(other_song))[0] +
                               "_" +
                               str(np.around(song_changer.get_new_nPVI(), 0)) +
                               ".xml"))

    print(song_changer.get_new_nPVI())
