import databaseConfigurations.sqlQueries as sqlQueries
import re
import processingData.resultsFiltering as resultsFiltering

def fetchingTweetsContainingGroups(cursor,location,searchQuery,listOfGroups, fromDate, toDate):
    allTweetResults=[]
    print(len(listOfGroups))
  
    for group in listOfGroups:
        groupTweetsResult= groupSearch(cursor, location,searchQuery, group,  fromDate, toDate)        
        allTweetResults.append(groupTweetsResult)
           
    print("Found a total of "+str(len(allTweetResults))+" tweets.")    
    return allTweetResults                        
#function to search for tweets containing a group of keywords
def groupSearch(cursor, location,searchQuery, group, fromDate, toDate):
    print("searching for group:")
    print (group)
    tweetsList=getTweetsList(cursor,group, searchQuery, location, fromDate, toDate)
    groupTweetsResult=[]
    strGroupOfTweets = ''.join(group)
    noCommaGroupOfTweets = resultsFiltering.replaceChars(',', '', strGroupOfTweets)
           
    print("Found "+str(len(tweetsList))+" total results for the group")    
    #setting a treshhold for filtering so that from all the tweets, we'll only..
    #..get the ones containing all words from the group
    treshhold = len(group)

    listOfTweetIDs = []
    for tweet in tweetsList:                 
                text = resultsFiltering.removeHtmlChars(tweet[2])           
                displayName = resultsFiltering.removeHtmlChars(tweet[9])
                tweetID = tweet[4]
                date = tweet[3].rpartition('.')[0]

                count=resultsFiltering.findKeywordsInText(tweet[2], group)       
 
                #once the treshhold is reached and the tweet hasn't been added yet..
                #..add it to a list        
                if count==treshhold and tweetID not in listOfTweetIDs:
                    verified = resultsFiltering.checkIfVerified(tweet[8])   
                    filteredTextTweet=[text,date,tweet[5],verified,displayName,noCommaGroupOfTweets,strGroupOfTweets] 
                    listOfTweetIDs.append(tweetID) 
                    groupTweetsResult.append(filteredTextTweet)
    print ("Found "+str(len(groupTweetsResult))+" tweets containing all words from the group")   
    print ("-------------------------------------S")

    return groupTweetsResult

def getTweetsList(cursor,keywordGroup, searchQuery, location, fromDate, toDate):
    resultsList = []
    #for eah word, fetch all tweets containing the word
    for word in keywordGroup:
        word = resultsFiltering.replaceChars("+", " ", word)
        print (word)
        result = sqlQueries.locationQueryKeyword(cursor, word,searchQuery, location, fromDate, toDate)
        print(len(result))
        for r in result:
            resultsList.append(r)  

    return resultsList           
