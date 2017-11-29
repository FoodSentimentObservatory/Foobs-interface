import cherrypy
import databaseConfigurations.sqlQueries as sqlQueries
import processingData.inputManagment as inputManagment
import os
from Cheetah.Template import Template
import datetime
import processingData.textCleanUp as textCleanUp
import re
from jinja2 import Environment, FileSystemLoader
from itertools import groupby
import html
import collections
import processingData.fileFunctions as fileFunctions
import visualisations.testScatterText as testScatterText

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env=Environment(loader=FileSystemLoader(CUR_DIR),
trim_blocks=True)
listOfCollectionData={}
class ServerConnection(object):
	def __init__(self):
		self.location=""
		self.searchQuery=""	

	@cherrypy.expose
	def index(self):
		listOfDatabases = inputManagment.getDBs() 
		searchNotesDic = inputManagment.getSearchNotes()
		listOfAllCollections = inputManagment.getCollectionsFromAllDbs()

		template = env.get_template('GUI/index.html')
		#sending the tweets and the group data to html
		return template.render(dicw=searchNotesDic, listOfDatabases=listOfDatabases, title="something", listOfAllCollections=listOfAllCollections)

	@cherrypy.expose
	def manual(self):
		return open('GUI/manual.html')	
	
	#direct towards the relevant script
	@cherrypy.expose
	def connectToScript(self, inputTypes, searchnoteID, dbName, start, endof,keywords, twoCollectionId):
		self.location = searchnoteID.split("-")[0]
		self.searchQuery = searchnoteID.split("- ")[1]
		self.dbName = dbName
		self.startDate = start
		self.endof = endof
		template = env.get_template('GUI/keywordSearch.html')
		#sending the tweets and the group data to html
		return template.render(startDate=self.startDate, endDate=self.endof, title="something")
 	
	#script for keyword searches
	@cherrypy.expose	
	def keywordSearch(self, group, groups, checkName,fromDate,toDate, dbName):		
			self.dbName=dbName	
			conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
			cursor = conn.cursor()
			listOfGroups=[]
			listOfTweets=[]
			listOfCollections = sqlQueries.getExistingCollections(cursor)

			self.fromDate = fromDate
			self.toDate = toDate
			#checking if there's only one or multiple keyword groups
			if isinstance(group, str):
				listofwords = group.split(",")
				listOfGroups.append(listofwords)
			else:
				for g in group:
					singleGroup = g.split(",")
					listOfGroups.append(singleGroup)
			#kinda pointless check but might be useful at a later stage....or not			
			if  len(group)>0:
				countOfGroups = len(listOfGroups)
				#getting all tweets with the specified keywords, the result is a list of lists, tweets are grouped in lists by keyword groups
				tweets=inputManagment.fetchingTweetsContainingGroups(cursor,self.location,self.searchQuery,listOfGroups, fromDate, toDate)
				i=0
				tweetList=[]
				groupList = []
				#for each group of tweets (all tweets fetched for one group of keywords)
				for groupOfTweets in tweets:
					numberOfTweets = len(groupOfTweets)
					if len(listOfGroups)>1:
						strGroupOfTweets = ''.join(group[i])
						frequentWords = textCleanUp.frequencyCount(groupOfTweets,group[i])
					else:
						strGroupOfTweets = ''.join(group)	
						frequentWords = textCleanUp.frequencyCount(groupOfTweets,group)
					noCommaGroupOfTweets = strGroupOfTweets.replace(',','')
					#getting the most frequent words in that group
					
					
					#sending to html the keyword group name, ID, number of tweets in it and a list of the most frequent words		
					groupTup = (noCommaGroupOfTweets, strGroupOfTweets,i,numberOfTweets,frequentWords, groupOfTweets)
					groupList.append(groupTup)
					i+=1

					for tweet in groupOfTweets:
						tweetL = list(tweet)
						#making links clickable
						text = textCleanUp.clickableLinks(tweetL[0])
						tweetL.append(text)
						#sending the tweets to a list
						tweetList.append(tweetL)

				index=5
				dicw = textCleanUp.dictionaryGen(tweetList,index)

			template = env.get_template('GUI/results.html')
			conn.close()
			#sending the tweets and the group data to html
			return template.render(dicw=dicw, listOfCollections=listOfCollections, groupList=groupList, i=0)

	@cherrypy.expose	
	def frequentKeywordSearch(self,group, tweets, word,groupIdStr,groupOriginalName, dbName):
		newGroups = []
		firstwordList =[]
		self.dbName=dbName	
		#the tweets list and the tuples of frequent keywords are returned as strs instead of lists..
		#..however, they do look like lists, so we need to strip them from the list chars and split them
		tweetsList=tweets.split("], [")
		tweetDataList=[]
		tweetDataListNoHtmlTags=[]
		for tweet in tweetsList:
			charList=['[[',']]','\n']
			check=1
			cleanTweet=textCleanUp.extraCharRemoval(tweet, charList,check)
			tweetData = cleanTweet.split("', '")
			text=html.escape(tweetData[0],quote=True)
			displayName = html.escape(tweetData[4],quote=True)
			newText = textCleanUp.clickableLinks(text)
			#making two lists, one that will be used for content and one for the hidden input field
			#difference is that the one for the hidden field doesn't contain html tags
			dataWithNoHtmlTags = [text,tweetData[1],tweetData[2],tweetData[3],displayName]
			filteredTweetData=[newText,tweetData[1],tweetData[2],tweetData[3],tweetData[4]]
			tweetDataList.append(filteredTweetData)
			tweetDataListNoHtmlTags.append(dataWithNoHtmlTags)
		#splitting the freqword str into a list
		groupListL=group.split("), (")
		cleanGroupList=[]
		for groups in groupListL:
			charList=['\'','[',']','(',')']
			check=0
			groups=textCleanUp.extraCharRemoval(groups, charList,check)
			groupTup = groups.split(", ")		
			cleanGroupList.append(groupTup[1])

		for tweet in tweetDataList:
			if word in tweet[0].lower():
				textCleanUp.addTweetToNewGroupsList(word,tweet,groupIdStr,newGroups)

		#searching if a frequent word is in a tweet			
		for freqWord in cleanGroupList:
			if freqWord!=word:
				for tweet in tweetDataList:
					if freqWord in tweet[0].lower():
						textCleanUp.addTweetToNewGroupsList(freqWord,tweet,groupIdStr,newGroups)
		#making a dictionary by frequent word				
		index=5
		dicw = textCleanUp.dictionaryGen(newGroups,index)
		i=0
		groupList=[]
		od = collections.OrderedDict(sorted(dicw.items()))
		for key, value in od.items():
			numberOfTweets=len(value)
			groupId=groupIdStr+key
			groupString=groupOriginalName+","+key
			frequentWords = textCleanUp.frequencyCount(value,groupString)
			listForInputValues=[]
			for tweet in tweetDataListNoHtmlTags:
				if key in tweet[0].lower():
					listForInputValues.append(tweet)
			groupTup = (key, groupString,i,numberOfTweets,frequentWords, listForInputValues)
			groupList.append(groupTup)
			i+=1

		template = env.get_template('GUI/freqResults.html')
		#sending the tweets and the group data to html
		return template.render(dicw=od, groupOriginalName=groupOriginalName, groupList=groupList, word=word)	

	@cherrypy.expose
	def saveCollection(self,collectionId, collectionName, collectionDescription, dbName, dateOfCreation, groupOfKeywords):
		print(collectionId)
		print(collectionName)
		print(collectionDescription)
		print (groupOfKeywords)

		print (listOfCollectionData)			
		self.dbName=dbName	
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()
		checkIfExists = sqlQueries.searchForUniqueId(cursor,collectionId)
		print(len(checkIfExists))
		if len(checkIfExists)>0:
			sqlQueries.updateCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation)
		else:
			sqlQueries.createANewCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation)	
		idOfCollection = sqlQueries.getCollectionId(cursor, collectionId)		
		sqlQueries.saveQueryParameters(cursor, idOfCollection, groupOfKeywords, self.searchQuery, self.location, self.fromDate, self.toDate)	
		collectionsList=sqlQueries.getExistingCollections(cursor)
		listOfAllParameters = sqlQueries.getAllCollectionParameters(cursor)
		index=1
		parametersDictionary = textCleanUp.dictionaryGen(listOfAllParameters, index)
		paramsList = textCleanUp.makeAStringOfKeywordGroups(parametersDictionary)
		conn.close()
		print(collectionsList)

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)
	@cherrypy.expose	
	def collectionsPage(self):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()

		collectionsList=sqlQueries.getExistingCollections(cursor)
		listOfAllParameters = sqlQueries.getAllCollectionParameters(cursor)
		index=1
		parametersDictionary = textCleanUp.dictionaryGen(listOfAllParameters, index)
		paramsList = textCleanUp.makeAStringOfKeywordGroups(parametersDictionary)
			

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList, paramsList=paramsList)

	@cherrypy.expose
	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()
		idOfCollection=sqlQueries.getCollectionId(cursor,collectionId)
		if len(keywordGroups)>0:
			if isinstance(keywordGroups, str):
				listOfKeywordGroups = [keywordGroups]
			else:
				listOfKeywordGroups=keywordGroups	
		
			for group in listOfKeywordGroups:
				print(str(group))
				sqlQueries.deleteASpecificParameter(cursor, str(idOfCollection), group)

		sqlQueries.updateCollectionEntry(cursor, collectionId, nameOfProject, descriptionOfProject,timeStamp)

		collectionsList=sqlQueries.getExistingCollections(cursor)
		listOfAllParameters = sqlQueries.getAllCollectionParameters(cursor)
		index=1
		parametersDictionary = textCleanUp.dictionaryGen(listOfAllParameters, index)
		paramsList = textCleanUp.makeAStringOfKeywordGroups(parametersDictionary)
		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	
	
	@cherrypy.expose
	def deleteCollection(self, collectionToDeleteId):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()
		idOfCollection = sqlQueries.getCollectionId(cursor, collectionToDeleteId)
		sqlQueries.deleteCollectionEntry(cursor, collectionToDeleteId)
		sqlQueries.deleteAllParametersOfACollection(cursor, str(idOfCollection))

		collectionsList=sqlQueries.getExistingCollections(cursor)
		listOfAllParameters = sqlQueries.getAllCollectionParameters(cursor)
		index=1
		parametersDictionary = textCleanUp.dictionaryGen(listOfAllParameters, index)
		paramsList = textCleanUp.makeAStringOfKeywordGroups(parametersDictionary)
		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	

	@cherrypy.expose	
	def showCollection(self, collectionToShowId):
			conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
			cursor = conn.cursor()

			idOfCollection = sqlQueries.getCollectionId(cursor, collectionToShowId)

			listOfCollectionParameters = sqlQueries.getParametersOfCollection(cursor, str(idOfCollection))
			collectionName = sqlQueries.getCollectionName(cursor, collectionToShowId)
			tweets=[]
			groupOfParameters = []
			i=0
			for parameter in listOfCollectionParameters:
				listOfKeywords = parameter[1].split(',')
				listOfListOfKeywords = []
				listOfListOfKeywords.append(listOfKeywords)
				tweetsFromGroup=inputManagment.fetchingTweetsContainingGroups(cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])
				numberOfTweets = len(tweetsFromGroup[0])
				noCommaGroupOfTweets = parameter[1].replace(",","")
				parameterData = [noCommaGroupOfTweets, parameter[1],i ,parameter[2], parameter[3], parameter[4], parameter[5], numberOfTweets]
				groupOfParameters.append(parameterData)	
				tweets.append(tweetsFromGroup)	
				i+=1		
			tweetList = [tweet for sublist in tweets for tweet in sublist]
			tweetL = [tweet for sublist in tweetList for tweet in sublist]	
			
			index = 5
			collectionDictionary = textCleanUp.dictionaryGen(tweetL,index)
			
			template = env.get_template('GUI/displayCollection.html')
			#sending the tweets and the group data to html
			return template.render(groupOfParameters=groupOfParameters, collectionDictionary=collectionDictionary, collectionName=collectionName)	


	#@cherrypy.expose
	#def visualiseCollectionsFromIndexPage(self,inputTypes, dbName, start, endof,keywords,twoCollectionId, collectionRow):
		#html = visualiseCollections(twoCollectionId,self.location,self.searchQuery,self.fromDate, self.toDate)
		#return html

	#@cherrypy.expose
	#def visualiseCollectionsFromCollectionsPage(self, twoCollectionId):
		#html = visualiseCollections(twoCollectionId)
		#return html

	@cherrypy.expose	
	def visualiseCollections(self, twoCollectionId):
			conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
			cursor = conn.cursor()
			print (twoCollectionId)	

			idsForVis = twoCollectionId.split(',')
			listOfDataForVis = []
			listOfCollectionNames = []
			for uniqueId in idsForVis:
				idOfCollection = sqlQueries.getCollectionId(cursor, uniqueId)

				listOfCollectionParameters = sqlQueries.getParametersOfCollection(cursor, str(idOfCollection))
				collectionName = sqlQueries.getCollectionName(cursor, uniqueId)
				listOfCollectionNames.append(collectionName)
				tweets=[]
				for parameter in listOfCollectionParameters:
					listOfKeywords = parameter[1].split(',')
					listOfListOfKeywords = []
					listOfListOfKeywords.append(listOfKeywords)
					tweetsFromGroup=inputManagment.fetchingTweetsContainingGroups(cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])	
					tweets.append(tweetsFromGroup)			
				tweetList = [tweet for sublist in tweets for tweet in sublist]
				
				for tweetGroup in tweetList:
							for tweet in tweetGroup:
								tweetTuple = (collectionName, tweet[4], tweet[0])
								listOfDataForVis.append(tweetTuple)
			jsonTweetData = fileFunctions.generateJson(listOfDataForVis)
			html = testScatterText.generateScatterText(jsonTweetData, listOfCollectionNames)
			conn.close()
			return html							

			
if __name__ == '__main__':

	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './GUI/public'
		}
	}

	cherrypy.quickstart(ServerConnection(), '/', conf)

