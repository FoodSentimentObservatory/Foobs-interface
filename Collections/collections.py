import databaseConfigurations.sqlQueries as sqlQueries
import DataManager.collectionsDataManager as collectionsDataManager
import DataManager.tweetsDataManager as tweetsDataManager
import processingData.resultsFiltering as resultsFiltering
import processingData.fileFunctions as fileFunctions
import Analysis.testScatterText as testScatterText

class Collection():

	def __init__(self, collectionId, cursor):
		self.collectionId = collectionId
		self.cursor = cursor
		self.idOfCollection = collectionsDataManager.getCollectionId(self.cursor,self.collectionId)
		self.groupOfParameters = []
		self.collectionName = collectionsDataManager.getCollectionName(cursor, str(self.collectionId))

	def saveCollection(self, collectionName, collectionDescription, dateOfCreation, groupOfKeywords, searchQuery, location, fromDate, toDate):
		checkIfExists = collectionsDataManager.searchForCollection(self.cursor,self.collectionId)
		if len(checkIfExists)>0:
			collectionsDataManager.updateExistingCollection(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation)
		else:
			collectionsDataManager.createNewCollection(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation)	

		self.idOfCollection = collectionsDataManager.getCollectionId(self.cursor,self.collectionId)
		collectionsDataManager.saveCollectionParameters(self.cursor, self.idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate)	

	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
			if len(keywordGroups)>0:
				if isinstance(keywordGroups, str):
					listOfKeywordGroups = [keywordGroups]
				else:
					listOfKeywordGroups=keywordGroups	
			
				for group in listOfKeywordGroups:
					print(str(group))
					collectionsDataManager.deleteASpecificParameter(self.cursor, str(self.idOfCollection), group)

			collectionsDataManager.updateExistingCollection(self.cursor, self.collectionId, nameOfProject, descriptionOfProject,timeStamp)

	def deleteACollection(self):
		collectionsDataManager.deleteAllParametersOfACollection(self.cursor, str(self.idOfCollection))	
		collectionsDataManager.deleteCollectionEntry(self.cursor, self.collectionId)	

	def showACollection(self):
		listOfCollectionParameters = collectionsDataManager.getParametersOfCollection(self.cursor, str(self.idOfCollection))

		tweets=[]
		i=0
		for parameter in listOfCollectionParameters:
			listOfKeywords = parameter[1].split(',')
			listOfListOfKeywords = []
			listOfListOfKeywords.append(listOfKeywords)
			tweetsFromGroup=tweetsDataManager.fetchingTweetsContainingGroups(self.cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])
			numberOfTweets = len(tweetsFromGroup[0])
			noCommaGroupOfTweets = parameter[1].replace(",","")
			parameterData = [noCommaGroupOfTweets, parameter[1],i ,parameter[2], parameter[3], parameter[4], parameter[5], numberOfTweets]
			self.groupOfParameters.append(parameterData)	
			tweets.append(tweetsFromGroup)	
			i+=1		
		tweetList = [tweet for sublist in tweets for tweet in sublist]
		tweetL = [tweet for sublist in tweetList for tweet in sublist]	
			
		index = 5
		collectionDictionary = resultsFiltering.dictionaryGen(tweetL,index)

		return collectionDictionary

	def getAllCollections(self):
		collectionsList=collectionsDataManager.getExistingCollections(self.cursor)

		return collectionsList

	def getAllParameters(self):
		listOfAllParameters = collectionsDataManager.getAllCollectionParameters(self.cursor)
		index=1
		parametersDictionary = resultsFiltering.dictionaryGen(listOfAllParameters, index)
		paramsList = resultsFiltering.makeAStringOfKeywordGroups(parametersDictionary)
		print(paramsList)

		return paramsList	

				

		