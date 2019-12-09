"""
A module to perform midi operations
"""

import numpy as np
import pandas as pd
import mido


def note_class(freq):
    a4 = 440
    c0 = a4 * np.power(2, -4.75)
    h = np.round(12 * np.log2(freq / c0)).astype(np.int8)
    n = h % 12
    return n


def octave(freq):
    a4 = 440
    c0 = a4 * np.power(2, -4.75)
    h = np.round(12 * np.log2(freq / c0)).astype(np.int8)
    oct_ = h // 12 - 1
    return oct_


def note(freq, midi=False):
    a4 = 440
    c0 = a4 * np.power(2, -4.75)
    return np.round(12 * np.log2(freq / c0)).astype(np.int8)


def label(note_or_freq, octave_n=None):
    name = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
    if octave_n is None:
        notes = name[note_class(note_or_freq)]
        octave_n = octave(note_or_freq).astype(str)
    else:
        notes = name[note_or_freq]
    return np.core.defchararray.add(notes.astype(str), octave_n.astype(str))


def csv_to_midi(df, dest, note_column='note', duration_column='duration', rest_notation=-1):
    song = SingleTrackMidi(dest)
    for i, v in df.iterrows():
        if v[note_column] == rest_notation:
            song.insert_rest(v[duration_column])
            continue
        song.insert_note(v[note_column], v[duration_column])
    song.save()


def group(df, note_column='note', duration_column='duration'):
    """
    https://stackoverflow.com/questions/40802800/how-to-groupby-consecutive-values-in-pandas-dataframe
    """
    return pd.DataFrame(
        [
            [g[duration_column].sum(), g[note_column].head(1).tolist()[0]]
            for i, g in df.groupby([(df[note_column] != df[note_column].shift()).cumsum()])
        ],
        columns=[duration_column, note_column]
    )


def group_weighted_average(
        song_df,
        note_thresh=4,
        dur_thresh=150,
        wa_thresh=3,
        duration_column='duration',
        note_column='note'):
    """
    note_thresh: the max number of notes to group together
    dur_thresh: the max number of duration of a note to be grouped together
    wa_thresh: the distance threshold from the current note to the weighted-averaged grouped note
    """
    grp = list()
    new_notes = list()
    curr_wa = None

    def note_weighted_average(notes):
        notes = pd.DataFrame(notes)
        weighted_note = np.round(np.average(notes['note'], weights=notes['duration'])).astype(int)
        duration = notes['duration'].sum()

        o, n = divmod(weighted_note, 12)
        o -= 1

        return pd.Series(dict(
            duration=duration,
            note=weighted_note
        ))

    for i, v in song_df.iterrows():
        dur = v[duration_column]
        n = v[note_column]
        # Stop grouping when rest or current note duration is long
        if n == -1 or dur > dur_thresh:
            if curr_wa is not None:
                new_notes += [curr_wa]
                grp = list()
                curr_wa = None
            new_notes += [v]
            continue

        # current weighted average is not none, check
        #  - if the current note exceeds the distance threshold from the weighted average
        #  - if the grouped notes exceed the length limit
        # stop grouping if at least one condition is met
        if curr_wa is not None:
            if np.abs(n - curr_wa['note']) > wa_thresh or len(grp) >= note_thresh:
                new_notes += [curr_wa]
                grp = [v]
                curr_wa = v
                continue

        # current limiting condition is not met
        # appending short notes
        grp += [v]
        curr_wa = note_weighted_average(grp)

    if curr_wa is not None:
        new_notes += [curr_wa]
    return pd.DataFrame(new_notes).reset_index(drop=True)


class SingleTrackMidi:
    def __init__(self, filename, track_program=None):
        self.filename = filename
        self.file = mido.MidiFile()
        self.single_track = mido.MidiTrack()
        self.rest = 0

        # appending single track to midi file
        self.file.tracks.append(self.single_track)

        if track_program:
            self.single_track.append(mido.Message('program_change', program=track_program, time=0))

        if not self.filename.endswith('.mid'):
            self.filename += '.mid'

    def insert_note(self, note, duration, velocity=64):
        self.single_track.append(mido.Message('note_on', note=note, velocity=velocity, time=self.rest))
        self.single_track.append(mido.Message('note_off', note=note, velocity=127, time=duration))
        self.rest = 0

    def insert_rest(self, duration):
        self.rest += duration

    def save(self):
        self.file.save(self.filename)
