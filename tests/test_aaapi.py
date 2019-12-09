#!/usr/bin/env python

"""Tests for `aaapi` package."""


import unittest

from aaapi import aaapi
import numpy as np


class TestAaapi(unittest.TestCase):
    """Tests for `aaapi` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_c_major_scale(self):
        notes = aaapi.MusicUtils.get_scale('C')
        expected_notes = np.array(list('CDEFGAB'))
        assert (notes == expected_notes).all()

    def test_all_major_scale(self):
        note_classes = aaapi.MusicUtils.get_note_classes()

        # sorted array of note scales
        expected_scales = np.array([
            ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            ['C', 'C#', 'D#', 'F', 'F#', 'G#', 'A#'],
            ['C#', 'D', 'E', 'F#', 'G', 'A', 'B'],
            ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#'],
            ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],
            ['C', 'D', 'E', 'F', 'G', 'A', 'A#'],
            ['C#', 'D#', 'F', 'F#', 'G#', 'A#', 'B'],
            ['C', 'D', 'E', 'F#', 'G', 'A', 'B'],
            ['C', 'C#', 'D#', 'F', 'G', 'G#', 'A#'],
            ['C#', 'D', 'E', 'F#', 'G#', 'A', 'B'],
            ['C', 'D', 'D#', 'F', 'G', 'A', 'A#'],
            ['C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B']], dtype='<U2')
        for i, v in enumerate(note_classes):
            scales = aaapi.MusicUtils.get_scale(v)
            print(v, scales)
            self.assertTrue((scales == expected_scales[i]).all())
