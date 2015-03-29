from __future__ import print_function
import music21
import numpy as np
import copy
from subprocess import call
import pandas as pd
import numpy as np


class nPVI_changer():

    """
    A class that changes nPVIs of existing songs.
    It takes an existing song (old_song), and is able to
    shuffle and sort the notes' durations. The final result
    can be accessed by getting self.new_song.
    """

    def __init__(self, old_song):

        # The first three fields do never change
        self.old_song = self.normalize_song(old_song)
        self.old_notes = self.get_notes(self.old_song)
        self.old_durations = self.get_durations(self.old_song)

        # All manipulations are taking placing here:
        # (new song and old song are the same in the beginning)
        self.new_song = self.normalize_song(old_song)
        self.new_notes = self.get_notes(self.old_song)
        self.new_durations = self.get_durations(self.old_song)

    # Helpers

    def normalize_song(self, song, desired_seconds = 15):
        """
        Get the first part of the song (melody) and change its bpm to 120
        """

        # Check if the song is a Score or a Stream
        if isinstance(song, music21.stream.Score):
            for part in song:
                # Search for first Stream (melody)
                if isinstance(part, music21.stream.Stream):
                    notes = part.flat.notesAndRests
                    break
        else:
            notes = song.flat.notesAndRests

        normalized_song = music21.stream.Stream()

        for note in notes:

            if isinstance(note, music21.harmony.ChordSymbol):
                continue

            normalized_song.append(note)

        bpm = 120

        ts = music21.meter.TimeSignature('200/4')
        normalized_song.insert(0, ts)

        t = music21.tempo.MetronomeMark(number=bpm)
        normalized_song.insert(0, t)


        needed_offset = bpm * desired_seconds / 60
        normalized_song = normalized_song.getElementsByOffset(0,
                                                              needed_offset,
                                                              mustFinishInSpan = True,
                                                              includeEndBoundary=True,
                                                              mustBeginInSpan=False)

        return normalized_song

    def final_update(self, song):
        bpm = 120
        t = music21.tempo.MetronomeMark(number=bpm)
        song.insert(0, t)
        return song



    def get_notes(self, song):

        notes = np.array([note for note in song])
        return notes

    def get_durations(self, song):

        notes_durations = np.array([note.quarterLength
                                    for note in song.notesAndRests])

        return notes_durations

    def get_old_nPVI(self):

        return music21.analysis.patel.nPVI(self.old_song.notesAndRests)

    def get_new_nPVI(self):
        return music21.analysis.patel.nPVI(self.new_song.notesAndRests)

    def update(self, new_song, normalize = True):

        final_new_song = new_song

        if normalize:
            final_new_song = self.normalize_song(final_new_song)

        self.new_song = final_new_song
        self.new_notes = self.get_notes(final_new_song)
        self.new_durations = self.get_durations(final_new_song)


    def normalize_durations(self, x, min_value=0.05):
        """
        Helper method for adding gaussian noise. If a value is below
        0, change this value to min_value. Otherwise, round to 2 decimals.
        """
        if x < min_value:
            return min_value
        else:
            return np.around(x, 2)

    # Low-level nPVI changer

    def change_nPVI(self, new_durations, do_update=False, do_write_and_load = False):
        """
        Actually change a song's note length distrbution
        """

        new_song = music21.stream.Stream()

        for n, d in zip(self.new_song.flat.notesAndRests, new_durations):

            if n.isRest:
                new_n = music21.note.Rest()

            else:
                new_n = music21.note.Note()
                new_n.pitches = n.pitches

            new_n.quarterLength = d
            new_song.append(new_n)


        if do_write_and_load:
            new_song.write("xml", "/home/pold/npvi/tmp.xml")
            new_song = music21.converter.parse("/home/pold/npvi/tmp.xml")

        new_song = self.normalize_song(new_song)

        if do_update:
            self.update(new_song, False)

        return new_song

    # Low-level noise function

    def add_noise(self, noise):

        new_durations = self.new_durations + noise
        vmakepositive = np.vectorize(self.normalize_durations)
        new_durations = vmakepositive(new_durations)

        return self.change_nPVI(new_durations, True, True)


    # High-level nPVI changer.
    # Provides algorithms for getting a certain distribution and
    # is able to add noise.

    def add_gaussian_noise(self, sd = 0.15):

        noise = np.random.normal(0, sd, len(self.new_durations))
        return self.add_noise(noise)

    def add_uniform_noise(self, low = -0.2, high = 0.2):

        noise = np.random.uniform(low, high)
        return self.add_noise(noise)

    def find_by_permutation(self, goal, eps=5, n=100000, max_sd = 1, min_sd = 0):
        for i in range(n):
            new_durations = np.random.permutation(self.new_durations)
            new_song = self.change_nPVI(new_durations, False)

            new_nPVI = music21.analysis.patel.nPVI(new_song.notesAndRests)

            midisong = "/home/pold/npvi/tmp.mid"
            new_song.write("midi", midisong)
            metricness = self.get_metricness(midisong)

            if metricness > max_sd or metricness < min_sd:
                continue

            if abs(new_nPVI - goal) < eps:

                # for n in new_song:
                #     print(n)
                #     print(n.offset)
                print("Found nPVI")
                print(new_nPVI)
                self.update(new_song, False)
                return new_song


    def find_lowest(self):
        new_durations = np.sort(self.new_durations)
        return self.change_nPVI(new_durations, True)

    def find_highest(self):
        lowest_first = np.sort(self.new_durations)
        highest_first = lowest_first[::-1]
        new_durations = np.array([])

        for x, (i, j) in enumerate(zip(lowest_first, highest_first)):
            if x % 2 == 0:
                new_durations = np.append(new_durations,
                                          np.array([i]))
            else:
                new_durations = np.append(new_durations,
                                          np.array([j]))

        return self.change_nPVI(new_durations, True)

    def reverse_durations(self):

        new_durations = self.new_durations[::-1]
        return self.change_nPVI(new_durations, True)
            
    def remove_melody(self):

        flattened_song = music21.stream.Stream()

        for n, d in zip(self.new_song, self.new_durations):
            new_n = music21.note.Note('C4')
            new_n.quarterLength = d
            flattened_song.append(new_n)

        self.update(flattened_song)
        return flattened_song

    def overlay_with_other_song(self, other_song):
        overlayed_song = music21.stream.Stream()

        other_song_flat = self.normalize_song(other_song, desired_seconds=60).notesAndRests

        this_song_flat = self.new_song.notesAndRests
        
        for this_n, other_n in zip(this_song_flat, other_song_flat):

            if other_n.isRest:
                new_n = music21.note.Rest()

            else:
                new_n = music21.note.Note()
                new_n.pitches = other_n.pitches

            new_n.duration = this_n.duration
            overlayed_song.append(new_n)
        self.update(overlayed_song)
        return overlayed_song

    def get_metricness(self, midisong, do_print = False):

        beatroot_path = "/home/pold/Downloads/beatroot-0.5.8.jar"
        beat_folder = "/home/pold/npvi/"
        file_name = "tmpcsv.csv" # TODO: automatically assign file name
        call(["java", "-jar", beatroot_path, "-o", beat_folder + file_name, midisong])

        timestamps = np.genfromtxt(beat_folder + file_name, delimiter=',')
        durations = np.diff(timestamps)

        sd = np.std(durations)

        if do_print:
            print("Durations", durations)
            print("SD", sd)

        return sd


