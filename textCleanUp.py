import spacy
import re
from spacy.attrs import ORTH
from spacy import en
import sys
import os
from operator import itemgetter
import fileFunctions
import spacyStopWords
from itertools import groupby

nlp = spacy.load("en")
spacyStopWords.stopWordsList(nlp)
#function to remove stop words, urls, punctuation, numbers and symbols using spacy. Goes through each tweet text and appends the result to two lists, one for the tweet and one for general statistics
#removing also words like e.coli?
def textCleanup(allWords,text):
    for word in text:
                words =re.sub(r'@', "", str(word))
                if word.is_stop != True and word.like_url != True and word.is_punct !=True and word.like_num != True and words.isalpha()== True and len(words)> 1:
                    allWords.append(words.lower())
#does a frequency count of words across the whole corpus given to it using spacy and also generates a list of repeated words and unique words
def frequencyCount(tweets, group):
    allWords = []
    repeatedWords=[]
    uniqueWords=[]
    for tweet in tweets:
        text = tweet[0].lower()
        sentence = nlp(text)
        textCleanup(allWords, sentence)
    allWordsStr = ' '.join(allWords)
    doc = nlp(allWordsStr)
    counts = doc.count_by(ORTH)
    i = 0
    #checks how many times each word appears in the whole word list and puts it either in repeated words or in unique words
    for word_id, count in sorted(counts.items(), reverse=True, key=lambda item: item[1]):
        words = nlp.vocab.strings[word_id]

        frequencyTuple = (str(count), words.lower())
        frequencyTupleStr = ' '.join(frequencyTuple)
        if count > 1:
                    repeatedWordsTuple = (str(count), words.lower())
                    repeatedWords.append(repeatedWordsTuple)

        else:
                    uniqueWords.append(words.lower())
    print("Generated frequencies for current group") 

    n=0
    topTen=[]
    #removing the group keywords from that list because we clearly know they are frequent and select the top 10 remaining
    for tup in repeatedWords:
        if tup[1]not in group and n<15:
            topTen.append(tup)
            n+=1               
    return topTen                

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
            textStr = re.sub(r'rt','',textStrRt)
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
            item=item.replace(ch,"")
    if check==0:        
        itemS=item[1:]   
    elif check==1:
        itemS=item[1:-1] 
    else:
        itemS=item          

    return itemS

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