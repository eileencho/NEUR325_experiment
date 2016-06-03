#Randomly generate sequence to assign nap/wake conditions for subjects.

import os
#Simport pyttsx
import codecs
import random


f = open('sequence.txt','w')
wakecounter = 0
sleepcounter = 0
for i in range(100):
	print 'at ', i
	a=random.randrange(0,2)
	condition = ''
	if a==0:
		condition = 'nap'
		sleepcounter +=1
	else:
		condition = 'wake'
		wakecounter +=1
	string ='subject '+str(i)+' condition: ' + condition + ' wakecounter: ' + str(wakecounter)+ ' sleepcounter: ' + str(sleepcounter) + '\n'
	f.write(string)
