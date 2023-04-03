from music21 import *
import numpy as np
import matplotlib.pyplot as plt

def plot_degree_freq(data):
	plt.plot(data)
	plt.show()

def plot_degree_matrix(data):
	plt.matshow(data)
	plt.show()

note_freq = [0, 0, 0, 0, 0, 0, 0]
chord_trans_freq = [[0 for i in range(8)] for o in range(8)]
note_trans_freq = [[0 for i in range(8)] for o in range(8)]

key = key.Key('C')
score = converter.parse('/home/rng/src/diss_eval/out.musicxml')

# chord freq
chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
for c in chords:
	d = roman.romanNumeralFromChord(c, key).scaleDegree
	freq[d] += 1
plot_degree_freq(freq)

# melody note freq
freq = [0, 0, 0, 0, 0, 0, 0, 0]
melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
for n in melody:
	d = roman.romanNumeralFromChord(chord.Chord([n]), key).scaleDegree
	freq[d] += 1
plot_degree_freq(freq)

# chord transition freq
chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
for c in range(0, len(chords)-1):
	da = roman.romanNumeralFromChord(chords[c], key).scaleDegree
	db = roman.romanNumeralFromChord(chords[c+1], key).scaleDegree
	tfreq[da][db] += 1
plot_degree_matrix(tfreq)

# melody note transition freq
tfreq = [[0 for i in range(8)] for o in range(8)]
melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
for n in range(0, len(melody)-1):
	da = roman.romanNumeralFromChord(chord.Chord([melody[n]]), key).scaleDegree
	db = roman.romanNumeralFromChord(chord.Chord([melody[n+1]]), key).scaleDegree
	tfreq[da][db] += 1
plot_degree_matrix(tfreq)


def get_chord_freq(score, key):
	chord_freq = [0, 0, 0, 0, 0, 0, 0]
	chord = score.measure(1).chordify().recurse().getElementsByClass('Chord')
	for c in chords:
		d = roman.romanNumeralFromChord(c, key).scaleDegree
		chord_freq[d] += 1
	return chord_freq
		

def get_note_freq(score, key):
	note_freq = [0, 0, 0, 0, 0, 0, 0]
	melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
	for n in melody:
		d = roman.romanNumeralFromChord(chord.Chord([n]), key).scaleDegree
		note_freq[d] += 1
	return note_freq


def get_chord_trans_freq(score, key):
	trans_freq = [[0 for i in range(8)] for o in range(8)]
	chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
	for c in range(0, len(chords)-1):
		da = roman.romanNumeralFromChord(chords[c], key).scaleDegree
		db = roman.romanNumeralFromChord(chords[c+1], key).scaleDegree
		trans_freq[da][db] += 1
	return trans_freq


def get_note_trans_freq(score, key):
	trans_freq = [[0 for i in range(8)] for o in range(8)]
	melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
	for n in range(0, len(melody)-1):
		da = roman.romanNumeralFromChord(chord.Chord([melody[n]]), key).scaleDegree
		db = roman.romanNumeralFromChord(chord.Chord([melody[n+1]]), key).scaleDegree
		trans_freq[da][db] += 1
	return trans_freq
