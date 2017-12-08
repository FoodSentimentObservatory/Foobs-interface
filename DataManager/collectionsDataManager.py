import DataManager.dataManager as dataManager
import processingData.resultsFiltering as resultsFiltering
import databaseConfigurations.config as config
import databaseConfigurations.sqlQueries as sqlQueries

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
        newCollectionDataList = [collection[0], collection[1], collection[2], collection[3], collection[4], collection[5], databaseCollectionName]
        listOfCollectionsWithDb.append(newCollectionDataList)
    conn.close()

def getExistingCollections(cursor):
	listOfCollections = sqlQueries.getExistingCollections(cursor)

	return listOfCollections

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
	sqlQueries.updateCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation)  

def createNewCollection(cursor, collectionId, collectionName, collectionDescription,dateOfCreation):
	sqlQueries.createANewCollectionEntry(cursor, collectionId, collectionName, collectionDescription,dateOfCreation)	

def saveCollectionParameters(cursor, idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate):
	sqlQueries.saveQueryParameters(cursor, idOfCollection, groupOfKeywords, searchQuery, location, fromDate, toDate)

def deleteASpecificParameter(cursor, idOfCollection, group):
	sqlQueries.deleteASpecificParameter(cursor, idOfCollection, group)		

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