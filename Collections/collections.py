import databaseConfigurations.sqlQueries as sqlQueries
import processingData.inputManagment as inputManagment
import processingData.textCleanUp as textCleanUp
import processingData.fileFunctions as fileFunctions
import visualisations.testScatterText as testScatterText

class Collection():

	def __init__(self, collectionId, cursor):
		self.collectionId = collectionId
		self.cursor = cursor
		self.idOfCollection = sqlQueries.getCollectionId(self.cursor,self.collectionId)
		self.groupOfParameters = []
		self.collectionName = sqlQueries.getCollectionName(cursor, str(self.collectionId))

	def saveCollection(self, collectionName, collectionDescription, dateOfCreation, groupOfKeywords, searchQuery, location, fromDate, toDate):
		checkIfExists = sqlQueries.searchForUniqueId(self.cursor,self.collectionId)
		if len(checkIfExists)>0:
			sqlQueries.updateCollectionEntry(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation)
		else:
			sqlQueries.createANewCollectionEntry(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation)	

		self.idOfCollection = sqlQueries.getCollectionId(self.cursor,self.collectionId)
		sqlQueries.saveQueryParameters(self.cursor, self.idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate)	

	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):
			if len(keywordGroups)>0:
				if isinstance(keywordGroups, str):
					listOfKeywordGroups = [keywordGroups]
				else:
					listOfKeywordGroups=keywordGroups	
			
				for group in listOfKeywordGroups:
					print(str(group))
					sqlQueries.deleteASpecificParameter(cursor, str(self.idOfCollection), group)

			sqlQueries.updateCollectionEntry(cursor, collectionId, nameOfProject, descriptionOfProject,timeStamp)

	def deleteACollection(self):
		sqlQueries.deleteAllParametersOfACollection(self.cursor, str(self.idOfCollection))	
		sqlQueries.deleteCollectionEntry(self.cursor, self.collectionId)	

	def showACollection(self):
		listOfCollectionParameters = sqlQueries.getParametersOfCollection(self.cursor, str(self.idOfCollection))

		tweets=[]
		i=0
		for parameter in listOfCollectionParameters:
			listOfKeywords = parameter[1].split(',')
			listOfListOfKeywords = []
			listOfListOfKeywords.append(listOfKeywords)
			tweetsFromGroup=inputManagment.fetchingTweetsContainingGroups(self.cursor,parameter[3],parameter[2],listOfListOfKeywords, parameter[4], parameter[5])
			numberOfTweets = len(tweetsFromGroup[0])
			noCommaGroupOfTweets = parameter[1].replace(",","")
			parameterData = [noCommaGroupOfTweets, parameter[1],i ,parameter[2], parameter[3], parameter[4], parameter[5], numberOfTweets]
			self.groupOfParameters.append(parameterData)	
			tweets.append(tweetsFromGroup)	
			i+=1		
		tweetList = [tweet for sublist in tweets for tweet in sublist]
		tweetL = [tweet for sublist in tweetList for tweet in sublist]	
			
		index = 5
		collectionDictionary = textCleanUp.dictionaryGen(tweetL,index)

		return collectionDictionary

	def getAllCollections(self):
		collectionsList=sqlQueries.getExistingCollections(self.cursor)

		return collectionsList

	def getAllParameters(self):
		listOfAllParameters = sqlQueries.getAllCollectionParameters(self.cursor)
		index=1
		parametersDictionary = textCleanUp.dictionaryGen(listOfAllParameters, index)
		paramsList = textCleanUp.makeAStringOfKeywordGroups(parametersDictionary)
		print(paramsList)

		return paramsList	

				

		