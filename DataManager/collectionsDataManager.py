import DataManager.dataManager as dataManager
import processingData.resultsFiltering as resultsFiltering
import databaseConfigurations.config as config
import databaseConfigurations.sqlQueries as sqlQueries
#contains functions for fetching collection data from the db

#function to retrieve all collections from all databases
def getCollectionsFromAllDbs():
    listOfCollectionsWithDb = []
    listOfDbNames=config.getAllDatabases()
    for db in listOfDbNames:
        getListOfCollection(db[1],listOfCollectionsWithDb)
    i=6
    dicCollections = resultsFiltering.dictionaryGen(listOfCollectionsWithDb,i)

    return dicCollections
#gets the collections for a given database
def getListOfCollection(database, listOfCollectionsWithDb):
    conn = dataManager.startDbConnection(database)
    cursor = conn.cursor()

    collectionsData = getExistingCollections(cursor)
    for collection in collectionsData:
        databaseCollectionName = database+"_collection"
        clusterRadioDbName = database+"_collection_forCluster"
        newCollectionDataList = [collection[0], collection[1], collection[2], collection[3], collection[4], collection[5], databaseCollectionName,clusterRadioDbName,collection[6]]
        listOfCollectionsWithDb.append(newCollectionDataList)
    conn.close()

def getExistingCollections(cursor):
	listOfCollections = sqlQueries.getExistingCollections(cursor)
	listOfCollectionsFixed = []
	for collection in listOfCollections:
			collectionName = resultsFiltering.replaceChars('"', "", collection[1])
			collectionDescription = resultsFiltering.replaceChars('"', "", collection[3])
			collectionList = [collection[0], collectionName,collection[2], collectionDescription, collection[4],collection[5],collection[6]]
			listOfCollectionsFixed.append(collectionList)
	return listOfCollectionsFixed

def getCollectionId(cursor, collectionId):
	idOfCollection = sqlQueries.getCollectionId(cursor,collectionId) 

	return idOfCollection

def getCollectionName(cursor, collectionId):
	collectionName = sqlQueries.getCollectionName(cursor, collectionId)

	return collectionName

def searchForCollection(cursor, collectionId):
	check = sqlQueries.searchForUniqueId(cursor,collectionId)	

	return check	

def updateExistingCollection(cursor, collectionId, collectionName, collectionDescription,dateOfCreation):
	collectionName = resultsFiltering.replaceChars("'", '"', collectionName)
	collectionDescription = resultsFiltering.replaceChars("'", '"', collectionDescription)
	sqlQueries.updateCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation)  

def createNewCollection(cursor, collectionId, collectionName, collectionDescription,dateOfCreation, tweetCount):
	collectionName = resultsFiltering.replaceChars("'", '"', collectionName)
	collectionDescription = resultsFiltering.replaceChars("'", '"', collectionDescription)
	sqlQueries.createANewCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation, tweetCount)	

def saveCollectionParameters(cursor, idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate, tweetCount,retweets):
	sqlQueries.saveQueryParameters(cursor, idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate, tweetCount,retweets)

def deleteASpecificParameter(cursor, idOfCollection, group):
	if group != '0':
		sqlQueries.deleteASpecificParameter(cursor, idOfCollection, group)
	else:
		print('No paramters to delete selected.')			

def deleteAllParametersOfACollection(cursor, idOfCollection):
	sqlQueries.deleteAllParametersOfACollection(cursor, idOfCollection)

def deleteCollectionEntry(cursor, collectionId):
	sqlQueries.deleteCollectionEntry(cursor, collectionId)	

def getParametersOfCollection(cursor, idOfCollection):
	listOfCollectionParameters = sqlQueries.getParametersOfCollection(cursor, idOfCollection)

	return listOfCollectionParameters

def getAllCollectionParameters(cursor):
	listOfAllParameters = sqlQueries.getAllCollectionParameters(cursor)	

	return listOfAllParameters

def setTotalTweetCountOfACollection(cursor, tweetCount, collectionID):
	sqlQueries.setTotalTweetCountOfACollection(cursor, tweetCount, collectionID)	

def getParameterTweetCount(cursor, uniqueIdentifier, keywordGroup):
	if keywordGroup!= '0':
		countOfTweets = sqlQueries.getParameterTweetCount(cursor, uniqueIdentifier, keywordGroup)
	else:
		countOfTweets = '0'	
	return countOfTweets	

def decreaseTotalTweetCountOfACollection(cursor, tweetCount, collectionID):
	sqlQueries.decreaseTotalTweetCountOfACollection(cursor, tweetCount, collectionID)	