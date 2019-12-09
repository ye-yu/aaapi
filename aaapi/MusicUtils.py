"""
A module to perform music-related operations
"""

import numpy as np
import pandas as pd


def analyse_scale(column, all_scores=False, only_use_top=7):
    value_counts = column.value_counts().reindex(get_note_classes(), fill_value=0).sort_values(ascending=False)
    # get top 7 notes
    if only_use_top:
        value_counts = value_counts[:only_use_top].reindex(get_note_classes(), fill_value=0).sort_values(ascending=False)
    scales = get_scales()
    scales_scores = {v: value_counts[scales[i]].sum() for i, v in enumerate(get_note_classes())}
    if all_scores:
        return scales_scores
    scales_scores = pd.Series(scales_scores)
    scales_scores = scales_scores / scales_scores.sum()
    return scales_scores.idxmax(), scales_scores.max()


def get_note_classes():
    return np.array([
        'C',
        'C#',
        'D',
        'D#',
        'E',
        'F',
        'F#',
        'G',
        'G#',
        'A',
        'A#',
        'B'
    ])


def get_scales():  # major scales only
    notes = get_note_classes()
    major_scale_indexers = np.array([
        0, 2, 4,
        5, 7, 9, 11
    ])
    scales = np.array([
        notes[
            np.sort((major_scale_indexers + i) % 12)
        ] for i in range(notes.shape[0])
    ])
    return scales


def get_scale(scale):
    scales = get_scales()
    note_classes = get_note_classes()
    idx = np.where(note_classes == scale)[0]
    return scales[idx]


a4 = 440
c0 = a4 * np.power(2, -4.75)


def freq_to_note(freq):
    return np.round(12 * np.log2(freq / c0)).astype(np.int8) + 12


def note_to_freq(note):
    return np.round(np.power(2, (note - 12) / 12) * c0, 2)


def oct_note_to_midi_note(octave, note):
    return (octave + 1) * 12 + note


def midi_note_to_oct_note(note):
    octave, note_class = divmod(note, 12)
    octave -= 1
    return octave, note_class


def midi_note_to_label(note):
    octave, note_class = midi_note_to_oct_note(note)
    note_classes = get_note_classes()
    return "{}{}".format(note_classes[note_class], octave)


def label_to_midi_note(label):
    note_class = label[:-1]
    octave = int(label[-1])
    note_classes = get_note_classes()
    note_class = np.where(note_classes == note_class)[0]
    return oct_note_to_midi_note(octave, note_class)
