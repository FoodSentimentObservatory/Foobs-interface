import sqlQueries
import config
import html
import re
import textCleanUp
import json

def fetchingTweetsContainingGroups(cursor,location,searchQuery,listOfGroups, fromDate, toDate):
    row=[]
    print(len(listOfGroups))
  
    for group in listOfGroups:
        groupRow= groupSearch(cursor, location,searchQuery, group,  fromDate, toDate)        
        row.append(groupRow)
           
    print("Found a total of "+str(len(row))+" tweets.")    
    return row                        
#function to search for tweets containing a group of keywords
def groupSearch(cursor, location,searchQuery, group, fromDate, toDate):
    print("searching for group:")
    print (group)
    rowL=[]
    groupRow=[]
    strGroupOfTweets = ''.join(group)
    noCommaGroupOfTweets = strGroupOfTweets.replace(',','')
    #for eah word, fetch all tweets containing the word
    for word in group:
        word = word.replace("+", " ")
        print (word)
        result = sqlQueries.locationQueryKeyword(cursor, word,searchQuery, location, fromDate, toDate)
        print(len(result))
        for r in result:
            rowL.append(r) 
         
    print("Found "+str(len(rowL))+" total results for the group")    
    #setting a treshhold for filtering so that from all the tweets, we'll only..
    #..get the ones containing all words from the group
    treshhold = len(group)
    print (treshhold)
    listOfTweetIDs = []
    for tweet in rowL:                 
                textOr=tweet[2].replace("\n"," ")
                text=html.escape(textOr,quote=True)
                
                displayName = html.escape(tweet[9],quote=True)
                tweetID = tweet[4]
                count=0       
                alreadySeen=[]

                date = tweet[3].rpartition('.')[0]
                #for each word in the grop, checking if it exists in the text..
                #if it does, one up the counter and search for the next word in the group
                #if a word appears twice in tweet, we only count it once
                for word in group:
                    regex = r'\b'+word+'\\b'
                    listL=re.findall(regex,tweet[2].lower())
                    if  len(listL)>0 and str(word) not in alreadySeen:
                        alreadySeen.append(word)
                        count+=1    
                #once the treshhold is reached and the tweet hasn't been added yet..
                #..add it to a list        
                if count==treshhold and tweetID not in listOfTweetIDs:
                    if tweet[8]==False:
                        verified="False"
                    elif tweet[8]==True:
                        verified="True"    
                    filteredTextTweet=[text,date,tweet[5],verified,displayName,noCommaGroupOfTweets,strGroupOfTweets] 
                    listOfTweetIDs.append(tweetID) 
                    groupRow.append(filteredTextTweet)
    print ("Found "+str(len(groupRow))+" tweets containing all words from the group")   
    print ("-------------------------------------S")

    return groupRow
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
        newNoteTup = (note[0],note[1],note[2],idstr, note[3],note[4],note[5],note[6], note[7], note[8],note[9],note[10],note[11],keywordListId)
        newNoteList.append(newNoteTup)
        n+=1
    #creating a dictionary, key is the sprint    
    i = 4
    dicNotes = textCleanUp.dictionaryGen(newNoteList,i)

    return dicNotes
#helper function to connect to each database, pull the search notes from it and gather all relevant search data
def getSprintNotes(sprintDb, sprint):
    conn = sqlQueries.connectionToDatabaseTest(sprintDb)
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
            earliestSearchDate = sqlQueries.getEarliestDate(cursor,newNoteM,location)
            mostRecentDate = sqlQueries.getMostRecentDate(cursor,newNoteM,location)

            dateEarliest = earliestSearchDate.rpartition('.')[0]
            dateRecent = mostRecentDate.rpartition('.')[0]
            firstSearchDate = sqlQueries.getFirstSearchDate(cursor,newNoteM,location)
            lastSearchDate = sqlQueries.getLastSearchDate(cursor,newNoteM,location)

            countOfSearches = sqlQueries.getCountOfSearches(cursor, newNoteM, location)
            countOfSearchesInt = countOfSearches[0][0]

            firstSearchDateModified = firstSearchDate[0][0].rpartition('.')[0]
            lastSearchDateModified = lastSearchDate[0][0].rpartition('.')[0]
            #using a function to pull the search keyword strings for each sprint
            keywords = getSprintQueryKeywords(cursor,newNoteM,location)
            count = sqlQueries.getCount(cursor, newNoteM,location)
            countInt = count[0][0]
            countWithCommas = '{0:,}'.format(countInt)
            print(newNote)
            print(sprintDb)
            print(keywords)
            print(countWithCommas)
            print(coordinates)
            print(countOfSearchesInt)
            print("--------------------------")
            #for each note we create a tuple containing data to display
            noteTup = (newNote, sprint, location,sprintDb,dateEarliest,dateRecent,keywords,countWithCommas,coordinates,firstSearchDateModified,lastSearchDateModified,countOfSearchesInt)
            newSprintNoteList.append(noteTup)
            alreadySeenNotes.append(newNote)
      
    return newSprintNoteList 
    conn.close()
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
                w = textCleanUp.extraCharRemoval(w, charList,check)
                wNew = w.replace("'",' ')
                if wNew not in queryList:
                    queryList.append(wNew)
    #sorting list aplhabetically, ignoring whether word starts with capital or small letter            
    sortedEditedQuery = sorted(queryList, key=str.lower)
    queryString = '; '.join(sortedEditedQuery)

    return queryString
#function that retrieves the coordinates for a given search
def getCoordinates(cursor, newNoteM, location):
        coordinates = sqlQueries.getLocationOfSearch(cursor, newNoteM, location)

        return coordinates
#function to retrieve all collections from all databases
def getCollectionsFromAllDbs():
    listOfCollectionsWithDb = []
    listOfDbNames=config.getAllDatabases()
    for db in listOfDbNames:
        getListOfCollection(db[1],listOfCollectionsWithDb)
    i=6
    dicCollections = textCleanUp.dictionaryGen(listOfCollectionsWithDb,i)

    return dicCollections
#gets the collections for a given database
def getListOfCollection(database, listOfCollectionsWithDb):
    conn = sqlQueries.connectionToDatabaseTest(database)
    cursor = conn.cursor()

    collectionsData = sqlQueries.getExistingCollections(cursor)
    for collection in collectionsData:
        databaseCollectionName = database+"_collection"
        newCollectionDataList = [collection[0], collection[1], collection[2], collection[3], collection[4], collection[5], databaseCollectionName]
        listOfCollectionsWithDb.append(newCollectionDataList)


    conn.close()