from subprocess import Popen, PIPE, STDOUT
from random import randint
import binascii
import time

import agentBaseClass
import bruteForceAgent
import wikipediaAgent
import packratAgent
import wikipediaPlus
import ultimateAgent

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

#a = agentBaseClass.AgentBaseClass()
#a = bruteForceAgent.BruteForceAgent()
#a = wikipediaAgent.WikipediaAgent()
#a = packratAgent.PackRatAgent()
#a = wikipediaPlus.WikipediaPlus()
a = ultimateAgent.UltimateAgent()
#print("Implementing agent ") + type(a)

print("Booting Z Machine...")
ret = startZplet('../Example Project/lib3rd/ieee-cig-advent-1.5.jar','../resources/monkey-and-bananas-v1.z8')
#ret = startZplet('../Example Project/lib3rd/ieee-cig-advent-1.5.jar','../resources/monkey-and-bananas-v1.z8')
#ret = startZplet('../Example Project/lib3rd/ieee-cig-advent-1.5.jar','../resources/lily.z5')
narrative = ret[0]
p = ret[1]
print("Z Machine Launched")

count = 0
while True:
    #command = action(narrative)
#    count = count + 1
#    if count > 100:
#        count = 0
#        input("pause")
#    Sleep(500)
    print("Narrative: " + narrative)
    command = a.action(narrative)
    narrative = postCommand(p, command)

