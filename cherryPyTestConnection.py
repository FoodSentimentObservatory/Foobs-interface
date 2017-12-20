import cherrypy
import DataManager.dataManager as dataManager
import DataManager.collectionsDataManager as collectionsDataManager
import os
from jinja2 import Environment, FileSystemLoader
import processingData.fileFunctions as fileFunctions
import Analysis.testScatterText as testScatterText
import Analysis.runJst as runJst
import SearchResult.keywordSearch as keywordSearch
import SearchResult.frequentKeywordsResults as frequentKeywordsResult
import Collections.collections as collections
import Analysis.donutVis as donutVis
import processingData.word2vec as word2vec
import processingData.resultsFiltering as resultsFiltering

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CUR_DIR+'/GUI/')
env=Environment(loader=FileSystemLoader(CUR_DIR+'/GUI'),
trim_blocks=True)
listOfCollectionData={}
class ServerConnection(object):
	def __init__(self):
		self.location=""
		self.searchQuery=""	
	#loads the homepage	
	@cherrypy.expose
	def index(self):
		listOfDatabases = dataManager.getDBs() 
		searchNotesDic = dataManager.getSearchNotes()
		listOfAllCollections = collectionsDataManager.getCollectionsFromAllDbs()

		template = env.get_template('index.html')
		return template.render(searchNotesDic=searchNotesDic, listOfDatabases=listOfDatabases, title="something", listOfAllCollections=listOfAllCollections)
	#loads the manual page	
	@cherrypy.expose
	def manual(self):
		return open('manual.html')	
	
	#loads the search form if an aption from the data explorer has been selected
	@cherrypy.expose
	def connectToScript(self, searchnoteID, dbName, start, endof,keywords, task):
		self.setSelfValues(searchnoteID,dbName,start,endof,keywords)
		template = env.get_template('keywordSearch.html')
		return template.render(startDate=self.startDate, endDate=self.endof, task=task)
	#loads the search form if an option from the cluster dataset menu has been selected	
	@cherrypy.expose
	def clusterFromDataSet(self,searchnoteIDForCluster, dbName, endof,start,keywordsCluster,task):
		self.setSelfValues(searchnoteIDForCluster,dbName,start,endof,keywordsCluster)
		template = env.get_template('keywordSearch.html')
		return template.render(startDate=self.startDate, endDate=self.endof, task=task)
	#sets the class values	
	def setSelfValues(self,searchNote,dbName,start,endof, keywords):
		self.location = searchNote.split("-")[0]
		self.searchQuery = searchNote.split("- ")[1]
		self.dbName = dbName
		self.startDate = start
		self.endof = endof	
		self.keywordsOfSearch = keywords
	#script for data explorer search, displays the result page
	@cherrypy.expose	
	def keywordSearch(self, group, checkName,fromDate,toDate, dbName,checkIfKeywords):
		self.fromDate = fromDate
		self.toDate = toDate
		self.dbName = dbName
		self.group = group		
		searchResult = keywordSearch.SearchResult(self.group, self.fromDate, self.toDate, self.dbName, self.location, self.searchQuery)
		listOfCollections = searchResult.listOfCollections()
		tweetDictionary = searchResult.retrieveTweets()
		groupList = searchResult.getGroupList()
		queryDataList = searchResult.getQueryData()
		
		template = env.get_template('results.html')
		return template.render(dicw=tweetDictionary, listOfCollections=listOfCollections, groupList=groupList, i=0, queryData = queryDataList)

	#script for the frequent keywords search	
	@cherrypy.expose	
	def frequentKeywordSearch(self,group, tweets, word,groupIdStr,groupOriginalName):
		frequentWordResult = frequentKeywordsResult.FrequentKeywordsResult(group, tweets, word,groupIdStr,groupOriginalName)
		orderedFreqKeywordTweetDict = frequentWordResult.returnDictionaryOfTweets()
		groupList = frequentWordResult.returnFrequentWordsGroupList()

		template = env.get_template('freqResults.html')
		return template.render(dicw=orderedFreqKeywordTweetDict, groupOriginalName=groupOriginalName, groupList=groupList, word=word)	
	#loads the cluster form page	
	@cherrypy.expose
	def specifyClusterParams(self, fromDate,toDate,dbName,checkIfKeywords, group, checkName):
		self.fromDate = fromDate
		self.toDate = toDate
		self.dbName = dbName
		self.group = group
		print(self.keywordsOfSearch)
		template = env.get_template('clusterSpecForm.html')
		return template.render(keywords=self.keywordsOfSearch, keywordGroups = self.group)
	#saves or updates a collection	
	@cherrypy.expose
	def saveCollection(self,collectionId, collectionName, collectionDescription, dbName, dateOfCreation, groupOfKeywords):
		self.dbName=dbName	
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionId,cursor)
		collectionsObject.saveCollection(collectionName, collectionDescription, dateOfCreation, groupOfKeywords, self.searchQuery, self.location, self.fromDate, self.toDate)

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)
	#loads the collections page	
	@cherrypy.expose	
	def collectionsPage(self):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection("S",cursor)
		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('collectionsPage.html')
		return template.render(collectionsList=collectionsList, paramsList=paramsList, dbName=self.dbName)
	#updates a collection on click of update button in the collections page	
	@cherrypy.expose
	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()
		
		collectionsObject = collections.Collection(collectionId,cursor)
		collectionsObject.updateCollection(collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups)

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	
	#deletes a collection on click of the delete button in the collections page
	@cherrypy.expose
	def deleteCollection(self, collectionToDeleteId):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToDeleteId,cursor)		
		collectionsObject.deleteACollection()

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	
	#shows a collection on the click of the show collection button in the collections page	
	@cherrypy.expose	
	def showCollection(self, collectionToShowId):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToShowId,cursor)	
		groupOfParameters = collectionsObject.groupOfParameters
		collectionDictionary = collectionsObject.showACollection()
		collectionName = collectionsObject.collectionName

		conn.close()

		template = env.get_template('displayCollection.html')
		return template.render(groupOfParameters=groupOfParameters, collectionDictionary=collectionDictionary, collectionName=collectionName)	

	#loads scatter text on selection of two collections, both from collections page and home page	
	@cherrypy.expose	
	def visualiseCollections(self, twoCollectionId, dbName):
			conn = dataManager.startDbConnection(dbName)	
			cursor = conn.cursor()	
			html = testScatterText.visualiseCollections(cursor,twoCollectionId)
			conn.close()
			return html		

	@cherrypy.expose
	def topicVisualisationHomePage(self):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsList=collectionsDataManager.getExistingCollections(cursor)

		conn.close()

		template = env.get_template('topicHomePage.html')
		return template.render(collectionsList=collectionsList)	

	@cherrypy.expose							
	def topicVisualisation(self, collectionIdToShow, numberOfTopics, numberOfTopicWords):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()
		print(collectionIdToShow)
		print(numberOfTopics)
		print(numberOfTopicWords)

		runJst.runJst(collectionIdToShow, numberOfTopics, numberOfTopicWords)

		fileFunctions.readJSTResultFiles()
	#loads the donut for a selected keyword from the clusters stats page
	#works by filtering the already created result dictionary to search for the selected keyword	
	@cherrypy.expose	
	def generateClusters(self,keyword):		
		cluster = donutVis.Cluster(self.tweetDictionary)
		clusteredTweetsDicts = cluster.clusterKeywords(self.keywordsForSegmentsList, keyword)
		tweetsOfClustersStr = cluster.tweetsString
		tweetsOfClustersList = cluster.filteredTweetsList
		
		template = env.get_template('clusters.html')
		return template.render(clustersList=clusteredTweetsDicts, tweetsOfClusters=tweetsOfClustersStr,tweetsOfClustersList=tweetsOfClustersList)
	#searches for tweets for the selected cluster and segment keywords
	#loads clusters stats page	
	@cherrypy.expose	
	def createClusters(self, keywordsToCluster, keywordsForSegments, enrichKeywords):	
		keywordClusterList = resultsFiltering.createKeywordList(keywordsToCluster,',')	

		if enrichKeywords == 'enrich':		
			keywordsToClusterEnriched = word2vec.getSimilarForListOfWords(keywordClusterList)
		else:
			keywordsToClusterEnriched=keywordClusterList	

		self.keywordsForSegmentsList = resultsFiltering.createKeywordList(keywordsForSegments,';')
		if self.group == 'no groups':
			searchResult = keywordSearch.SearchResult(keywordsToClusterEnriched, self.fromDate, self.toDate, self.dbName, self.location, self.searchQuery)
			self.tweetDictionary = searchResult.retrieveTweets()
			keywordConstraints = 'none'
		else:
			searchResult = keywordSearch.SearchResult(self.group, self.fromDate, self.toDate, self.dbName, self.location, self.searchQuery)
			self.tweetDictionary = searchResult.filterTweets(keywordsToClusterEnriched)
			keywordConstraints = resultsFiltering.getKeywordContraintString(self.group)	

		cluster = donutVis.Cluster(self.tweetDictionary)
		listOfCounts = cluster.getCounts(self.keywordsForSegmentsList)
		listOfResultParameters = [self.fromDate, self.toDate,self.location, self.searchQuery, keywordConstraints]
		keywordsWithNoResults = cluster.getKeywordsWithNoResults(keywordsToClusterEnriched, listOfCounts)
		if len(keywordsWithNoResults)==0:
			check = 0
		else:
			check = 1

		template = env.get_template('clustersStatsPage.html')
		return template.render(countsList = listOfCounts,listOfResultParameters=listOfResultParameters,keywordsWithNoResults=keywordsWithNoResults,check=check)	

	

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

