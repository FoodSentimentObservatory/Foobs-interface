import scattertext as st
import spacy
from pprint import pprint
from scattertext import SampleCorpora
from scattertext.CorpusFromPandas import CorpusFromPandas
from scattertext import produce_scattertext_explorer
import pandas as pd
import numpy as np
import json
import DataManager.collectionsDataManager as collectionsDataManager
import DataManager.tweetsDataManager as tweetsDataManager
import processingData.fileFunctions as fileFunctions
#gets all the data it needs for the two collections and sets it into a format that can
#be processed by the scatter text method.
def visualiseCollections(cursor, twoCollectionId):
	idsForVis = twoCollectionId.split(',')
	listOfDataForVis = []
	listOfCollectionNames = []
	for uniqueId in idsForVis:
		idOfCollection = collectionsDataManager.getCollectionId(cursor, uniqueId)

		listOfCollectionParameters = collectionsDataManager.getParametersOfCollection(cursor, str(idOfCollection))
		collectionName = collectionsDataManager.getCollectionName(cursor, uniqueId)
		listOfCollectionNames.append(collectionName)
		tweets=[]
		for parameter in listOfCollectionParameters:
			listOfKeywords = parameter[1].split(',')
			listOfListOfKeywords = []
			listOfListOfKeywords.append(listOfKeywords)
			tweetsFromGroup=tweetsDataManager.fetchingTweetsContainingGroups(cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])	
			tweets.append(tweetsFromGroup)		

		tweetList = [tweet for sublist in tweets for tweet in sublist]
				
		for tweetGroup in tweetList:
			for tweet in tweetGroup:
				tweetTuple = (collectionName, tweet[4], tweet[0])
				listOfDataForVis.append(tweetTuple)

	jsonTweetData = fileFunctions.generateJson(listOfDataForVis)
	html = generateScatterText(jsonTweetData, listOfCollectionNames)

	return html	
#actually generates the html for the page
def generateScatterText(data, listOfCollectionNames):
	collectionOne = listOfCollectionNames[0]
	collectionTwo = listOfCollectionNames[1]

	convention_df = pd.DataFrame(eval(data))
	nlp = spacy.en.English()

	pprint(convention_df.iloc[1])


	corpus = CorpusFromPandas(convention_df,
	                          category_col='group',
	                          text_col='tweet',
	                          nlp=nlp).build()

	html = produce_scattertext_explorer(corpus,
	                                    category=collectionOne,
	                                    category_name=collectionOne,
	                                    not_category_name=collectionTwo,
	                                    minimum_term_frequency=5,
	                                    width_in_pixels=1000,
	                                    metadata=convention_df['username'])

	return html

	