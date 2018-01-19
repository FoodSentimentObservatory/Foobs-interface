import spacy
import re
from spacy.attrs import ORTH
from spacy import en
import sys
import os
from operator import itemgetter
import processingData.spacyStopWords as spacyStopWords
from itertools import groupby
import html

#function to remove stop words, urls, punctuation, numbers and symbols using spacy. Goes through each tweet text and appends the result to two lists, one for the tweet and one for general statistics
#removing also words like e.coli?
def textCleanup(allWords,text):
    for word in text:
            words = replaceChars('@', '', str(word))
            if word.is_stop != True and word.like_url != True and word.is_punct !=True and word.like_num != True and words.isalpha()== True and len(words)> 1:
                allWords.append(words.lower())          

#removes retweets*
#* if we don't have the original tweet text, one retweet can get through the filtering..
# ..the retweet is stripped from the 'rt' and any mentions and the remaining string is compared to a list of originals
def removeDupsAndRetweets(text, origTexts,retweetTexts):
    textList = text.split()
    textStrList = [word for word in textList if word.isalpha()]
    textStrRt = ' '.join(textStrList)
    textStr = replaceChars("rt", '', textStrRt)
    textStrStripped = textStr.strip()

    if textList[0]=="rt":
        if textStrStripped in origTexts:
            retweetTexts.append(textStrStripped)
            include = False
        else:
            origTexts.append(textStrStripped)
            include = True

    elif textList[0]!="rt" and textStrStripped not in origTexts:
        origTexts.append(textStrStripped)
        include = True
    else:
        include = False    

    return include
#make any links in the tweet bodies clickable
def clickableLinks(item):
    r = re.compile(r"(https://[^ ]+)")
    text= r.sub(r'<a href="\1">\1</a>', item)   

    return text 
#function to remove any extra characters from a string
def extraCharRemoval(item, charList,check):
    for ch in charList:
        if ch in item:
            item=replaceChars(ch, "", item)
    if check==0:        
        itemS=item[1:]   
    elif check==1:
        itemS=item[1:-1] 
    else:
        itemS=item          

    return itemS

def replaceChars(oldChar, newChar, text):
    item=text.replace(oldChar,newChar)

    return item

def addTweetToNewGroupsList(word,tweet,groupIdStr,newGroups):
    groupId=groupIdStr+word
    textWithLinks = clickableLinks(tweet[0])
    tweetWithWord = [tweet[0], tweet[1], tweet[2], tweet[3], tweet[4],word,groupId,tweet[7],textWithLinks]
    newGroups.append(tweetWithWord)    
#generate a dictionary given a list and an index number
def dictionaryGen(tweetGroups,i):
    dicw={}
    f = lambda x: x[i]
    #putting the tweets in dictionary, split by keywordGroupId
    for key, group in groupby(sorted(tweetGroups, key=f), f):
        dicw[key] = list(group) 

    return dicw    
#take a dictionary of collections and their keywords and for...
# each collection concatenate all the keyword groups into one string
# used for javaScript
def makeAStringOfKeywordGroups(parametersDictionary):
        paramsList = []
        for key, value in parametersDictionary.items():
            paramsString = ""
            i = 0
            for group in value:
                if i == 0:
                    paramsString = group[0]
                else: 
                    paramsString = paramsString + ";" + group[0]
                i+=1
            paramsSublist = [key,paramsString]
            paramsList.append(paramsSublist)

        return paramsList    
#replaces new lines in tweets with a space
def removeHtmlChars(text):
    textNoNewLines = replaceChars("\n", " ", text)
    textNoHtmlChars=html.escape(textNoNewLines,quote=True)  

    return  textNoHtmlChars    

def findKeywordsInText(text, keywordGroup):
    alreadySeenWords = []
    count = 0
    #for each word in the grop, checking if it exists in the text..
    #if it does, one up the counter and search for the next word in the group
    #if a word appears twice in tweet, we only count it once  
    for word in keywordGroup:
        checkIfExists = findWordInText(word, alreadySeenWords, text)
        count += checkIfExists         
    return count   
#searches for word in text, the word cannot be part of a bigger word
#but the regex matches hashtags and punctuation signs
def findWordInText(word, alreadySeenWords, text):
    count = 0
    regex = r'\b'+word.strip()+'\\b'
    listL=re.findall(regex,text.lower())
    if  len(listL)>0 and str(word) not in alreadySeenWords:
        alreadySeenWords.append(word)
        count=1 
  
    return count         
#checks if a user is verified
def checkIfVerified(verifiedValue):
    if verifiedValue==False:
        verified="False"
    elif verifiedValue==True:
        verified="True"  

    return verified   
