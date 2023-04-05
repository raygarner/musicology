from music21 import *
import numpy as np
import matplotlib.pyplot as plt
import os
import math


def plot_degree_freq(data, name):
	plt.plot(data)
	plt.savefig(name + '.png')
	plt.close()


def plot_degree_matrix(data, name):
	plt.matshow(data)
	plt.savefig(name + '.png')
	plt.close()


def normalise_list(xs):
	sum = 0
	for m in range(0, len(xs)-1):
		sum += xs[m]
	for m in range(0, len(xs)-1):
		xs[m] = (xs[m] / sum) * 100
	return xs


def normalise_matrix(xss):
	sum = 0
	for m in range(0, len(xss)-1):
		for n in range(0, len(xss[0])-1):
			sum += xss[m][n]
	for m in range(0, len(xss)-1):
		for n in range(0, len(xss[0])-1):
			xss[m][n] = (xss[m][n] / sum) * 100
	return xss


def add_lists(xs, ys):
	for i in range(0, len(xs)-1):
		xs[i] += ys[i]


def add_matrices(xss, yss):
	for m in range(0, len(xss)-1):
		for n in range(0, len(xss[0])-1):
			xss[m][n] += yss[m][n]
			

def get_chord_freq(score, key):
	chord_freq = [0, 0, 0, 0, 0, 0, 0, 0]
	chords = score.measure(1).chordify().recurse().getElementsByClass('Chord')
	for c in chords:
		d = roman.romanNumeralFromChord(c, key).scaleDegree
		if d < len(chord_freq):
			chord_freq[d] += 1
	return chord_freq
		

def get_note_freq(score, key):
	note_freq = [0, 0, 0, 0, 0, 0, 0, 0]
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



def ref_analyse_chord_freq(score):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	chords = score.chordify()
	for m in range(0, len(score.makeMeasures()) - 1):
		try:
			k = score.measure(m).analyze('key')
		except:
			continue
		for c in score.measure(m).chordify().recurse().getElementsByClass('Chord'):
			ma[roman.romanNumeralFromChord(c, k).scaleDegree] += k.tonalCertainty()
	return ma


def ref_analyse_composer_chord_freq(composer):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	scores = corpus.getComposer(composer)
	for s in scores[0:10]:
		add_lists(ma, ref_analyse_chord_freq(corpus.parse(s)))
	return ma


def ref_analyse_chord_trans_freq(score):
	ma = [[0 for i in range(8)] for o in range(8)]
	chords = score.chordify()
	for m in range(0, len(score.makeMeasures()) - 1):
		try:
			k = score.measure(m).analyze('key')
		except:
			continue
		mchords = score.measure(m).chordify().recurse().getElementsByClass('Chord')
		for c in range(0, len(mchords)-2):
			ca = roman.romanNumeralFromChord(mchords[c],k).scaleDegree 
			cb = roman.romanNumeralFromChord(mchords[c+1],k).scaleDegree 
			ma[ca][cb] += k.tonalCertainty()
	return ma


def ref_analyse_composer_chord_trans_freq(composer):
	ma = [[0 for i in range(8)] for o in range(8)]
	scores = corpus.getComposer(composer)
	for s in scores[0:10]:
		add_matrices(ma, ref_analyse_chord_trans_freq(corpus.parse(s)))
	return ma


def ref_analyse_melody_note_freq(path):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	f = abcFormat.ABCFile()
	f.open(path)
	try:
		ah = f.read()
	except:
		return ma
	ahDict = ah.splitByReferenceNumber()
	for i in ah.splitByReferenceNumber():
		k = None
		ahDict[i].tokenProcess()
		for t in ahDict[i].tokens:
			if type(t) == abcFormat.ABCMetadata and t.src[0] == 'K':
				k = t.getKeySignatureObject()
			elif type(t) == abcFormat.ABCNote:
				(n,_) = abcFormat.ABCNote().getPitchName(t.src)
				if (n):
					try:
						ma[roman.romanNumeralFromChord(chord.Chord([n]), k).scaleDegree] += 1
					except:
						continue
	return ma


def ref_analyse_composer_melody_note_freq(composer):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	scores = corpus.getComposer(composer)
	for s in scores[0:5]:
		add_lists(ma, ref_analyse_melody_note_freq(s))
	return ma


