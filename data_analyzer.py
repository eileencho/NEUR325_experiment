import os
import csv
import codecs
from collections import defaultdict
import argparse
__author__='Eileen Cho'

#read in answer keys
#depending on the typdict param, returns a dict mapping words to response or category
def ansKey(filename,typedict):
	f=open(filename)
	reader = csv.reader(f)
	returnAns = defaultdict(str)
	for row in reader:
		k = row[1]
		if typedict=="cat":
			v = row[2] #category
		else:
			v = row[0] #response y/n
		returnAns[k] = v
	f.close()
	return returnAns

#read in data and returns three dictionaries
#cResponse maps question number to response given
#pResponse maps practice words to correct or incorrect value
#exResponse maps experimental words to correct or incorrect value
def dataReader(filename):
	f=open(filename)
	reader = csv.reader(f)
	headers = reader.next()
	correctIndex = headers.index('correct')
	wordIndex = headers.index('target')
	formIndex = headers.index('form_response')

	exResponse = defaultdict(int)
	pResponse = defaultdict(int)
	cResponse = defaultdict(str)

	for index, row in enumerate(reader):
		if index<4: #looking at content questions
			cResponse[index+1] = row[formIndex]
		elif index in range(4,10): #looking at practice questions
			pResponse[row[wordIndex]] = int(row[correctIndex])
		else:
			exResponse[row[wordIndex]] = int(row[correctIndex])
	f.close()
	return cResponse, pResponse, exResponse

#score breakdown (frequency)
#sorts responses by separating into
def breakdown(pResponse, exResponse,pKey,exKey):
	pBreakdown = {'present':0,'trick':0,'not':0, 'overall':0}
	exBreakdown = {'present':0,'trick':0,'not':0,'overall':0}

	#total correct answers
	pBreakdown['overall'] = sum(pResponse.values())
	exBreakdown['overall'] = sum(exResponse.values())

	#breakdown of incorrect answers
	for k in pResponse: #practice answers
		if pResponse[k]==0:
			pBreakdown[pKey[k]]+=1
	for k in exResponse: #experiment answers
		if exResponse[k]==0:
			exBreakdown[exKey[k]]+=1

	return pBreakdown, exBreakdown

'''convert scores to percentages'''
def percentage(pBreakdown, exBreakdown):
	pReturn = defaultdict(float)
	exReturn = defaultdict(float)
	divisor = 0
	for k in pBreakdown:
		if k=='overall':
			divisor = 6
		else:
			divisor = 2
		pReturn[k] = float(pBreakdown[k])/divisor*100
	for k in exBreakdown:
		if k=='overall':
			divisor = 60
		else:
			divisor = 20
		exReturn[k] = float(exBreakdown[k])/divisor*100

	return pReturn,exReturn

#Extracts the accuracty of multiple choice content questions.
def mcAccuracy(cData):
	cAnswer = {1:"c. Wolverine", 2:"a. Dancing", 3:"d. To compete in the Daytona 200", 4:"c. Gorilla mask"}
	cResult = defaultdict(str)
	total = 0
	for k in cData:
		if cData[k]==cAnswer[k]:
			cResult[k] = "CORRECT"
			total+=1
		else:
			cResult[k] = "INCORRECT"
	return cResult,total

#put into string formatting breakdown of subject name, score breakdown, and condition.
def toString(pBreakdown,exBreakdown,subjName,condition):
	s=''
	s+= "Subject: "+ str(subjName)+"\n"
	s+= "Condition: "+ str(condition)+"\n"
	s+= "Practice overall score: "+ str(pBreakdown['overall'])+" correct out of 6\n"
	s+= "Incorrect words category breakdown"+"\n"
	s+= "present: "+ str(pBreakdown['present'])+" out of 2 incorrect\n"
	s+= "trick: "+ str(pBreakdown['trick'])+" out of 2 incorrect\n"
	s+= "not: "+ str(pBreakdown['not'])+" out of 2 incorrect\n"
	s+= "\n"
	s+= "Experiment overall score: "+str(exBreakdown['overall'])+" correct out of 60\n"
	s+= "Incorrect words category breakdown"+"\n"
	s+= "present: "+ str(exBreakdown['present'])+" out of 20 incorrect\n"
	s+= "trick: "+ str(exBreakdown['trick'])+" out of 20 incorrect\n"
	s+= "not: "+ str(exBreakdown['not'])+" out of 20 incorrect\n"
	s+= "\n"
	s+= "."*40
	s+= "\n"
	return s

