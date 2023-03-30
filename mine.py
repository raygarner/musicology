from music21 import *
import numpy as np
import matplotlib.pyplot as plt

key = key.Key('C')
score = converter.parse('/home/rng/src/music_tools/out.musicxml')
chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
print(len(chords))
for c in chords:
	print(roman.romanNumeralFromChord(c, key).scaleDegree)
print()
melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
for n in melody:
	print(roman.romanNumeralFromChord(chord.Chord([n]), key).scaleDegree)

