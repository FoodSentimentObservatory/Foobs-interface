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

#removes duplicating tweets (based on platfrom ID) and retweets*
#* if we don't have the original tweet text, one retweet can get through the filtering..
# ..the retweet is stripped from the 'rt' and any mentions and the remaining string is compared to a list of originals
def removeDupsAndRetweets(row, location):
    twitterIDs = []
    origTexts = []
    retweetTexts = []
    rowS=[]
    i = 0
    sortedRow = sorted(row, key=itemgetter(3))
    for r in sortedRow:
        i = i+1
        if r[4] not in twitterIDs:
            twitterIDs.append(r[4])
            text = r[2].lower()
            textList = text.split()
            textStrList = [word for word in textList if word.isalpha()]
            textStrRt = ' '.join(textStrList)
            textStr = replaceChars("rt", '', textStrRt)
            textStrStripped = textStr.strip()
            if textList[0]=="rt":
                if textStrStripped in origTexts:
                    retweetTexts.append(textStrStripped)
                else:
                    origTexts.append(textStrStripped)
                    rowS.append(r)

            elif textList[0]!="rt" and textStrStripped not in origTexts:
                origTexts.append(textStrStripped)
                rowS.append(r)

        if i%10000==0:
            print("processed "+ str(i) +  " tweets")

    print ("All tweets from "+location+" have been processed.")

    return rowS
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
    tweetWithWord = [tweet[0], tweet[1], tweet[2], tweet[3], tweet[4],word,groupId]
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

def findWordInText(word, alreadySeenWords, text):
    count = 0
    regex = r'\b'+word.strip()+'\\b'
    listL=re.findall(regex,text.lower())
 
    if  len(listL)>0 and str(word) not in alreadySeenWords:
        alreadySeenWords.append(word)
        count=1 
  
    return count         

def checkIfVerified(verifiedValue):
    if verifiedValue==False:
        verified="False"
    elif verifiedValue==True:
        verified="True"  

    return verified   

def splitStrOfGroups(group):
    listOfGroups = []
    if isinstance(group, str):
        if (group != 'no groups'):
            listofwords = group.split(",")
            listOfGroups.append(listofwords)
        else:
            listOfGroups=['all tweets'] 
    else:
        for g in group:
            singleGroup = g.split(",")
            listOfGroups.append(singleGroup)

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
            print(newKeywordGroup)
            newKeywordGroupList.append(newKeywordGroup)

    return newKeywordGroupList    

def getKeywordContraintString(group):
    listOfGroups = splitStrOfGroups(group)
    intermediateListOfGroups = []
    for g in listOfGroups:
        gStr = ' AND '.join(g)
        intermediateListOfGroups.append(gStr)

    listOfGroupsStr = '; '.join(intermediateListOfGroups)

    return listOfGroupsStr    

def getTwitterLink(tweetId,userHandle):
    twitterLink = "https://twitter.com/"+userHandle+"/status/"+str(tweetId)

    return twitterLink    

def createKeywordList(keywords, splitChar):
    if isinstance(keywords, str):
        keywordList = keywords.split(splitChar)
    else:
        keywordList=keywords 

    return keywordList       