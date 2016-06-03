#python reading list

import os
import pyttsx
import codecs
from collections import defaultdict
import data_analyzer
__author__='Eileen Cho'

read_list = []
answer = defaultdict(str)

f = open('practicelist.txt','r')
for line in f:
	read_list.append(line.rstrip())

engine = pyttsx.init()
engine.setProperty('rate',120)
y = 'y'
n = 'n'
for w in read_list:
	engine.say(w)
	engine.runAndWait()
	ans = input('Answer y or n: ')
	answer[w]= ans

print answer