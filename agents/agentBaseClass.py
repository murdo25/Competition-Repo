#An agent that executes actions randomly

import random as rand
import time

class AgentBaseClass:

	def __init__(self):
		self.verb_list = ['n', 's', 'e', 'w', 'up', 'down', 'get', 'drop', 'climb on', 'wave', 'eat']
		self.object_list = ['', 'chair', 'stick', 'banana']
		
		#mod by ben for the additional prepositions
		self.preposition_list = ['with', 'in', 'at', 'above', 'under']
		#Verb and Preposition Dictionary
		self.VPD = {}


	def action(self, narrative):
		time.sleep(0.5)		
		command = rand.choice(self.verb_list) + " " + rand.choice(self.object_list)
		return command.strip()
		
	#Verb Noun Prep Noun, return list	
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
	
        #look in box
        #
	#Verb Prep Noun, return list	
	def getVPN(self):
		sents = []
		
		for v in self.verb_list:
			for p in self.prep_list:
				for n in self.object_list:
						sentence = "{} {} {}".format(v, p, n)
						sents.append(sentence)
		
		#for each string, check against vector matrix and delete bad strings

		return sents

	#fill a dictionary with a <str,set> combo
	def updatePrepositionDictionary(self,verb,prepSet):
		self.VPD[verb] = prepSet
		pass
	
	#using the dictionary, return a list of commands
	def getCommands(self):
	
		sents = []
		#Verb
		for v in self.verb_list:
			#Noun
			for obj in self.object_list:
				#Dictionary of prepositions according to verbs
				for key in VPD.keys:
					#set or list of prepositions
					for prep in VPD[key]:
						#second Noun
						for obj2 in self.object_list:
							sentence = "{} {} {} {}". format(v, obj, prep, obj2)
							sents.append(sentence)
		
		return sents
							
	
							
							
							
							
							
							
							
							
							
							
							
