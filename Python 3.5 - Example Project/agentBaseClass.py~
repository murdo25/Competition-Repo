#An agent that executes actions randomly

import random as rand
import time

class AgentBaseClass:

	def __init__(self):
		self.verb_list = ['n', 's', 'e', 'w', 'up', 'down', 'get', 'drop', 'climb on', 'wave', 'eat']
		self.object_list = ['', 'chair', 'stick', 'banana']

	def action(self, narrative):
		time.sleep(0.5)		
		command = rand.choice(self.verb_list) + " " + rand.choice(self.object_list)
		return command.strip()
