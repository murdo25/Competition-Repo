#uses top n verbs from Wikipedia as its verb list (some hand optimization included)
#grabs objects from game text and inventory
#looks for verbs that match objects using one of:
#	w2v analogies
#	wikipedia co-occurance counts
#	verbFinder dependency counts
#seeks a verb that:
#	(A) satisfies the above search criteria
#	(B) is in the agent's verb list
#	(C) has not been tried with that object before
#remembers which verb/object combos produced reward/state changes using one of
#	simple counts
#	Qvalues

import agentBaseClass
import numpy as np
import time
import random as rand
import scholar.scholar as sch
import nltk
import verbFinder

class UltimateAgent(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.scholar = sch.Scholar()
		#self.verb_list=self.scholar.get_most_common_words('VB', 200)
		self.verb_list = ['throw', 'spray', 'stab', 'slay', 'open', 'pierce', 'thrust', 'exorcise', 'place', 'jump', 'take', 'make', 'read', 'strangle', 'swallow', 'slide', 'wave', 'look', 'dig', 'pull', 'put', 'rub', 'fight', 'ask', 'score', 'apply', 'take', 'knock', 'block', 'kick', 'step', 'break', 'wind', 'blow', 'crack', 'drop', 'blast', 'leave', 'yell', 'skip', 'stare', 'hurl', 'hit', 'kill', 'glass', 'engrave', 'bottle', 'pour', 'feed', 'hatch', 'swim', 'spray', 'melt', 'cross', 'insert', 'lean', 'sit', 'move', 'fasten', 'play', 'drink', 'climb', 'walk', 'consume', 'kiss', 'startle', 'shout', 'close', 'cast', 'set', 'drive', 'lift', 'strike', 'startle', 'catch', 'board', 'speak', 'think', 'get', 'answer', 'tell', 'feel', 'get', 'turn', 'listen', 'read', 'watch', 'wash', 'purchase', 'do', 'sleep', 'fasten', 'drag', 'swing', 'empty', 'switch', 'slip', 'twist', 'shoot', 'slice', 'read', 'burn', 'hop']
		self.verb_list += ['wait', 'point', 'light', 'unlight']
	
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
		self.last_verb = ''
		self.last_object = ''
		self.last_action = 'look'
		self.inventory_list = []
		self.TWO_WORD_OBJECTS = True
		self.inventory_count = 0
		self.look_flag = 0
		self.exploration_counts = {}

		#self.corpus_name = "corpora/Wikipedia_first_100000_lines.txt"
		self.corpus_name = "corpora/classic_books.txt"
		self.totalCount = {}
		for v in self.verb_list:
			self.totalCount[v] = 0.0
		f = open(self.corpus_name)
		for line in f:
			for v in self.verb_list:				
				if v in line:
					self.totalCount[v] = self.totalCount[v] + 1
		f.close()

		#self.verbFiner = verbFinder.verbFinder()

		self.alreadyTried = {}
		self.success = {}


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

	def get_wikipedia_verbs(self, obj, n):
		#returns the n most-commonly-co-occurring verbs from the 
		#wikipedia corpus (give or take a few)

		count = {}
		for v in self.verb_list:
			count[v] = 0.0

		f = open(self.corpus_name)
		for line in f:
			if obj in line:
				for v in self.verb_list:
					if v in line:
						count[v] = count[v] + 1
		f.close()
		
		for v in self.verb_list:
			count[v] = count[v]/self.totalCount[v]

		max_verbs = []


#		print("WIKIPEDIA_VERBS")
#		print("Object is " + obj)
#		for v in self.verb_list:
#			print(v + " " + str(count[v]))
#		input("pause")
		
		while len(max_verbs) < n:
			for v in max_verbs:
				count[v] = -1
			max_val = max(count.values())
			max_verbs = max_verbs + [k for k in count if count[k] == max_val]
		
		return max_verbs

	def getVerb(self, game_text, input_object):
		#returns a verb that:
		# (A) satisfies the active search criterion
		# (B) is in the agent's verb_list
		# (C) has not already been tried in this state with this object	

		obj = input_object
		if len(input_object.split()) > 1:
			obj = input_object.split()[-1]

		obj = obj.lower()

		#matching_verbs = self.verbFinder.verbsForWord(obj, 100)
		
		matching_verbs = self.scholar.get_verbs(obj, 100)
		for i in range(len(matching_verbs)):
			matching_verbs[i] = matching_verbs[i][:-3] 

		#matching_verbs = self.get_wikipedia_verbs(obj, 10)
		
		tryList = []

		for v in matching_verbs:
			if v in self.verb_list:
				if self.alreadyTried[game_text][input_object][v] == 0:
					tryList.append(v)

		if len(tryList) == 0:
			if obj not in self.success[game_text].keys():
				self.success[game_text][obj] = {}
				for v in self.verb_list:
					self.success[game_text][obj][v] = 0.0
			tryList = list(self.success[game_text][obj].keys())

		if len(tryList) == 0:
			tryList = self.verb_list

#		print("GETVERB:")
		print("Active object is " + obj)
		print("Here are the verbs returned by Scholar:")
		print(matching_verbs)
		print("I will select randomly from one of these verbs:")
		print(tryList)
#		input("pause")

		vrb = rand.choice(tryList)
		return vrb

	def chooseAction(self, game_text):

		objects = self.find_objects(game_text) + self.inventory_list + ['']
		obj = rand.choice(objects)

		#if this is a new state or object, then
		#initialize the proper dictionary keys
		if game_text not in self.alreadyTried.keys():
			self.alreadyTried[game_text] = {}

		if obj not in self.alreadyTried[game_text].keys():
			self.alreadyTried[game_text][obj] = {}
			for v in self.verb_list:
				self.alreadyTried[game_text][obj][v] = 0

		if game_text not in self.success.keys():
			self.success[game_text] = {}

		if obj not in self.success[game_text].keys():
			self.success[game_text][obj] = {}
			for v in self.verb_list:
				self.success[game_text][obj][v] = 0

#		print("CHOOSEACTiON")
#		print("object list is ")
#		print(objects)
#		print(obj)
#		print(self.alreadyTried[game_text][obj])
#		print(self.success[game_text])
#		input("pause")
		
		#check to see whether the last action was successful
		if self.last_state != self.current_state:
#			print("STATE CHANGE: " + self.last_state + " --> " + self.current_state)
#			print("Updating self.success[" + self.last_state + "][" + self.last_object + "][" + self.last_verb +"]")
			if self.last_state not in self.success.keys():
				self.success[self.last_state] = {}
			if self.last_object not in self.success[self.last_state].keys():
				self.success[self.last_state][self.last_object] = {}
				for v in self.verb_list:
					self.success[self.last_state][self.last_object][v] = 0
			self.success[self.last_state][self.last_object][self.last_verb] = 1
#		else:
#			print("No state change: " + self.current_state)
#		print(self.success[self.last_state])
#		input("pause")
		
		#choose the next action
		vrb = self.getVerb(game_text, obj)		
		self.alreadyTried[game_text][obj][vrb] = 1
		self.last_verb = vrb
		self.last_object = obj
		return vrb + ' ' + obj

	def action(self, narrative):
		if self.last_action == "inventory":
			self.inventory_list = self.find_objects(narrative)
		elif self.last_action == "look":
			self.last_state = self.current_state
			self.current_state = narrative	
			
		if self.look_flag == 1:
			self.look_flag = 0
			self.last_action = "look"
			return "look"
		
		if self.inventory_count == 5:
			self.inventory_count = 0
			self.last_action = "inventory"
			return "inventory"
		
		#update flags	
		self.look_flag = 1
		self.inventory_count = self.inventory_count + 1
		
		#select an action
		self.last_action = self.chooseAction(self.current_state)
#		print ("Game text is " + narrative) 
#		print ("State is " + self.current_state) 
#		print ("Inventory is ")
#		print (self.inventory_list)
		print ("Action is " + self.last_action.strip()) 
#		input("pause")				
		return self.last_action.strip()