def ref_analyse_melody_note_trans_freq(path):
	ma = [[0 for i in range(8)] for o in range(8)]
	f = abcFormat.ABCFile()
	f.open(path)
	try:
		ah = f.read()
	except:
		return (ma, mi)
	ahDict = ah.splitByReferenceNumber()
	for i in ah.splitByReferenceNumber():
		ahDict[i].tokenProcess()
		for t in range(0, len(ahDict[i].tokens)-1):
			if type(ahDict[i].tokens[t+1]) == abcFormat.ABCMetadata and ahDict[i].tokens[t+1].src[0] == 'K':
				k = ahDict[i].tokens[t+1].getKeySignatureObject()
			elif type(ahDict[i].tokens[t+1]) == abcFormat.ABCNote and type(ahDict[i].tokens[t]) == abcFormat.ABCNote:
				(n2,_) = abcFormat.ABCNote().getPitchName(ahDict[i].tokens[t+1].src)
				(n1,_) = abcFormat.ABCNote().getPitchName(ahDict[i].tokens[t].src)
				if (n1 and n2):
					try:
						ma[roman.romanNumeralFromChord(chord.Chord([n1]), k).scaleDegree]\
						  [roman.romanNumeralFromChord(chord.Chord([n2]), k).scaleDegree] += 1
					except:
						continue
	return ma


def ref_analyse_composer_melody_note_trans_freq(composer):
	ma = [[0 for i in range(8)] for o in range(8)]
	scores = corpus.getComposer(composer)
	for s in scores[0:5]:
		add_matrices(ma, ref_analyse_melody_note_trans_freq(s))
	return ma


def get_list_difference(xs, ys):
	d = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in range(0, len(xs)):
		d[i] = round(abs(xs[i] - ys[i]))
	d[len(d)-2] = sum(d)
	d[len(d)-1] = round(sum(d) / len(d)-3)
	return d


def get_matrix_difference(xss, yss):
	ma = [[0 for i in range(8)] for o in range(8)]
	for m in range(0, len(ma)-1):
		for n in range(0, len(ma)-1):
			ma[m][n] = round(abs(xss[m][n] - yss[m][n]))
	return ma


def sum_matrix(xss):
	sum = 0
	for m in range(0, len(xss)-1):
		for n in range(0, len(xss[0])-1):
			sum += xss[m][n]
	return sum


def average_matrix(xss):
	sum = sum_matrix(xss)
	elements = len(xss) * len(xss[0])
	return sum / elements


#print("Getting reference chord frequencies")
#ref_chord_freq = ref_analyse_composer_chord_freq('bach')
#print("Getting reference melody note frequencies")
#ref_note_freq = ref_analyse_composer_melody_note_freq('essenFolksong')
#print("Getting reference chord transition frequencies")
#ref_chord_trans_freq = ref_analyse_composer_chord_trans_freq('bach')
print("Getting reference melody note transition frequencies")
ref_note_trans_freq = ref_analyse_composer_melody_note_trans_freq('essenFolksong')

print("Analysing my output")
key = key.Key('C')
my_chord_freq = [0, 0, 0, 0, 0, 0, 0, 0]
my_note_freq = [0, 0, 0, 0, 0, 0, 0, 0]
my_chord_trans_freq = [[0 for i in range(8)] for o in range(8)]
my_note_trans_freq = [[0 for i in range(8)] for o in range(8)]
path = '/home/rng/src/diss_eval'
dir = os.fsencode(path)
for file in os.listdir(dir):
	filename = os.fsdecode(file)
	if filename.endswith('.musicxml'):
		full_path = path + '/' + filename
		print(full_path)
		score = converter.parse(full_path)
		#add_lists(my_chord_freq, get_chord_freq(score, key))
		#add_lists(my_note_freq, get_note_freq(score, key))
		#add_matrices(my_chord_trans_freq, get_chord_trans_freq(score, key))
		add_matrices(my_note_trans_freq, get_note_trans_freq(score, key))

