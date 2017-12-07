import databaseConfigurations.config as config
import pymssql
#connecting to database
def connectionToDatabaseTest(dbName):
    server = config.dbServer()
    databased = dbName
    portd = config.databasePort()
    #connection to the database
    conn = pymssql.connect(server,database=databased,port=portd,autocommit=True)
    #cursor = conn.cursor()
    print ("Connection to Database " +dbName+" was successfull")

    return conn

def closeDbConnection():
    conn = connectionToDatabase.conn
    conn.close()    

#collecting all tweets from a given search from a given location containing a given keyword
def locationQueryKeyword(cursor, keyword,searchDescription, location, fromDate, toDate):
     cursor.execute("SELECT [Post].[Id],[Post].[hasCreator],\
     [Post].[body], [Post].[createdAt], [Post].[platformPostID],\
     [UserAccount].[platformAccountId],[Search].[Note], [Post].[SearchId],\
     [UserAccount].[verified],[UserAccount].[displayName] \
     FROM [Post]\
     INNER join [Search] ON [Post].[SearchId]=[Search].Id\
     INNER join [UserAccount] ON [UserAccount].[Id]= [Post].[hasCreator]\
     WHERE [Search].[Note] LIKE '%"+ searchDescription +"%' AND [Search].[Note] LIKE '%"+ location +"%'\
     AND [Post].[body] LIKE '%" + keyword +"%'\
     AND [Post].[createdAt]>= '"+fromDate+"' AND [Post].[createdAt]<='"+toDate+"'\
     ORDER BY [Post].[createdAt] ASC")
     row = cursor.fetchall()

     return row
#collect unique sprint notes
def sprintNotesQuery(cursor,dbName):
    cursor.execute("SELECT Distinct [Search].[Note]  FROM [Search]")

    row = cursor.fetchall()

    return row    
#get the earliest tweet from a search
def getEarliestDate(cursor,queryString,location):
    cursor.execute("SELECT TOP 1 [Post].[createdAt] FROM [Post]\
    INNER join [Search] ON [Post].[SearchId]=[Search].Id\
    WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%' ORDER BY [Post].[createdAt] ASC")
    oldestDate = cursor.fetchall()
    return oldestDate[0][0]
#get the most recent tweet from a search    
def getMostRecentDate(cursor,queryString, location):
    cursor.execute("SELECT TOP 1 [Post].[createdAt] FROM [Post]\
    INNER join [Search] ON [Post].[SearchId]=[Search].Id\
    WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%' ORDER BY [Post].[createdAt] DESC")
    mostRecentDate = cursor.fetchall()

    return mostRecentDate[0][0]
#get the query words for each note
def getQueryKeywords(cursor, queryString, location):
    cursor.execute("SELECT DISTINCT [Search].[Keywords] FROM Search WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%'")

    keywordList = cursor.fetchall()

    return keywordList
#count all unique platformPostIds in the db for a given search string
def getCount(cursor, queryString,location):
    cursor.execute("SELECT COUNT(Distinct platformPostID) From Post INNER JOIN Search ON [Post].[SearchId]=[Search].[Id] where Search.Note like '%"+queryString+"%' AND Search.Note like '%"+location+"%'")

    count = cursor.fetchall()

    return count
#get the coordinates of a search
def getLocationOfSearch(cursor, queryString, location):
    cursor.execute("SELECT Distinct [Search].[radius], [GeoPoint].[latitude], [GeoPoint].[longitude] FROM Search INNER JOIN GeoPoint ON [Search].[LocationId]=[GeoPoint].[locationId] WHERE Search.Note like '%"+queryString+"%' AND Search.Note like '%"+location+"%'")    

    coordinates = cursor.fetchall()

    return coordinates
#get the first search date
def getFirstSearchDate(cursor,queryString,location):    
    cursor.execute("SELECT TOP 1 [Search].[startOfSearch] FROM [Search] WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%' ORDER BY [Search].[startOfSearch] ASC")

    firstSearch = cursor.fetchall()

    return firstSearch
#get the last search date
def getLastSearchDate(cursor,queryString,location):
    cursor.execute("SELECT TOP 1 [Search].[endOfSearch] FROM [Search] WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%' ORDER BY [Search].[endOfSearch] DESC")

    lastSearchDate = cursor.fetchall()

    return lastSearchDate    
