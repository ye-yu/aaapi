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
            self.assertTrue((scales == expected_scales[i]).all())

    def test_freq_note(self):
        note = 69
        freq = aaapi.MusicUtils.note_to_freq(69)
        expected_note = aaapi.MusicUtils.freq_to_note(freq)
        self.assertEqual(note, expected_note)

    def test_midi_octave_note(self):
        note = 69
        octave, note_class = aaapi.MusicUtils.midi_note_to_oct_note(note)
        expected_note = aaapi.MusicUtils.oct_note_to_midi_note(octave, note_class)
        self.assertEqual(note, expected_note)

    def test_440hz_to_C_note(self):
        freq = 261.63
        note = aaapi.MusicUtils.freq_to_note(freq)
        expected_note = 60
        self.assertEqual(note, expected_note, msg="Expected {}: got {} instead.".format(expected_note, note))

    def test_60midi_to_oct_note(self):
        note = 60
        octave, note_class = aaapi.MusicUtils.midi_note_to_oct_note(note)
        expected_octave, expected_note_class = 4, 0
        self.assertEqual(octave, expected_octave)
        self.assertEqual(note_class, expected_note_class)

    def test_C4note_to_label(self):
        note = 60
        label = aaapi.MusicUtils.midi_note_to_label(note)
        expected_label = 'C4'
        self.assertEquals(label, expected_label)

    def test_C4label_to_midi(self):
        label = 'C4'
        note = aaapi.MusicUtils.label_to_midi_note(label)
        expected_note = 60
        self.assertEqual(note, expected_note)
