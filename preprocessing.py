from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize

def process_text(file_name):
	with open(file_name) as data_file:
		lines = data_file.readlines()

	poem_lines = []

	for i in range(len(lines)):
		if lines[i][0:3] != '   ' and lines[i] != '\n':
			poem_lines.append(lines[i].strip())

	return poem_lines
