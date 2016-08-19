from subprocess import Popen, PIPE, STDOUT
from random import randint
import binascii
import os, re

import agentBaseClass
import bruteForceAgent

def startZplet(jardir, gamedir):
    if(gamedir != ''):
        p = Popen(['java', '-jar', jardir, 'ieeecig.advent.IOAgent', gamedir], stdin=PIPE, stdout=PIPE)
    else:
        p = Popen(['java', '-jar', jardir, 'ieeecig.advent.IOAgent'], stdin=PIPE, stdout=PIPE)
    return (readNarrative(p),p)

def postCommand(p, command):
    print("Response: " + command)
    p.stdin.write(bytes(command + "\n", "ascii"))
    p.stdin.flush()
    return readNarrative(p)

def readNarrative(p):
    narrative=""
    cont = True
    while cont:
        for line in p.stdout:
            if(line.decode("utf-8").startswith("BREAK-NARRATIVE")):
                print("BREAK")
                cont = False
                break
            narrative = narrative + line.decode("utf-8") + "\n"
    return narrative

def action(narrative):
    print("Narrative: " + narrative)
    commands = ["n", "s", "e", "w", "verbose", "yes", "no", "IEEECIG-ADVENT-QUIT-COMMAND", "IEEECIG-ADVENT-RESTART-COMMAND", "IEEECIG-ADVENT-SOFT-RESTART-COMMAND"] 
    command = commands[randint(0,len(commands)-1)]
    if(len(command)%2==1):
        command = command + " "
    return command


total_steps_per_game = 10
_ = open('scores.txt', 'w').close()

list_of_games = os.listdir('../resources/')
for current_game in list_of_games:
	if current_game.endswith('z5'):
		print("Now playing: " + current_game)

		print("Booting Z Machine...")
		ret = startZplet('../Example Project/lib3rd/ieee-cig-advent-1.5.jar','../resources/' + current_game)
		narrative = ret[0]
		p = ret[1]
		print("Z Machine Launched")

		#a = agentBaseClass.AgentBaseClass()
		a = bruteForceAgent.BruteForceAgent()

		steps_per_game = 0
		current_score = 0
		while steps_per_game < total_steps_per_game:
			#command = action(narrative)
			print("Narrative: " + narrative)
			command = a.action(narrative)
			narrative = postCommand(p, command)
			steps_per_game += 1

			
			score_narrative = postCommand(p, command)
			score_pattern = '[0-9]+ [\(total ]*[points ]*[out ]*of [a maximum of ]*[a possible ]*[0-9]+'
			matchObj = re.search(score_pattern, score_narrative, re.M|re.I)
			if matchObj != None:
				score_words = matchObj.group().split(' ')
				current_score = int(score_words[0]), int(score_words[len(score_words)-1])

			scores_output_file = open('scores.txt', 'a')
			scores_output_file.write(current_game + '\t' + str(steps_per_game) + '\t' + str(current_score) + '\n')
			scores_output_file.close()