#put into string formatting the totals across all subjects, categorized by nap or wake.
def printTotals(subjTotalsNap,subjTotalsWake,napCount,wakeCount):
	s=''
	s+= "Nap Total Scores (averaged)"+"\n"
	s+= "Overall: "+ str(subjTotalsNap['overall']/napCount)+" out of 60 correct\n"
	s+= "Incorrect words category breakdown"+"\n"
	s+= "present: "+ str((subjTotalsNap['present']/napCount))+" out of 20 incorrect\n"
	s+= "trick: "+ str((subjTotalsNap['trick']/napCount))+" out of 20 incorrect\n"
	s+= "not: "+ str((subjTotalsNap['not']/napCount))+" out of 20 incorrect\n"
	s+= "\n"
	s+= "Wake Total Scores (averaged)"+"\n"
	s+= "Overall: "+ str(subjTotalsWake['overall']/wakeCount)+" out of 60 correct\n"
	s+= "Incorrect words category breakdown"+"\n"
	s+= "present: "+ str((subjTotalsWake['present']/wakeCount))+" out of 20 incorrect\n"
	s+= "trick: "+ str((subjTotalsWake['trick']/wakeCount))+" out of 20 incorrect\n"
	s+= "not: "+ str((subjTotalsWake['not']/wakeCount))+" out of 20 incorrect\n"
	s+= "\n"
	s+= "-"*40
	s+= "\n"
	return s

#put into string formatting subject multiple choice answers and accuracy.
def printMC(cdata,subjName):
	result,total=mcAccuracy(cdata)
	s=""
	s+="Subject: " + str(subjName) + "\n"
	s+="a1: "+ str(cdata[1]) + " " + str(result[1]) + "\n"
	s+="a2: "+ str(cdata[2]) + " " +str(result[2]) + "\n"
	s+="a3: "+ str(cdata[3]) + " " + str(result[3]) + "\n"
	s+="a4: "+ str(cdata[4]) + " " +str(result[4]) + "\n"
	s+="Total correct: " + str(total) + "\n\n"
	return s

#main function. Extracts necessary data from file, processes into proper formatting, do prelim calculations, output to console and file
def main():
	#get all necessary data
	practiceFile = 'practice_words.csv'
	experimentFile = 'experimental_words.csv'
	fnames = os.listdir('behavioral_data')
	f = open(os.path.join('analyzed_data','subject_analysis.txt'),'w') #file to write subject experimental task results
	g = open(os.path.join('analyzed_data','mc_questions.txt'),'w') #file to write subject multiple choice results

	#parse out answer keys
	practiceCat = ansKey(practiceFile,'cat')
	experimentCat = ansKey(experimentFile,'cat')

	#initialize dictionaries to store results of data extraction, contains totals across subjects, separated by category.
	subjTotalsNap = defaultdict(float)
	subjTotalsWake = defaultdict(float)
	mcTotalsNap = defaultdict(float)
	mcTotalsWake = defaultdict(float)

	#keep count of number of subjects per category for averaging use.
	napCount = 0
	wakeCount = 0

	for subj in fnames:
		#reading in subject files...
		sFilename = list(subj)
		condition = ''
		#determine subject condition based on file name. If 0, then nap, if 1 then awake.
		if sFilename[14]=='0':
			condition = 'nap'
			napCount+=1
		else:
			condition = 'awake'
			wakeCount+=1

		#read in necessary data from data file...
		cdata,pdata,exdata = dataReader(os.path.join('behavioral_data',subj))


		#calculating incorrect breakdown...
		pBreakdown, exBreakdown = breakdown(pdata,exdata,practiceCat,experimentCat)

		#calculating subject totals...
		for k in exBreakdown:
			if condition == 'nap':
				subjTotalsNap[k]+=exBreakdown[k]
			else:
				subjTotalsWake[k]+=exBreakdown[k]

		#print to console for each subject
		print printMC(cdata,subj)
		print toString(pBreakdown,exBreakdown, subj, condition)

		#write to txt file for each subject
		f.write(toString(pBreakdown,exBreakdown, subj, condition))
		g.write(printMC(cdata,subj))
		
	#print to console for totals and write to file
	print printTotals(subjTotalsNap,subjTotalsWake,napCount,wakeCount)
	f.write(printTotals(subjTotalsNap,subjTotalsWake,napCount,wakeCount))

#run main function
if __name__=='__main__':
	main()

