#!/usr/bin/env python3
"""
A tool to find and draw all possible chord finger positions on
a string instrument. Partially inspired by a finger injury.
"""

import logging
import sys
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


SEMITONE_INDEX = {
    "A": 0,
    "A#": 1, "Bb": 1,
    "B": 2,
    "C": 3,
    "C#": 4, "Db": 4,
    "D": 5,
    "D#": 6, "Eb": 6,
    "E": 7,
    "F": 8,
    "F#": 9, "Gb": 9,
    "G": 10,
    "G#": 11, "Ab": 11
}

INVERTED_SEMITONE_INDEX = {val: key for key, val in SEMITONE_INDEX.items()}

SEMITONE_DIVISOR = 12

CHORD_INTERVALS = {
    "major":  [0, 4, 7, 12],
    "minor":  [0, 3, 7, 12],
    "7":      [0, 4, 7, 11],
    "major7": [0, 4, 7, 10],
    "minor7": [0, 3, 7, 10]
}


class FrettedStringInstrument:
    def __init__(self, string_list, num_frets):
        self.string_list = string_list
        self.num_frets = num_frets

class SopranoUkulele(FrettedStringInstrument):
    def __init__(self):
        FrettedStringInstrument.__init__(self, ["G", "C", "E", "A"], 12)
        # TODO: Non-standard tuning

class StandardGuitar(FrettedStringInstrument):
    def __init__(self):
        FrettedStringInstrument.__init__(self, ["E", "A", "D", "G", "B", "E"], 19)


class StandardHand:
    def __init__(self):
        self.finger_list = [1, 2, 3, 4]
        # TODO: Non-standard hand


class FingeringSolver:
    def __init__(self, instrument, hand):
        self.instrument = instrument
        self.hand = hand # currently unused

    def get_chord_notes(self, root, chord):
        """
        Return a list of valid notes for the given root and chord
        """
        note_list = []
        interval_distance_list = CHORD_INTERVALS[chord]
        for interval_distance in interval_distance_list:
            note_idx = SEMITONE_INDEX[root]
            interval_note_idx = (note_idx + interval_distance) % SEMITONE_DIVISOR
            note_list.append(INVERTED_SEMITONE_INDEX[interval_note_idx])
        return note_list

    def find_valid_frets_on_string(self, string_tone, num_frets, root, chord):
        """
        Return a list of frets indicies that can be pressed on a string
        of the given tone and number of frets for the given root and chord
        """
        fret_list = []
        target_note_set = set(self.get_chord_notes(root, chord))
        logger.debug(root + " " + chord + " = " + str(target_note_set))
        string_note_idx = SEMITONE_INDEX[string_tone]
        for fret_idx in range(num_frets + 1): # + 1 to account for open string
            fretted_note_idx = (string_note_idx + fret_idx) % SEMITONE_DIVISOR
            fretted_note = INVERTED_SEMITONE_INDEX[fretted_note_idx]
            if fretted_note in target_note_set:
                fret_list.append(fret_idx)
        return fret_list

    def draw_all_possible_frets_for(self, root, chord):
        """
        Draw a diagram of all possible finger positions on this insturment
        for the given root and chord.
        """
        print(root + " " + chord)
        for string_tone in reversed(self.instrument.string_list):
            valid_fret_list = self.find_valid_frets_on_string(
                string_tone, self.instrument.num_frets, root, chord)

            # draw the frets to be pressed on this string
            string_output_line = string_tone + "|"
            if 0 in valid_fret_list:
                string_output_line += "o" # play open string
            else:
                string_output_line += " "

            for fret_idx in range(1, self.instrument.num_frets + 1):
                if fret_idx in valid_fret_list:
                    string_output_line += "x" # valid fret
                else:
                    string_output_line += "-"
            print(string_output_line)


if __name__ == "__main__":
    ukulele = SopranoUkulele()
    guitar = StandardGuitar()
    hand = StandardHand()
    solver = FingeringSolver(ukulele, hand)

    parser = argparse.ArgumentParser(description=
        'A tool to draw all possible chord finger positions on a soprano ukulele')
    parser.add_argument('root', choices=SEMITONE_INDEX.keys(), help='the root of the chord')
    parser.add_argument('chord', choices=CHORD_INTERVALS.keys(), help='the type of chord')
    args = parser.parse_args()

    solver.draw_all_possible_frets_for(args.root, args.chord)
    """
    solver = FingeringSolver(guitar, hand)
    # I–V–vi–IV progression (B)
    solver.draw_all_possible_frets_for("B", "major")
    solver.draw_all_possible_frets_for("F#", "major")
    solver.draw_all_possible_frets_for("Ab", "minor")
    solver.draw_all_possible_frets_for("E", "major")
    """
