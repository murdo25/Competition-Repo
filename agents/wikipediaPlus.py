#uses top n verbs from Wikipedia as its verb list
#prioritizes them based on co-occurrence with relevant nouns
#grabs objects from game text and inventory
#uses count-based exploration

import agentBaseClass
import numpy as np
import time
import random as rand
import scholar.scholar as sch
import nltk

class WikipediaPlus(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.scholar = sch.Scholar()
		self.verb_list=self.scholar.get_most_common_words('VB', 200)
		#self.verb_list = ['get', 'drop', 'up', 'down']

		if 'save' in self.verb_list:
			self.verb_list.remove('save') #to prevent agent from trying to save the game...		
		if 'quit' in self.verb_list:
			self.verb_list.remove('quit') #to prevent agent from trying to quit the game...		
		if 'restart' in self.verb_list:
			self.verb_list.remove('restart') #to prevent agent from trying to restart the game...		

		self.verb_list.append('north')
		self.verb_list.append('south')
		self.verb_list.append('west')
		self.verb_list.append('east')
		self.verb_list.append('northwest')
		self.verb_list.append('southwest')
		self.verb_list.append('northeast')
		self.verb_list.append('southeast')
		self.verb_list.append('up')
		self.verb_list.append('down')
		self.verb_list.append('')
	

		self.num_states = 5000
		self.last_state = ''
		self.current_state = ''
		self.last_action = ''
		self.inventory_list = []
		self.TWO_WORD_OBJECTS = True
		self.inventory_count = 0
		self.look_flag = 0
		self.exploration_counts = {}

		self.corpus_name = "corpora/Wikipedia_first_100000_lines.txt"
		#self.corpus_name = "corpora/classic_books.txt"
		self.totalCount = {}
		for v in self.verb_list:
			self.totalCount[v] = 0.0
		f = open(self.corpus_name)
		for line in f:
			for v in self.verb_list:				
				if v in line:
					self.totalCount[v] = self.totalCount[v] + 1
		f.close()



	def state_index(self, narrative):
		return abs(hash(narrative))%self.num_states

	def find_objects(self, narrative):
		#assumes an object is mutable if it appears as a noun in the game text
		tokens = nltk.word_tokenize(narrative)
		tags = nltk.pos_tag(tokens)
		nouns = [word for word,pos in tags if word.isalnum() and (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]

		if self.TWO_WORD_OBJECTS == True:
			tokens = nltk.word_tokenize(narrative)
			tags = nltk.pos_tag(tokens)
			for i in range(0, len(tags) - 1):
				if (tags[i][1] == "JJ") and (tags[i+1][1] in ["NN", "NNP", "NNS", "NNPS"]):
					nouns.append(tags[i][0] + " " + tags[i+1][0])

		return nouns


	def bestMatch(self, input_object, verb_list):
		#returns the verb that occurs most often in conjunction with the obj
		#(using a Wikipedia corpus to accumulate counts)

		obj = input_object
		if len(input_object.split()) > 1:
			obj = input_object.split()[-1]

		count = {}
		for v in verb_list:
			count[v] = 0.0

		f = open(self.corpus_name)
		for line in f:
			if obj in line:
				for v in verb_list:
					if v in line:
						count[v] = count[v] + 1
		f.close()

#		print("Co-occurance counts for object " + obj)
#		print(count)
#		input("pause")

#		print("total counts" + obj)
#		print(self.totalCount)
#		input("pause")

		#scale counts by frequency of verb in corpus
		for v in self.verb_list:
			try:
				count[v] = count[v]/self.totalCount[v]
			except:
				count[v] = 0

#		print("co-occurance ratios" + obj)
#		print(count)
#		input("pause")

		max_val = max(count.values())
		max_verbs = [k for k in count if count[k] == max_val]

#		print ("Best match:")
#		print(max_verbs)
#		input("pause")
		return rand.choice(max_verbs)

	def chooseAction(self, narrative, objects):
		#select a random object
		#later, we may prioritize objects or explore the idea of 'boredom'
		#or insert an 'active object' that is the focus of the agent's attention for a while
		obj = rand.choice(objects)

		#if this is a new state or object, then
		#initialize the proper dictionary keys
		if narrative not in self.exploration_counts.keys():
			self.exploration_counts[narrative] = {obj:{}}
			for v in self.verb_list:
				self.exploration_counts[narrative][obj][v] = 0

		if obj not in self.exploration_counts[narrative].keys():
			self.exploration_counts[narrative][obj] = {}
			for v in self.verb_list:
				self.exploration_counts[narrative][obj][v] = 0

		
#		print("Current exploration counts for object " + obj + " and state: " + narrative)
#		print(self.exploration_counts[narrative][obj])
#		input("pause")

		#select all verbs with lowest count
		min_val = min(self.exploration_counts[narrative][obj].values())
		min_verbs = [k for k in self.exploration_counts[narrative][obj] if self.exploration_counts[narrative][obj][k] == min_val]
#		print("Verbs with the lowest exploration counts:")
#		print(min_verbs)
#		input("pause")	

		#of those verbs, select the one that co-occurs 
		#most often with the object in Wikipedia
		#that's our action
		#vrb = rand.choice(min_verbs)
		vrb = self.bestMatch(obj, min_verbs)		

		#update counts and return the action
		self.exploration_counts[narrative][obj][vrb] = self.exploration_counts[narrative][obj][vrb] + 1
		return vrb + ' ' + obj

	def action(self, narrative):
		#time.sleep(1)
		if self.last_action == "inventory":
			self.inventory_list = self.find_objects(narrative)
		else:
			if self.look_flag == 1:
				self.last_state = self.current_state
				self.look_flag = 0
				return "look"
		
			if self.inventory_count == 5:
				self.inventory_count = 0
				self.last_action = "inventory"
				return "inventory"
		
		#update flags	
		self.look_flag = 1
		self.inventory_count = self.inventory_count + 1
		self.last_state = self.current_state
		self.current_state = narrative
		
		#select an action
		objects = self.find_objects(narrative) + self.inventory_list + ['']

		self.last_action = self.chooseAction(narrative, objects)
		print ("Action is " + self.last_action.strip()) 				
		return self.last_action.strip()

