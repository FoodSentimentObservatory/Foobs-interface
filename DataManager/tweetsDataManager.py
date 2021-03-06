import databaseConfigurations.sqlQueries as sqlQueries
import re
import processingData.resultsFiltering as resultsFiltering

def fetchingTweetsContainingGroups(cursor,location,searchQuery,listOfGroups, fromDate, toDate, retweets):
    allTweetResults=[]
    for group in listOfGroups:      
        groupTweetsResult= groupSearch(cursor, location,searchQuery, group,  fromDate, toDate,retweets)        
        allTweetResults.append(groupTweetsResult)
               
    return allTweetResults                        
#function to search for tweets containing a group of keywords
def groupSearch(cursor, location,searchQuery, group, fromDate, toDate, retweets):
    print("searching for group:")
    print (group)
    retweets = retweets.strip()
    tweetsList=getTweetsList(cursor,group, searchQuery, location, fromDate, toDate)
    groupTweetsResult=[]
    if group != 'all tweets':
        treshhold = len(group)
        strGroupOfTweets = ''.join(group)
        charList = [",", " "]
        noCommaGroupOfTweets = resultsFiltering.extraCharRemoval(strGroupOfTweets, charList,2)
    else:
        treshhold = 0  
        strGroupOfTweets = group
        noCommaGroupOfTweets = 'alltweets'       
    print("Found "+str(len(tweetsList))+" total results for the group")    
    #setting a treshhold for filtering so that from all the tweets, we'll only..
    #..get the ones containing all words from the group    
    listOfTweetIDs = []
    listOfOriginalTweetBodies = []
    listOfRetweetTweetBodies = []
    for tweet in tweetsList:                 
                tweetID = tweet[4]
                if treshhold > 0:
                    count=resultsFiltering.findKeywordsInText(tweet[2], group) 
                else:
                    count= 0                        
                #once the treshhold is reached and the tweet hasn't been added yet..
                #..add it to a list        
                if count==treshhold and tweetID not in listOfTweetIDs:
                    if retweets == "N":
                        includeRetweets = resultsFiltering.removeDupsAndRetweets(tweet[2].lower(), listOfOriginalTweetBodies,listOfRetweetTweetBodies)
                    else:
                        includeRetweets = True

                    if includeRetweets== True:
                        linkToTweet = resultsFiltering.getTwitterLink(tweetID,tweet[5])        
                        text = resultsFiltering.removeHtmlChars(tweet[2]) 
                        date = tweet[3].rpartition('.')[0]          
                        displayName = resultsFiltering.removeHtmlChars(tweet[9])
                        verified = resultsFiltering.checkIfVerified(tweet[8])   
                        filteredTextTweet=[text,date,tweet[5],verified,displayName,noCommaGroupOfTweets,strGroupOfTweets,linkToTweet] 
                        listOfTweetIDs.append(tweetID) 
                        groupTweetsResult.append(filteredTextTweet)
    print ("Found "+str(len(groupTweetsResult))+" tweets containing all words from the group")   
    print ("-------------------------------------S")

    return groupTweetsResult
#fetching all tweets for each word in a group of keywords
def getTweetsList(cursor,keywordGroup, searchQuery, location, fromDate, toDate):
    resultsList = []
    #for each word, fetch all tweets containing the word
    if keywordGroup != 'all tweets':
        for word in keywordGroup:
            word = resultsFiltering.replaceChars("+", " ", word)
            print (word)
            result = sqlQueries.locationQueryKeyword(cursor, word,searchQuery, location, fromDate, toDate)
            print(len(result))
            #we loop through the results so that we can avoid having a list of lists of tweets
            for r in result:
                resultsList.append(r)
    #if no keyword groups specified, fetch all tweets from the selected search, in the given timeframe
    #by default the timeframe is first tweet to last tweet               
    else:
        resultsList=sqlQueries.retrieveAllTweetsFromTimeframe(cursor,searchQuery, location, fromDate, toDate)             

    return resultsList           