#count the times searches for a given discourse have been performed
def getCountOfSearches(cursor, queryString, location):
    cursor.execute("SELECT  COUNT(*) FROM\
        (SELECT  DISTINCT StartOfSearch, Note\
        FROM [Search]\
        WHERE [Search].[Note] LIKE '%"+queryString+"%' AND [Search].[Note] LIKE '%"+location+"%') a") 

    countOfSearches = cursor.fetchall()

    return countOfSearches   
#fetch all the existing collections from the database
def getExistingCollections(cursor):
    cursor.execute("SELECT * FROM [Collections]")   

    listOfCollections = cursor.fetchall()

    return listOfCollections 
#returns a specific collection
def searchForUniqueId(cursor,collectionId):
    cursor.execute("SELECT * FROM [Collections] WHERE [Collections].[uniqueIdentifier] ='"+collectionId+"'")   

    collection = cursor.fetchall()

    return collection 
#updates a collection
def updateCollectionEntry(cursor, collectionIds, collectionNames, collectionDescriptions,dateOfCreation):
    cursor.execute("UPDATE [Collections] SET [Description] = '%s', [collectionName] = '%s', [lastUpdated] = '%s' WHERE [uniqueIdentifier] = '%s'"%(collectionDescriptions,collectionNames,dateOfCreation,collectionIds))
    print("entry updated")    
#creates a new collection
def createANewCollectionEntry(cursor, collectionIds, collectionNames, collectionDescriptions,dateOfCreation):
    sql = "INSERT INTO [Collections] ([Description],[uniqueIdentifier],[collectionName],[dateCreated]) VALUES (%s,%s,%s,%s)" 
    cursor.execute(sql,(collectionDescriptions,collectionIds,collectionNames,dateOfCreation))
    print("entry created")    
#deletes a collection
def deleteCollectionEntry(cursor, collectionId):
    cursor.execute("DELETE FROM [Collections] WHERE [uniqueIdentifier] = '"+collectionId+"'")   
    print ("entry deleted") 
#deletes all parameters that are linked to a collection
def deleteAllParametersOfACollection(cursor, collectionId):
        cursor.execute("DELETE FROM [ParametersForCollections] WHERE [collectionId] = '"+collectionId+"'")
        print("parameters have been deleted.")
#deletes a specific collection parameter
def deleteASpecificParameter(cursor, uniqueIdentifier, keywordGroup):
    cursor.execute("DELETE FROM [ParametersForCollections] WHERE [collectionId]='"+uniqueIdentifier+"' AND [keywords] ='"+keywordGroup+"'")        
#retrieves the name of a collection
def getCollectionName (cursor, uniqueId):
    cursor.execute("SELECT [CollectionName] FROM [Collections] WHERE [uniqueIdentifier] = '"+uniqueId+"'")  

    collectionName = cursor.fetchall()
    if len(collectionName)>0:
        collectionNameStr = collectionName[0][0]
    else:    
        collectionNameStr=""
        
    return collectionNameStr  
#saves query parameters to database
def saveQueryParameters(cursor, collectionId, keywords, searchQuery, location, fromDate, toDate):
    sql = "INSERT INTO [ParametersForCollections] ([keywords], [searchQuery], [location], [fromDate], [toDate], [collectionId]) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(keywords,searchQuery,location,fromDate,toDate,collectionId))
    print("new keyword group created.")
#retrieves all parameters for a given collection
def getParametersOfCollection(cursor, collectionId):
    cursor.execute("SELECT * FROM [ParametersForCollections] WHERE [collectionId] = '"+collectionId+"'")

    collectionParametersList = cursor.fetchall()

    return collectionParametersList    
#retrieves all parameters from the parameter table
def getAllCollectionParameters(cursor):
    cursor.execute("SELECT [keywords],[collectionId] FROM [ParametersForCollections]")  

    listOfAllParamaters = cursor.fetchall()

    return listOfAllParamaters  
#retrieves the id of a collection
def getCollectionId (cursor, collectionUniqueId):
    cursor.execute("SELECT TOP 1 [Id], [uniqueIdentifier] FROM [Collections] WHERE [Collections].[uniqueIdentifier] = '"+collectionUniqueId+"'")

    collection = cursor.fetchall()
    if len(collection)>0:
        collectionId= collection[0][0]
    else:
        collectionId=1    

    return collectionId    

