#An agent that executes actions randomly

import random as rand
import time

class AgentBaseClass:

	def __init__(self):
		self.verb_list = ['n', 's', 'e', 'w', 'up', 'down', 'get', 'drop', 'climb on', 'wave', 'eat']
		self.object_list = ['', 'chair', 'stick', 'banana']
		# mod by ben for the additional prepositions
		self.preposition_list = ['with', 'in', 'at', 'above', 'under']

	def action(self, narrative):
		time.sleep(0.5)		
		command = rand.choice(self.verb_list) + " " + rand.choice(self.object_list)
		return command.strip()
		
	#Verb Noun Prep Noun	
	def getVNPN(self):
		sents = []
		
		for v in self.verb_list:
			for n in self.object_list:
				for p in self.prep_list:
					for n2 in self.object_list:
						sentence = "{} {} {} {}".format(v, n, p, n2)
						sents.append(sentence)
		
		#for each string, check against vector matrix and delete bad strings

		return sents
		
		#Verb Prep Noun	
	def getVPN(self):
		sents = []
		
		for v in self.verb_list:
			for p in self.prep_list:
				for n in self.object_list:
						sentence = "{} {} {}".format(v, p, n)
						sents.append(sentence)
		
		#for each string, check against vector matrix and delete bad strings

		return sents
