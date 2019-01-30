#!/usr/bin/env python3
"""
Calculates all possible chord finger positions on a string instrument
"""

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
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
    def __init__(self, stringList, numFrets):
        self.stringList = stringList
        self.numFrets = numFrets

class SopranoUkulele(FrettedStringInstrument):
    def __init__(self):
        FrettedStringInstrument.__init__(self, ["G", "C", "E", "A"], 12)
		# TODO: Non-standard tuning

class StandardGuitar(FrettedStringInstrument):
    def __init__(self):
        FrettedStringInstrument.__init__(self, ["E", "A", "D", "G", "B", "E"], 19)

class StandardHand:
    def __init__(self):
        self.fingerList = [1, 2, 3, 4]
	# TODO: Non-standard hand

class FingeringSolver:
    def __init__(self, instrument, hand):
        self.instrument = instrument
        self.hand = hand

    def getChordNotes(self, root, chord):
        noteList = []
        intervalDistList = CHORD_INTERVALS[chord]
        for intervalDist in intervalDistList:
            noteIdx = SEMITONE_INDEX[root]
            intervalNoteIdx = (noteIdx + intervalDist) % SEMITONE_DIVISOR
            noteList.append(INVERTED_SEMITONE_INDEX[intervalNoteIdx])
        return noteList

    def findValidFretsOnString(self, stringTone, numFrets, root, chord):
        fretList = []
        targetNoteSet = set(self.getChordNotes(root, chord))
        logger.debug(root + " " + chord + " = " + str(targetNoteSet))
        stringNoteIdx = SEMITONE_INDEX[stringTone]
        for fretIdx in range(numFrets+1): # +1 to account for open string
            frettedNoteIdx = (stringNoteIdx + fretIdx) % SEMITONE_DIVISOR
            frettedNote = INVERTED_SEMITONE_INDEX[frettedNoteIdx]
            if frettedNote in targetNoteSet:
                fretList.append(fretIdx)
        return fretList

    def drawAllPossibleFretsFor(self, root, chord):
        print(root + " " + chord)
        for string in reversed(self.instrument.stringList):
            validFretList = self.findValidFretsOnString(string, self.instrument.numFrets,
                                                        root, chord)
			# draw the frets on this string
            stringOutputLine = string + "|"
            if 0 in validFretList:
                stringOutputLine += "o" # open string
            else:
                stringOutputLine += " "

            for fretIdx in range(1, self.instrument.numFrets+1):
                if fretIdx in validFretList:
                    stringOutputLine += "x" # valid fret
                else:
                    stringOutputLine += "-"
            print(stringOutputLine)


if __name__ == "__main__":
    ukulele = SopranoUkulele()
    guitar = StandardGuitar()
    hand = StandardHand()
    solver = FingeringSolver(ukulele, hand)
    #solver = FingeringSolver(guitar, hand)
    #solver.drawAllPossibleFretsFor("F#", "7")

    solver.drawAllPossibleFretsFor("G", "major")
    solver.drawAllPossibleFretsFor("D", "major")
    solver.drawAllPossibleFretsFor("E", "minor")
    solver.drawAllPossibleFretsFor("C", "major")
