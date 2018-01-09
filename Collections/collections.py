import DataManager.collectionsDataManager as collectionsDataManager
import DataManager.tweetsDataManager as tweetsDataManager
import processingData.resultsFiltering as resultsFiltering
import DataManager.dataManager as dataManager

#class that contains the methods for collections
class Collection():
	def __init__(self, collectionId, cursor):
		self.collectionId = collectionId
		self.cursor = cursor
		self.idOfCollection = collectionsDataManager.getCollectionId(self.cursor,self.collectionId)
		self.groupOfParameters = []
		self.collectionName = collectionsDataManager.getCollectionName(cursor, str(self.collectionId))
	#function checks if a collection already exists, if it does, it updates it, if not it creates a new collection entry
	#also saves the new parameters to the parameters table	
	def saveCollection(self, collectionName, collectionDescription, dateOfCreation, groupOfKeywords, searchQuery, location, fromDate, toDate, tweetsCount):
		checkIfExists = collectionsDataManager.searchForCollection(self.cursor,self.collectionId)
		if len(checkIfExists)>0:
			collectionsDataManager.updateExistingCollection(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation)
			collectionsDataManager.setTotalTweetCountOfACollection(self.cursor, tweetsCount, self.collectionId)
		else:
			collectionsDataManager.createNewCollection(self.cursor, self.collectionId, collectionName, collectionDescription,dateOfCreation, tweetsCount)	

		self.idOfCollection = collectionsDataManager.getCollectionId(self.cursor,self.collectionId)
		collectionsDataManager.saveCollectionParameters(self.cursor, self.idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate, tweetsCount)	
	#updates a collection, triggered by the update modal on the collections page
	#if specified any, removes parameters for the given collection	
	def updateCollection(self, collectionId, timeStamp, nameOfProject, descriptionOfProject,keywordGroups):		
			if isinstance(keywordGroups, str):
				listOfKeywordGroups = [keywordGroups]
			else:
				listOfKeywordGroups=keywordGroups	
			
			for group in listOfKeywordGroups:
				print(str(group))
				countOfTweets = collectionsDataManager.getParameterTweetCount(self.cursor, str(self.idOfCollection), group)
				collectionsDataManager.decreaseTotalTweetCountOfACollection(self.cursor, countOfTweets, self.collectionId)
				collectionsDataManager.deleteASpecificParameter(self.cursor, str(self.idOfCollection), group)

			collectionsDataManager.updateExistingCollection(self.cursor, self.collectionId, nameOfProject, descriptionOfProject,timeStamp)
	#deletes a collection from the collections table and its parameters from the parametersForCollections table		
	def deleteACollection(self):
		collectionsDataManager.deleteAllParametersOfACollection(self.cursor, str(self.idOfCollection))	
		collectionsDataManager.deleteCollectionEntry(self.cursor, self.collectionId)	
	#fetches the tweets related to that collection from the database and displays them	
	def showACollection(self):
		listOfCollectionParameters = self.getAllCollectionParamters()
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
		tweetL = resultsFiltering.addClickableLinks(tweetList)	
			
		index = 5
		collectionDictionary = resultsFiltering.dictionaryGen(tweetL,index)

		return collectionDictionary
	#fetches a list of all collections available in the database	
	def getAllCollections(self):
		collectionsList=collectionsDataManager.getExistingCollections(self.cursor)

		return collectionsList
	#fetches all parameters from the parameters table in the db, used for the collections page	
	def getAllParameters(self):
		listOfAllParameters = collectionsDataManager.getAllCollectionParameters(self.cursor)
		index=1
		parametersDictionary = resultsFiltering.dictionaryGen(listOfAllParameters, index)
		paramsList = resultsFiltering.makeAStringOfKeywordGroups(parametersDictionary)
		print(paramsList)

		return paramsList

	def getAllCollectionParamters(self):		
		listOfCollectionParameters = collectionsDataManager.getParametersOfCollection(self.cursor, str(self.idOfCollection))

		return listOfCollectionParameters

	def getAllCollectionParametersKeywords(self):
		listOfCollectionParameters = self.getAllCollectionParamters()

		collectionKeywordStr = ""
		i=0
		for parameter in listOfCollectionParameters:
			if i==0 or i==len(listOfCollectionParameters):
				collectionKeywordStr += parameter[1]
			else:
				collectionKeywordStr = collectionKeywordStr + " OR " + parameter[1]

			i+=1	

		return collectionKeywordStr			
				

		