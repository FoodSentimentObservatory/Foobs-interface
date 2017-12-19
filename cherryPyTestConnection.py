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
env=Environment(loader=FileSystemLoader(CUR_DIR),
trim_blocks=True)
listOfCollectionData={}
class ServerConnection(object):
	def __init__(self):
		self.location=""
		self.searchQuery=""	

	@cherrypy.expose
	def index(self):
		listOfDatabases = dataManager.getDBs() 
		searchNotesDic = dataManager.getSearchNotes()
		listOfAllCollections = collectionsDataManager.getCollectionsFromAllDbs()

		template = env.get_template('GUI/index.html')
		return template.render(dicw=searchNotesDic, listOfDatabases=listOfDatabases, title="something", listOfAllCollections=listOfAllCollections)

	@cherrypy.expose
	def manual(self):
		return open('GUI/manual.html')	
	
	#direct towards the relevant script
	@cherrypy.expose
	def connectToScript(self, searchnoteID, dbName, start, endof,keywords, task):
		self.setSelfValues(searchnoteID,dbName,start,endof,keywords)
		template = env.get_template('GUI/keywordSearch.html')
		return template.render(startDate=self.startDate, endDate=self.endof, title="something",task=task)

	@cherrypy.expose
	def clusterFromDataSet(self,searchnoteIDForCluster, dbName, endof,start,keywordsCluster,task):
		self.setSelfValues(searchnoteIDForCluster,dbName,start,endof,keywordsCluster)
		template = env.get_template('GUI/keywordSearch.html')
		return template.render(startDate=self.startDate, endDate=self.endof, title="something",task=task)

	def setSelfValues(self,searchNote,dbName,start,endof, keywords):
		self.location = searchNote.split("-")[0]
		self.searchQuery = searchNote.split("- ")[1]
		self.dbName = dbName
		self.startDate = start
		self.endof = endof	
		self.keywordsOfSearch = keywords
	#script for keyword searches
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
		
		template = env.get_template('GUI/results.html')
		return template.render(dicw=tweetDictionary, listOfCollections=listOfCollections, groupList=groupList, i=0, queryData = queryDataList)

	#calling the frequent keywords module	
	@cherrypy.expose	
	def frequentKeywordSearch(self,group, tweets, word,groupIdStr,groupOriginalName):
		frequentWordResult = frequentKeywordsResult.FrequentKeywordsResult(group, tweets, word,groupIdStr,groupOriginalName)
		orderedFreqKeywordTweetDict = frequentWordResult.returnDictionaryOfTweets()
		groupList = frequentWordResult.returnFrequentWordsGroupList()

		template = env.get_template('GUI/freqResults.html')
		return template.render(dicw=orderedFreqKeywordTweetDict, groupOriginalName=groupOriginalName, groupList=groupList, word=word)	
	@cherrypy.expose
	def specifyClusterParams(self, fromDate,toDate,dbName,checkIfKeywords, group, checkName):
		self.fromDate = fromDate
		self.toDate = toDate
		self.dbName = dbName
		self.group = group
		print(self.keywordsOfSearch)
		template = env.get_template('GUI/clusterSpecForm.html')
		return template.render(keywords=self.keywordsOfSearch, keywordGroups = self.group)

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

		template = env.get_template('GUI/collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)

	@cherrypy.expose	
	def collectionsPage(self):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection("S",cursor)
		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		return template.render(collectionsList=collectionsList, paramsList=paramsList, dbName=self.dbName)

	@cherrypy.expose
	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()
		
		collectionsObject = collections.Collection(collectionId,cursor)
		collectionsObject.updateCollection(collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups)

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	
	
	@cherrypy.expose
	def deleteCollection(self, collectionToDeleteId):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToDeleteId,cursor)		
		collectionsObject.deleteACollection()

		collectionsList = collectionsObject.getAllCollections()
		paramsList = collectionsObject.getAllParameters()

		conn.close()

		template = env.get_template('GUI/collectionsPage.html')
		return template.render(collectionsList=collectionsList,paramsList=paramsList)	

	@cherrypy.expose	
	def showCollection(self, collectionToShowId):
		conn = dataManager.startDbConnection(self.dbName)	
		cursor = conn.cursor()

		collectionsObject = collections.Collection(collectionToShowId,cursor)	
		groupOfParameters = collectionsObject.groupOfParameters
		collectionDictionary = collectionsObject.showACollection()
		collectionName = collectionsObject.collectionName

		conn.close()

		template = env.get_template('GUI/displayCollection.html')
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

		template = env.get_template('GUI/topicHomePage.html')
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

	@cherrypy.expose	
	def generateClusters(self,keyword):		
		cluster = donutVis.Cluster(self.tweetDictionary)
		clusteredTweetsDicts = cluster.clusterKeywords(self.keywordsForSegmentsList, keyword)
		tweetsOfClustersStr = cluster.tweetsString
		tweetsOfClustersList = cluster.filteredTweetsList
		
		template = env.get_template('GUI/clusters.html')
		return template.render(clustersList=clusteredTweetsDicts, tweetsOfClusters=tweetsOfClustersStr,tweetsOfClustersList=tweetsOfClustersList)

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

		template = env.get_template('GUI/clustersStatsPage.html')
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

