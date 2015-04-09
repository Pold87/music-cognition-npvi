from __future__ import print_function
import nPVIchanger_noflat as changer
import music21 as m21
from subprocess import call
from copy import deepcopy
import numpy as np
from os import path, listdir, system

songpath = "/home/pold/npvi/versions/aubio/norests/"
song1 = m21.converter.parse("/home/pold/npvi/nucki.xml")
song_changer = changer.nPVI_changer(song1)

def aubio_metricness(midisong, do_print=False):

    file_name = "../tmpcsasdasdvaubio.csv" # TODO: automatically assign file name
    system("aubiotrack " + midisong + " > " + songpath + file_name)
    timestamps = np.genfromtxt(songpath + file_name, delimiter='\n')
    durations = np.diff(timestamps)
    sd = np.std(durations)
    return sd

all_files = listdir(songpath)

for s in all_files:
    print(s)
    midisong = songpath + s
    song = m21.converter.parse(midisong)
    print(m21.analysis.patel.nPVI(song.flat.notesAndRests))
    print(song_changer.get_metricness(midisong, do_print=False))
    print("Aubio Metricness")
    print(aubio_metricness(midisong))


