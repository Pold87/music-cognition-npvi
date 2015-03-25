import music21
import numpy as np
import copy


class nPVI_changer():

    def __init__(self, old_song):

        # The first three fields do never change
        self.old_song = self.normalize_song(old_song)
        self.old_notes = self.get_notes(self.old_song)
        self.old_durations = self.get_durations(self.old_song)

        # All manipulations are taking placing here:
        self.new_song = self.normalize_song(self.old_song)
        self.new_notes = self.get_notes(self.old_song)
        self.new_durations = self.get_durations(self.old_song)

    # Helpers

    def normalize_song(self, song):
        notes = song.flat.notesAndRests
        normalized_song = music21.stream.Stream()

        for note in notes:
            if note.isNote or note.isRest:
                normalized_song.append(note)

        return normalized_song

    def get_notes(self, song):
            
        notes = np.array([note for note in song
                          if note.isNote or note.isRest])
        return notes

    def get_durations(self, song):

        notes_durations = np.array([note.quarterLength
                                    for note in song
                                    if note.isNote or note.isRest])

        return notes_durations

    def get_old_nPVI(self):

        return music21.analysis.patel.nPVI(self.old_song)

    def get_new_nPVI(self):
        return music21.analysis.patel.nPVI(self.new_song)

    def update(self, new_song):

        self.new_song = new_song
        self.new_notes = self.get_notes(self.new_song)
        self.new_durations = self.get_durations(self.new_song)

    # Low-level

    def change_nPVI(self, new_durations, do_update=False):
        new_song = music21.stream.Stream()

        for n, d in zip(self.new_notes, new_durations):
            new_n = copy.deepcopy(n)
            new_n.quarterLength = d
            new_song.append(new_n)

        if do_update:
            self.update(new_song)

        return new_song

    # High-level

    def add_noise(self):

        noise = np.random.beta(1, 1, len(self.new_notes))
        new_durations = self.new_durations + noise
        return self.change_nPVI(new_durations, True)

    def find_by_permutation(self, goal, eps=10, n=100000):
        for i in xrange(n):
            new_durations = np.random.permutation(self.new_durations)
            new_song = self.change_nPVI(new_durations, False)
            new_nPVI = music21.analysis.patel.nPVI(new_song)
            if abs(new_nPVI - goal) < eps:
                print("Found nPVI")
                self.update(new_song)
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
        