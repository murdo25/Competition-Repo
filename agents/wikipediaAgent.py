#uses top n verbs from Wikipedia as its verb list
#grabs objects from game text
#tries actions randomly

import agentBaseClass
import numpy as np
import time
import random as rand
import scholar.scholar as sch

class BruteForceAgent(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.scholar = sch.Scholar()
		self.verb_list=self.scholar.get_most_common_words('VB', 200)
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

		self.look_flag = 0
		self.last_state = ''
		self.current_state = ''
		self.last_action = ''
		self.verb_probabilities = np.ones(len(self.verb_list))
		self.object_probabilities = np.ones(len(self.object_list))
		self.num_states = 5000
		self.action_list = []

		#self.action_probabilities = np.ones(len(self.action_map[0]))
	
	def state_index(self, narrative):
		return abs(hash(narrative))%self.num_states


	def action(self, narrative):
		#time.sleep(1)
		if self.look_flag == 1:
			self.last_state = self.current_state
			self.look_flag = 0
			return "look"
		else:
			self.look_flag = 1
			self.current_state = narrative
			if self.current_state == self.last_state:
				#we didn't change state, so we don't
				#want to use that verb/object combo again
				print("No state change! Downsampling last action: " + self.last_action)
				self.action_map[self.state_index(narrative)][self.action_list.index(self.last_action)] = 0
				print(self.action_map[self.state_index(narrative)])
			else:
				print("STATE CHANGED!")
				print(self.last_state)
				print(self.current_state)
			#self.last_action = rand.choice(self.action_list)			
			action_probabilities = self.action_map[self.state_index(narrative)]
			try:
				self.last_action = np.random.choice(self.action_list, p=action_probabilities/np.sum(action_probabilities))
				return self.last_action.strip()
			except:
				return "look"

