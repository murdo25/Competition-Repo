#Tracks which actions have been tried in which state.
#Any action that failed to produce a state change is rejected

import agentBaseClass
import numpy as np
import time
import random as rand

class BrutePrepAgent(agentBaseClass.AgentBaseClass):


	def __init__(self):
		self.verb_list = ['n', 's', 'e', 'w', 'up', 'down', 'get', 'drop', 'climb on', 'wave', 'eat', 'break', 'hit']
		self.verb_indx = 0
		self.object_list = ['', 'chair', 'stick', 'banana']
		self.object_indx = 0
		self.object_indx2 = 0
		self.prep_list = ['on', 'in', 'by', 'next to', 'with', 'to']
		self.prep_indx = 0
		self.look_flag = 0
		self.last_state = ''
		self.current_state = ''
		self.last_action = ''
		self.verb_probabilities = np.ones(len(self.verb_list))
		self.object_probabilities = np.ones(len(self.object_list))
		self.num_states = 5000
		self.action_list = []
		for v in self.verb_list:
			for o in self.object_list:
				self.action_list.append(v + " " + o)
		self.action_map = np.ones((self.num_states, len(self.action_list))) #action probabilities
										    #for each state
		
		#self.action_probabilities = np.ones(len(self.action_map[0]))
	
	def state_index(self, narrative):
		return abs(hash(narrative))%self.num_states
		
	#Return Verb
	def getVerb():
		if len(self.verb_list) > (self.verb_indx +1):
			Vrb = self.verb_list[self.verb_indx]
			self.verb_indx += 1
		else:
			Vrb = self.verb_list[len(self.verb_list) - 1]
			self.verb_indx = 0
			# increse the next sets indx by 1
			#if (self.object_indx +1) < len(self.object_list):
			self.object_indx += 1
			
		return Vrb
		
	#Return Noun 1	
	def getNoun():
		if len(self.object_list) > (1 + self.object_indx):
			N1 = self.object_list[self.object_indx]
			
		else:
			N1 = self.object_list[len(self.object_list) -1]
			self.object_indx = 0
			# increse the next sets indx by 1
			#if (self.prep_indx +1) < len(self.prep_list):
			self.prep_indx += 1
		
		return N1
		
		
	#Return Preposition	
	def getPrep():
		if len(self.prep_list) > (1 + self.prep_indx):
			P = self.prep_list[self.prep_indx]
		
		else:
			P = self.prep_list[len(self.prep_list) -1]
			self.prep_indx = 0	
			#if (self.object_indx2 + 1) < len(self.object_list):
			self.object_indx2 += 1
		
		return P
		
		
	#Return Noun 2	
	def getNoun2():
		if len(self.object_list) > (1 + self.object_indx2):
			N2 = self.object_list[self.object_indx2]
			
		else:
			#KILL EVERYTHING, YOU'VE GONE THROUGH EVERY COMBO
			
		return N2
		
		
		
		
		
		
	#Verb Noun Prep Noun	
	def getVNPN(self):
	
		V = getVerb()
		N = getNoun()
		P = getPrep()
		N2 = getNoun2()
		
		move = (V + ' ' + N + ' ' + P + ' ' + N2)
		# if checkBleu(move) != true  than try again    //Add later
		return move



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




