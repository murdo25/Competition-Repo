
import numpy as np
import random as rand

class verbFinder:

	def __init__(self, inputFile = "parseyText.txt"):
		self.verbs = {}
		self.nouns = {}
		self.adjectives = {}
		
		self.list = []
		f = open(inputFile)
		for line in f:
			self.list.append(line.split())

		self.parse()

	def verbsForNoun(self, noun):
		print(self.nouns[noun])

	def verbsForAdj(self, adj):
		print(self.adjectives[adj])

	def wordsForVerb(self, verb):
		print(self.verbs[verb])

	def numDependencies(self, verb, word):
		print(self.verbs[verb][word])	

	def print(self):
		for i in range(len(self.list)):
			print(self.list[i])

	def inc_verb(self, verb, word):
		if verb not in self.verbs:
			self.verbs[verb] = {}
		if word not in self.verbs[verb]:
			self.verbs[verb][word] = 0
		self.verbs[verb][word] += 1

	def inc_noun(self, noun, verb):
		if noun not in self.nouns:
			self.nouns[noun] = {}
		if verb not in self.nouns[noun]:
			self.nouns[noun][verb] = 0
		self.nouns[noun][verb] += 1

	def inc_adj(self, adj, verb):
		if adj not in self.adjectives:
			self.adjectives[adj] = {}
		if verb not in self.adjectives[adj]:
			self.adjectives[adj][verb] = 0
		self.adjectives[adj][verb] += 1

	def parse(self):
		sentence = []
		for i in range(len(self.list)):
			if len(self.list[i]) == 0:
				for w1 in sentence:
					#find all words with a verb as the parent
					if w1['type'] == 'VERB':
						for w2 in sentence:
							if w2['parent'] == w1['index'] and w2['type'] != 'VERB':
								self.inc_verb(w1['text'], w2['text'])			
								if w2['type'] == 'NOUN':
									self.inc_noun(w2['text'], w1['text'])			
								if w2['type'] == 'ADJ':
									self.inc_adj(w2['text'], w1['text'],)			

				#	print(w1)
				#print(self.verbs)
				#input('pause')
				sentence = [] #beginning of new sentence
			else:
				word = {}
				word['index'] = self.list[i][0]
				word['text'] = self.list[i][1]
				word['type'] = self.list[i][3]
				word['parent'] = self.list[i][6]
				if word['type'] == 'NOUN' or word['type'] == 'VERB' or word['type'] == 'ADJ':
					sentence.append(word)

			
