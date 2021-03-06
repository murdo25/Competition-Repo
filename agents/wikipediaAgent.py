#uses top n verbs from Wikipedia as its verb list
#grabs objects from game text and inventory
#tries actions randomly

import agentBaseClass
import numpy as np
import time
import random as rand
import scholar.scholar as sch
import nltk

class WikipediaAgent(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.scholar = sch.Scholar()
		self.verb_list=self.scholar.get_most_common_words('VB', 200)

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
		#self.verb_probabilities = np.ones(len(self.verb_list))
		#self.object_probabilities = np.ones(len(self.object_list))
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
			self.last_action = rand.choice(self.verb_list) + " " + rand.choice(objects)
			print ("Action is " + self.last_action.strip()) 				
			return self.last_action.strip()
		except:
			return "look"

