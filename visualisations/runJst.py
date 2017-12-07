import subprocess
import os
import databaseConfigurations.config as config
import databaseConfigurations.sqlQueries as sqlQueries
import processingData.inputManagment as inputManagment
from spacy.attrs import ORTH
from spacy import en
import spacy
import processingData.spacyStopWords as spacyStopWords
import processingData.fileFunctions as fileFunctions

nlp = spacy.load("en")
spacyStopWords.stopWordsList(nlp)

#function to prepare the file that will be ran by jst
def prepareJstData(collectionIdToShow, numberOfTopics, numberOfTopicWords):
	idOfCollection = sqlQueries.getCollectionId(cursor, collectionIdToShow)

	listOfCollectionParameters = sqlQueries.getParametersOfCollection(cursor, str(idOfCollection))
	collectionName = sqlQueries.getCollectionName(cursor, collectionIdToShow)
	tweets=[]
	originalWordCountList = []
	for parameter in listOfCollectionParameters:
		listOfKeywords = parameter[1].split(',')
		listOfListOfKeywords = []
		listOfListOfKeywords.append(listOfKeywords)
		tweetsFromGroup=inputManagment.fetchingTweetsContainingGroups(cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])
		tweets.append(tweetsFromGroup)

	tweetList = [tweet for sublist in tweets for tweet in sublist]
	tweetL = [tweet for sublist in tweetList for tweet in sublist]	
	allTweetsCleaned = []
	for tweet in tweetL:
		count = len(tweet[0].split(" "))
		countTuple = (tweet[0], tweet[0], count)
		originalWordCountList.append(countTuple)
		sentence = nlp(tweet[0])
		cleanText = []
		textCleanUp.textCleanup(cleanText, sentence)
		tweetList = [tweet[0],tweet[1], cleanText, tweet[3]]
		allTweetsCleaned.append(tweetList)

	fileFunctions.writeJstFile(allTweetsCleaned, originalWordCountList)

#function to run jst
def runJST(collectionIdToShow, numberOfTopics, numberOfTopicWords):
	prepareJstData(collectionIdToShow, numberOfTopics, numberOfTopicWords)

	FNULL = open(os.devnull, 'w')  
	trainingPropertiesFilePath = config.getJstTrainingProperties()
	jstExecutable = config.getJstExecutable()
	args = jstExecutable+" -est -config " + trainingPropertiesFilePath
	print("Begining to run jst.")
	subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
	print("jst finished.")
