#uses hand-picked verbs - tries to acquire things, open things, unlock things
#selects objects from game text and inventory

import agentBaseClass
import numpy as np
import time
import random as rand
import nltk

class PackRatAgent(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.verb_list=['get', 'drop', 'open', 'unlock', 'climb', 'descend', 'enter', 'exit', 'attack', 'up', 'down', 'north', 'south', 'east', 'west', 'northwest', 'southwest', 'northeast', 'southeast', '']
		self.verb_probabilities=[10, 10, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		self.verb_probabilities=self.verb_probabilities/np.sum(self.verb_probabilities)

		self.num_states = 5000
		self.last_state = ''
		self.current_state = ''
		self.last_action = ''
		self.inventory_list = []
		self.TWO_WORD_OBJECTS = True
		self.inventory_count = 0
		self.look_flag = 0

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

		try:
			self.last_action = np.random.choice(self.verb_list, p=self.verb_probabilities) + " " + rand.choice(objects)
			print ("Action is " + self.last_action.strip()) 				
			return self.last_action.strip()
		except:
			return "look"

