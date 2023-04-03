from music21 import *
import numpy as np
import matplotlib.pyplot as plt
import os


def plot_degree_freq(data):
	plt.plot(data)
	plt.show()


def plot_degree_matrix(data):
	plt.matshow(data)
	plt.show()


def add_lists(xs, ys):
	for i in range(0, len(xs)-1):
		xs[i] += ys[i]


def add_matrices(xs, ys):
	for m in range(0, len(xs)-1):
		for n in range(0, len(xs[0])-1):
			xs[m][n] += ys[m][n]
			

def get_chord_freq(score, key):
	chord_freq = [0, 0, 0, 0, 0, 0, 0, 0]
	chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
	for c in chords:
		d = roman.romanNumeralFromChord(c, key).scaleDegree
		if d < len(chord_freq):
			chord_freq[d] += 1
	return chord_freq
		

def get_note_freq(score, key):
	chord_freq = [0, 0, 0, 0, 0, 0, 0, 0]
	melody = score.getElementsByClass('Part')[0].measure(1).getElementsByClass('Note')
	for n in melody:
		d = roman.romanNumeralFromChord(chord.Chord([n]), key).scaleDegree
		if d < len(note_freq):
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


key = key.Key('C')
chord_freq = [0, 0, 0, 0, 0, 0, 0, 0]
note_freq = [0, 0, 0, 0, 0, 0, 0, 0]
chord_trans_freq = [[0 for i in range(8)] for o in range(8)]
note_trans_freq = [[0 for i in range(8)] for o in range(8)]
path = '/home/rng/src/diss_eval'
dir = os.fsencode(path)
for file in os.listdir(dir):
	filename = os.fsdecode(file)
	if filename.endswith('.musicxml'):
		full_path = path + '/' + filename
		print(full_path)
		score = converter.parse(full_path)
		add_lists(chord_freq, get_chord_freq(score, key))
		add_lists(note_freq, get_note_freq(score, key))
		add_matrices(chord_trans_freq, get_chord_trans_freq(score, key))
		add_matrices(note_trans_freq, get_note_trans_freq(score, key))
plot_degree_freq(chord_freq)
plot_degree_freq(note_freq)
plot_degree_matrix(chord_trans_freq)
plot_degree_matrix(note_trans_freq)

