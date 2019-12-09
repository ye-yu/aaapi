"""
A module to perform music-related operations
"""

import numpy as np
import pandas as pd


def analyse_scale(column, all_scores=False, only_use_top=7):
    value_counts = column.value_counts().reindex(get_notes(), fill_value=0).sort_values(ascending=False)
    # get top 7 notes
    if only_use_top:
        value_counts = value_counts[:only_use_top].reindex(get_notes(), fill_value=0).sort_values(ascending=False)
    scales = get_scales()
    scales_scores = {v: value_counts[scales[i]].sum() for i, v in enumerate(get_notes())}
    if all_scores:
        return scales_scores
    scales_scores = pd.Series(scales_scores)
    scales_scores = scales_scores / scales_scores.sum()
    return scales_scores.idxmax(), scales_scores.max()


def get_notes():
    return np.array([
        'A',
        'A#',
        'B',
        'C',
        'C#',
        'D',
        'D#',
        'E',
        'F',
        'F#',
        'G',
        'G#'
    ])


def get_scales():  # major scales only
    notes = get_notes()
    major_scale_indexers = np.array([
        0,
        2, 3,
        5,
        7, 8,
        10
    ])
    scales = np.array([
        notes[
            np.sort((major_scale_indexers + i) % 12)
        ] for i in range(notes.shape[0])
    ])
    scales = np.concatenate((scales[-3:], scales[:-3]))
    return scales
