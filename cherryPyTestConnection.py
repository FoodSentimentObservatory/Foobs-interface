import cherrypy
import databaseConfigurations.sqlQueries as sqlQueries
import processingData.inputManagment as inputManagment
import os
from jinja2 import Environment, FileSystemLoader
import processingData.fileFunctions as fileFunctions
import visualisations.testScatterText as testScatterText
import visualisations.runJst as runJst
import SearchResult.keywordSearch as keywordSearch
import SearchResult.frequentKeywordsResults as frequentKeywordsResult
import Collections.collections as collections

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
		self.fromDate = fromDate
		self.toDate = toDate
		self.dbName = dbName		
		searchResult = keywordSearch.SearchResult(group, self.fromDate, self.toDate, self.dbName, self.location, self.searchQuery)
		listOfCollections = searchResult.listOfCollections()
		tweetDictionary = searchResult.retrieveTweets()
		groupList = searchResult.getGroupList()
		
		template = env.get_template('GUI/results.html')
		#sending the tweets and the group data to html
		return template.render(dicw=tweetDictionary, listOfCollections=listOfCollections, groupList=groupList, i=0)
	#calling the frequent keywords module	
	@cherrypy.expose	
	def frequentKeywordSearch(self,group, tweets, word,groupIdStr,groupOriginalName):
		frequentWordResult = frequentKeywordsResult.FrequentKeywordsResult(group, tweets, word,groupIdStr,groupOriginalName)

		orderedFreqKeywordTweetDict = frequentWordResult.returnDictionaryOfTweets()

		groupList = frequentWordResult.returnFrequentWordsGroupList()

		template = env.get_template('GUI/freqResults.html')
		#sending the tweets and the group data to html
		return template.render(dicw=orderedFreqKeywordTweetDict, groupOriginalName=groupOriginalName, groupList=groupList, word=word)	

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

		collectionsObject = collections.Collection(collectionId,cursor)
		collectionsObject.saveCollection(collectionName, collectionDescription, dateOfCreation, groupOfKeywords, self.searchQuery, self.location, self.fromDate, self.toDate)

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)
	@cherrypy.expose	
	def collectionsPage(self):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection("S",cursor)
		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList, paramsList=paramsList)

	@cherrypy.expose
	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()
		
		collectionsObject = collections.Collection(collectionId,cursor)
		collectionsObject.updateCollection(collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups)

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	
	
	@cherrypy.expose
	def deleteCollection(self, collectionToDeleteId):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToDeleteId,cursor)		
		collectionsObject.deleteACollection()

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	

	@cherrypy.expose	
	def showCollection(self, collectionToShowId):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToShowId,cursor)	
		groupOfParameters = collectionsObject.groupOfParameters
		collectionDictionary = collectionsObject.showACollection()
		collectionName = collectionsObject.collectionName

		conn.close()

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

			html = testScatterText.visualiseCollections(cursor,twoCollectionId)
			conn.close()
			return html		

	@cherrypy.expose
	def topicVisualisationHomePage(self):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()

		collectionsList=sqlQueries.getExistingCollections(cursor)

		conn.close()

		template = env.get_template('GUI/topicHomePage.html')
		#sending the tweets and the group data to html
		return template.render(collectionsList=collectionsList)	

	@cherrypy.expose							
	def topicVisualisation(self, collectionIdToShow, numberOfTopics, numberOfTopicWords):
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	
		cursor = conn.cursor()
		print(collectionIdToShow)
		print(numberOfTopics)
		print(numberOfTopicWords)

		visualisations.runJst(collectionIdToShow, numberOfTopics, numberOfTopicWords)

		fileFunctions.readJSTResultFiles()

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

