import databaseConfigurations.sqlQueries as sqlQueries
import databaseConfigurations.config as config
import html
import re
import processingData.resultsFiltering as resultsFiltering

def startDbConnection(dbName):        
    conn = sqlQueries.connectionToDatabaseTest(dbName) 

    return conn

#gets all db names from the config file and creates a list of dbs
#containing db name, string for an html id tag and a string of all other db names
#which is to be used by the javascript in order to set visibility of divs
def getDBs():
    listOfDBs=[]
    listOfDbNames=config.getAllDatabases()

    for db in listOfDbNames:
        notDbString = ""
        for notDb in listOfDbNames:
            if notDb[1] != db[1]:
                if len(notDbString) == 0:
                    notDbString = notDb[1]
                else:
                    notDbString = notDbString + ";" + notDb[1]    
        idStr = "radio_"+db[1]
        dbTuple = (db[1], idStr, notDbString)    
        listOfDBs.append(dbTuple)

    return listOfDBs    
#main function to get data for each sprint's notes
#loops through each database specified in the config file
def getSearchNotes():
    sprintNotesList = []
    listOfDbNames=config.getAllDatabases()
    for db in listOfDbNames:
        print(db[1])
        sprintName = db[1]
        sprintNotes = getSprintNotes(db[1],sprintName)
        sprintNotesList.append(sprintNotes)

    noteList = [item for sprint in sprintNotesList for item in sprint]
    n=5
    newNoteList =[]
    #giving an id that would be used for the creation of radio buttons in the interface
    for note in noteList:
        idstr= "radio"+str(n)
        keywordListId ="keywordList"+str(n)
        clusterId = "cluster"+str(n)
        keyId = note[3]+"_key"
        clusterKeywordsId = "clusterKeyword"+str(n)
        newNoteTup = (note[0],note[1],note[2],idstr, note[3],note[4],note[5],note[6], note[7], note[8],note[9],note[10],note[11],keywordListId,clusterId,keyId,clusterKeywordsId)
        newNoteList.append(newNoteTup)
        n+=1
    #creating a dictionary, key is the sprint    
    i = 4
    dicNotes = resultsFiltering.dictionaryGen(newNoteList,i)

    return dicNotes
#helper function to connect to each database, pull the search notes from it and gather all relevant search data
def getSprintNotes(sprintDb, sprint):
    conn = startDbConnection(sprintDb)
    cursor = conn.cursor()

    #query to get all unique notes
    sprintNotes = sqlQueries.sprintNotesQuery(cursor, sprintDb)   
    newSprintNoteList=[]
    alreadySeenNotes = []
    #the result is returned in an odd format, so the following lines extract the
    #relevant parts of the search string - discourse and general location
    for note in sprintNotes:
        #sprint one has some random numbers attached to each search note, 
        #hence select distinct doesn't work on it
        if "(" in note[0]:
            newNoteS = note[0].split("(",1)[0]
            searchNote=newNoteS
            newNoteM = newNoteS.split("-")[-1]
            location = note[0].split(" ",1)[0]
            newNote = location + " -"+newNoteM
        else:
            searchNote=note[0]
            newNoteM = str(note[0]).split("-")[-1] 
            locationS = str(note[0]).split("-")[0]
            location = locationS.split(" ")[0]
            newNote = location + " -"+newNoteM        
        #because of the random numbers mentioned above, after we clean the note string
        #we need to check if we've already encoutered it before, if not, continue with the rest    
        if newNote not in alreadySeenNotes:
            coordinates = getCoordinates(cursor, newNoteM, location)
            #getting the earliest and the most recent tweet from db and removing the milliseconds
            dateEarliest = getDate(cursor,newNoteM,location, "earliest")
            dateRecent = getDate(cursor,newNoteM,location, "most recent")

            firstSearchDate = getDate(cursor,newNoteM,location, "first search")
            lastSearchDate = getDate(cursor,newNoteM,location, "last search")

            countOfSearches = sqlQueries.getCountOfSearches(cursor, newNoteM, location)

            #using a function to pull the search keyword strings for each sprint
            keywords = getSprintQueryKeywords(cursor,newNoteM,location)
            count = sqlQueries.getCount(cursor, newNoteM,location)
            countWithCommas = '{0:,}'.format(count)
            print(newNote)
            print(sprintDb)
            print(keywords)
            print(countWithCommas)
            print(coordinates)
            print(countOfSearches)
            print("--------------------------")
            #for each note we create a tuple containing data to display
            noteTup = (newNote, sprint, location,sprintDb,dateEarliest,dateRecent,keywords,countWithCommas,coordinates,firstSearchDate,lastSearchDate,countOfSearches)
            newSprintNoteList.append(noteTup)
            alreadySeenNotes.append(newNote)
      
    return newSprintNoteList 
    conn.close()
#getting the time frames for searches and tweets
def getDate(cursor,searchNote,location, dateType):
    if dateType == "earliest":
        date =  sqlQueries.getEarliestDate(cursor,searchNote,location)
    elif dateType == "most recent":
        date =  sqlQueries.getMostRecentDate(cursor,searchNote,location)
    elif dateType == "first search":
        date = sqlQueries.getFirstSearchDate(cursor,searchNote,location)
    else:
        date = sqlQueries.getLastSearchDate(cursor,searchNote,location)  

    dateMilSecondsRemoved = date.rpartition('.')[0]
    
    return dateMilSecondsRemoved               
#function to pull keyword string for search notes from database and put them together
def getSprintQueryKeywords(cursor,note,location):
    keywordQueryList = sqlQueries.getQueryKeywords(cursor, note, location)
    queryList = []
    for query in keywordQueryList:
        newQuery=[]
        editedQuery = []
        check=2
        #making a list of words and removing extra characters
        for word in query:
            wordList=word.split(" OR ")
            charList = ['"','(',')']
            for w in wordList:
                w = resultsFiltering.extraCharRemoval(w, charList,check)
                cleanWord = resultsFiltering.replaceChars("'", " ", w)
                #wNew = w.replace("'",' ')
                if cleanWord not in queryList:
                    queryList.append(cleanWord)
    #sorting list aplhabetically, ignoring whether word starts with capital or small letter            
    sortedEditedQuery = sorted(queryList, key=str.lower)
    queryString = '; '.join(sortedEditedQuery)

    return queryString
#function that retrieves the coordinates for a given search
def getCoordinates(cursor, newNoteM, location):
        coordinates = sqlQueries.getLocationOfSearch(cursor, newNoteM, location)

        return coordinates