# fig = plt.figure()
# fig, axarr = plt.subplots(2,1)
# axarr[0].set_title("Chord frequency")
# normalise_list(my_chord_freq)
# normalise_list(ref_chord_freq)
# axarr[0].plot(my_chord_freq)
# axarr[0].plot(ref_chord_freq)
# axarr[0].legend(["our system", "Bach"])
# axarr[0].set_xlabel("chord degree")
# axarr[0].set_ylabel("frequency")
# axarr[1].axis('tight')
# axarr[1].axis('off')
# axarr[1].set_title("Difference between Bach and our system")
# collabel=("", "Chord I", "Chord II", "Chord III", "Chord IV", "Chord V", "Chord VI", "Chord VII", "Total", "Average")
# the_table = axarr[1].table(cellText=[get_list_difference(my_chord_freq, ref_chord_freq)], loc='best', colLabels=collabel)
# the_table.scale(1,4)
# the_table.set_fontsize(12)
# plt.tight_layout(pad=3)
# plt.savefig("out/chord_freq.png")
# plt.close()
# 
# fig = plt.figure()
# fig, axarr = plt.subplots(2,1)
# axarr[0].set_title("Melody note frequency")
# normalise_list(my_note_freq)
# normalise_list(ref_note_freq)
# axarr[0].plot(my_note_freq)
# axarr[0].plot(ref_note_freq)
# axarr[0].legend(["our system", "folk songs"])
# axarr[0].set_xlabel("note degree")
# axarr[0].set_ylabel("frequency")
# axarr[1].axis('tight')
# axarr[1].axis('off')
# axarr[1].set_title("Difference between folk songs and our system")
# collabel=("", "Note I", "Note II", "Note III", "Note IV", "Note V", "Note VI", "Note VII", "Total", "Average")
# the_table = axarr[1].table(cellText=[get_list_difference(my_note_freq, ref_note_freq)], loc='best', colLabels=collabel)
# the_table.scale(1,4)
# the_table.set_fontsize(12)
# plt.tight_layout(pad=3)
# plt.savefig("out/note_freq.png")
# plt.close()

# normalise_matrix(my_chord_trans_freq)
# normalise_matrix(ref_chord_trans_freq)
# fig = plt.figure()
# fig, axarr = plt.subplots(2, 2)
# fig.suptitle('Chord transition frequency comparison') 
# axarr[0, 0].matshow(my_chord_trans_freq)
# axarr[0, 0].set_title("Our system")
# axarr[0, 1].matshow(ref_chord_trans_freq)
# axarr[0, 1].set_title("Bach")
# collabel=("", "I", "II", "III", "IV", "V", "VI", "VII")
# axarr[1, 0].axis('tight')
# axarr[1, 0].axis('off')
# axarr[1, 0].set_title("% Difference between ours and Bach")
# diff = get_matrix_difference(my_chord_trans_freq, ref_chord_trans_freq)
# the_table = axarr[1, 0].table(cellText=diff, loc='best', colLabels=collabel, rowLabels=collabel)
# the_table.auto_set_font_size(False)
# the_table.set_fontsize(9)
# axarr[1, 1].axis('tight')
# axarr[1, 1].axis('off')
# axarr[1, 1].set_title("Total and average % difference")
# the_other_table = axarr[1, 1].table(cellText=[[sum_matrix(diff), round(average_matrix(diff))]], loc='best', colLabels=("Total", "Average"))
# fig.tight_layout()
# plt.savefig("out/chord_trans_freq.png")
# plt.close()

normalise_matrix(my_note_trans_freq)
normalise_matrix(ref_note_trans_freq)
fig = plt.figure()
fig, axarr = plt.subplots(2, 2)
fig.suptitle('Melody note transition frequency comparison') 
axarr[0, 0].matshow(my_note_trans_freq)
axarr[0, 0].set_title("Our system")
axarr[0, 1].matshow(ref_note_trans_freq)
axarr[0, 1].set_title("Folksongs")
collabel=("", "I", "II", "III", "IV", "V", "VI", "VII")
axarr[1, 0].axis('tight')
axarr[1, 0].axis('off')
axarr[1, 0].set_title("% Difference between ours and folksongs")
diff = get_matrix_difference(my_note_trans_freq, ref_note_trans_freq)
the_table = axarr[1, 0].table(cellText=diff, loc='best', colLabels=collabel, rowLabels=collabel)
the_table.auto_set_font_size(False)
the_table.set_fontsize(9)
axarr[1, 1].axis('tight')
axarr[1, 1].axis('off')
axarr[1, 1].set_title("Total and average % difference")
the_other_table = axarr[1, 1].table(cellText=[[sum_matrix(diff), round(average_matrix(diff))]], loc='best', colLabels=("Total", "Average"))
fig.tight_layout()
plt.savefig("out/melody_note_trans_freq.png")
plt.close()
