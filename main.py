from music21 import *
import numpy as np
import matplotlib.pyplot as plt

def analyse_chord_freq(score):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	mi = [0, 0, 0, 0, 0, 0, 0, 0]
	chords = score.chordify()
	for m in range(0, len(score.makeMeasures()) - 1):
		try:
			k = score.measure(m).analyze('key')
		except:
			continue
		for c in score.measure(m).chordify().recurse().getElementsByClass('Chord'):
			if k.mode == "major":
				ma[roman.romanNumeralFromChord(c, k).scaleDegree] += k.tonalCertainty()
			elif k.mode == "minor":
				mi[roman.romanNumeralFromChord(c, k).scaleDegree] += k.tonalCertainty()
			else:
				print(k.mode)
	return (ma,mi)

def analyse_chord_trans_freq(score):
	ma = [[0 for i in range(8)] for o in range(8)]
	mi = [[0 for i in range(8)] for o in range(8)]
	chords = score.chordify()
	#for m in range(0, len(score[3]) - 1):
	for m in range(0, len(score.makeMeasures()) - 1):
		try:
			k = score.measure(m).analyze('key')
		except:
			continue
		mchords = score.measure(m).chordify().recurse().getElementsByClass('Chord')
		for c in range(0, len(mchords)-2):
			ca = roman.romanNumeralFromChord(mchords[c],k).scaleDegree 
			cb = roman.romanNumeralFromChord(mchords[c+1],k).scaleDegree 
			if k.mode == "major":
				ma[ca][cb] += k.tonalCertainty()
			elif k.mode == "minor":
				mi[ca][cb] += k.tonalCertainty()
			else:
				print("umm...")
	return (ma,mi)


def analyse_composer_chord_freq(composer):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	mi = [0, 0, 0, 0, 0, 0, 0, 0]
	scores = corpus.getComposer(composer)
	print(len(scores))
	for s in scores[0:10]:
		print(s)
		(ma_tmp, mi_tmp) = analyse_chord_freq(corpus.parse(s))
		for i in range(1, 7):
			ma[i] += ma_tmp[i]
			mi[i] += mi_tmp[i]
	ma_chords = sum(ma)
	mi_chords = sum(mi)
	for i in range(1,7):
		if (ma_chords > 0):
			ma[i] = (ma[i] / ma_chords) * 100
		if (mi_chords > 0):
			mi[i] = (mi[i] / mi_chords) * 100
	return (ma,mi)


def analyse_composer_chord_trans_freq(composer):
	ma = [[0 for i in range(8)] for o in range(8)]
	mi = [[0 for i in range(8)] for o in range(8)]
	scores = corpus.getComposer(composer)
	print(len(scores))
	for s in scores[0:10]:
		print(s)
		(ma_tmp, mi_tmp) = analyse_chord_trans_freq(corpus.parse(s))
		for m in range(1, 7):
			for n in range(1, 7):
				ma[m][n] += ma_tmp[m][n]
				mi[m][n] += mi_tmp[m][n]
	return (ma, mi)


def analyse_abc_note_freq(path):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	mi = [0, 0, 0, 0, 0, 0, 0, 0]
	f = abcFormat.ABCFile()
	f.open(path)
	try:
		ah = f.read()
	except:
		return (ma, mi)
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
						if k.mode == "major":
							ma[roman.romanNumeralFromChord(chord.Chord([n]), k).scaleDegree] += 1
						elif k.mode == "minor":
							mi[roman.romanNumeralFromChord(chord.Chord([n]), k).scaleDegree] += 1
						else:
							print("modal")
							input()
					except:
						continue
	return (ma, mi)


def analyse_abc_composer_chord_freq(composer):
	ma = [0, 0, 0, 0, 0, 0, 0, 0]
	mi = [0, 0, 0, 0, 0, 0, 0, 0]
	scores = corpus.getComposer(composer)
	for s in scores[0:5]:
		(ma_tmp, mi_tmp) = analyse_abc_note_freq(s)
		for m in range(1, 7):
			ma[m] += ma_tmp[m]
			mi[m] += mi_tmp[m]
	return (ma, mi)


def analyse_abc_chord_trans_freq(path):
	ma = [[0 for i in range(8)] for o in range(8)]
	mi = [[0 for i in range(8)] for o in range(8)]
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
						if k.mode == "major":
							ma[roman.romanNumeralFromChord(chord.Chord([n1]), k).scaleDegree]\
							  [roman.romanNumeralFromChord(chord.Chord([n2]), k).scaleDegree] += 1
						elif k.mode == "minor":
							mi[roman.romanNumeralFromChord(chord.Chord([n1]), k).scaleDegree]\
							  [roman.romanNumeralFromChord(chord.Chord([n2]), k).scaleDegree] += 1
						else:
							print("modal")
							input()
					except:
						continue
	return (ma, mi)


def analyse_abc_composer_chord_trans_freq(composer):
	ma = [[0 for i in range(8)] for o in range(8)]
	mi = [[0 for i in range(8)] for o in range(8)]
	scores = corpus.getComposer(composer)
	print(len(scores))
	for s in scores[0:5]:
		print(s)
		(ma_tmp, mi_tmp) = analyse_abc_chord_trans_freq(s)
		for m in range(1, 7):
			for n in range(1, 7):
				ma[m][n] += ma_tmp[m][n]
				mi[m][n] += mi_tmp[m][n]
	return (ma, mi)


def plot_degree_freq(ma, mi):
	print(ma)
	print(mi)
	plt.plot(ma)
	plt.plot(mi)
	plt.legend(['major','minor'])
	plt.xlabel('degree')
	plt.ylabel('percent')
	plt.show()


# bach chord frequency analysis
#(ma,mi) = analyse_composer_chord_freq('bach')
#(ma,mi) = analyse_composer_chord_freq('essenFolksong')
#plot_degree_freq(ma, mi)


# chord transition frequency analysis
#(ma, mi) = analyse_composer_chord_trans_freq('bach')
#plt.matshow(ma)
#plt.show()


# folk song chord frequency analysis
#(ma, mi) = analyse_abc_composer_chord_freq('essenFolksong')
#plt.plot(ma)
#plt.plot(mi)
#plt.show()


# folk song chord transition frequency analysis
(ma, mi) = analyse_abc_composer_chord_trans_freq('essenFolksong')
plt.matshow(ma)
plt.show()