#takes the group input that has been given by the user in the
#keywordSearch page and makes into a list. If the input is equal to:
#'no groups', the list only contains the phrase all tweets, which means
#that the rest of the code will ignore the keyword input
def splitStrOfGroups(group):
    listOfGroups = []
    if isinstance(group, str):
        if (group != 'no groups'):
            listofwords = group.split(",")
            cleanListOfWords = getCleanPhrasesAndWords(listofwords)
            listOfGroups.append(cleanListOfWords)
        else:
            listOfGroups=['all tweets'] 
    else:
        for g in group:
            if g!= "":
                cleanListOfWords = getCleanPhrasesAndWords(g)
                listOfGroups.append(cleanListOfWords)        

    return listOfGroups            

def addNewKeywordGroups(group, keywordsToCluster):    
    newKeywordGroupList = []
    keywordsToClusterList = keywordsToCluster.split(',')
    print (keywordsToClusterList)
    keywordsOfDataSet = splitStrOfGroups(group)
    for keyword in keywordsToClusterList:
        for word in keywordsOfDataSet:
            newKeywordGroup = [keyword]
            for w in word:
                newKeywordGroup.append(w)
            newKeywordGroupList.append(newKeywordGroup)

    return newKeywordGroupList    
#if keyword groups have been specified by the user in the keywordSearch page
#when clustering has been selected as a function, the keyword groups are turned
#into a readable logical string here to be displayed on the clustersStatsPage
def getKeywordContraintString(group):
    listOfGroups = splitStrOfGroups(group)
    intermediateListOfGroups = []
    for g in listOfGroups:
        gStr = ' AND '.join(g)
        intermediateListOfGroups.append(gStr)

    listOfGroupsStr = '; '.join(intermediateListOfGroups)

    return listOfGroupsStr    
#generates a link for the tweet on twitter
def getTwitterLink(tweetId,userHandle):
    twitterLink = "https://twitter.com/"+userHandle+"/status/"+str(tweetId)

    return twitterLink    
#function to split a string into a list, takes split character as a variable
#as different strings can be split by different characters
def createKeywordList(keywords, splitChar):
    if isinstance(keywords, str):
        keywords=keywords.replace("\n","")
        keywords = keywords.replace("\r","")
        if " OR " in keywords:
            keywordList = []
            groupList = keywords.split(" OR ")
            for group in groupList:
                keywordGroup = group.split(splitChar)
                keywordList.append(keywordGroup)
        else:     
            keywordList = keywords.split(splitChar)
    else:
        keywordList=keywords 

    return keywordList      
#adds clickable links to each tweet list for display
def addClickableLinks(tweets):
    tweetList=[]

    #for each group of tweets (all tweets fetched for one group of keywords)
    for groupOfTweets in tweets:
        for tweet in groupOfTweets:
            tweetL = list(tweet)
            #making links clickable
            text = clickableLinks(tweetL[0])
            tweetL.append(text)
            #sending the tweets to a list
            tweetList.append(tweetL)

    return tweetList 
#function to filter tweets for donut display, currently used when 
#collection option has been selected for donut vis
def filterTweets(tweetsDictionary, keywordsToClusterEnriched):
        newListOfTweets = [] 
        for key, value in tweetsDictionary.items():
            for tweet in value:
                for wordList in keywordsToClusterEnriched:
                        count = findKeywordsInText(tweet[0],wordList)
                        if count==len(wordList):
                            wordStr=','.join(wordList)
                            wordKeyStr = ''.join(wordList)
                            newTweetList = [tweet[0],tweet[1],tweet[2],tweet[3],tweet[4],tweet[5], wordStr, tweet[7],tweet[8],wordKeyStr]
                            newListOfTweets.append(newTweetList)                
        index = 9
        newTweetsDictionary = dictionaryGen(newListOfTweets,index)

        return  newTweetsDictionary                

def makeToList(keywordClusterList):
    newKeywordList = []
    for group in keywordClusterList:
        if "+" in group:
            groupList = group.split("+")
        else:
            groupList = [group] 

        newKeywordList.append(groupList)  

    return newKeywordList     

def getCleanPhrasesAndWords(group):
    listOfCleanPhrasesAndWords = []
    if isinstance(group, str):
        cleanPhrase(group,listOfCleanPhrasesAndWords)
    else:    
        for word in group:      
            cleanPhrase(word,listOfCleanPhrasesAndWords)

    return listOfCleanPhrasesAndWords

def cleanPhrase(phrase,listOfCleanPhrasesAndWords):
    #checking if it's not an empty string
    #e.g. the user has opened two keyword fields, but only typed
    #in one and left the other one blanc
    if phrase != "":
        #removing the +s from phrases and replacing them with spaces
        cleanPhrase = replaceChars("+", " ", phrase)
        listOfCleanPhrasesAndWords.append(cleanPhrase)        