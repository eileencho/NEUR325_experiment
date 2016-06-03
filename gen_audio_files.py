#google text to speech module create audio files from list

import os
import codecs
from gtts import gTTS

read_list = []
f = open('list.txt','r')
for line in f:
	read_list.append(line.rstrip())


for w in read_list:
	print "saving %s..."%w 
	tts = gTTS(text=w,lang='en')
	filename = w+'.ogg'
	tts.save(os.path.join('audio_files',filename))
print "Done generating audio files"


