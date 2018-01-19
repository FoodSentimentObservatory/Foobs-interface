import processingData.resultsFiltering as resultsFiltering
from spacy.attrs import ORTH
from spacy import en
import spacy
import processingData.spacyStopWords as spacyStopWords

nlp = spacy.load("en")
spacyStopWords.stopWordsList(nlp)

def frequencyCount(tweets, group):
    repeatedWords=[]
    uniqueWords=[]

    allWordsStr = filterTexts(tweets, nlp)
    doc = nlp(allWordsStr)
    counts = doc.count_by(ORTH)
    i = 0
    #checks how many times each word appears in the whole word list and puts it either in repeated words or in unique words
    for word_id, count in sorted(counts.items(), reverse=True, key=lambda item: item[1]):
        words = nlp.vocab.strings[word_id]

        frequencyTuple = (str(count), words.lower())
        frequencyTupleStr = ' '.join(frequencyTuple)
        if count > 1:
                    repeatedWords.append(words.lower())
        else:
                    uniqueWords.append(words.lower())

    repeatedWordsList=[]
    #taking all the repeated words and checking how many tweets contain each
    for repeatedWord in repeatedWords:
        numberOfTweets = 0
        for tweet in tweets:
            alreadySeen=[]
            #checking if a word appears in the tweet text, if it appears more than once, the
            #count would still be 1, as we're only interested if it's in the tweet at all
            #and not how many times it 
            count = resultsFiltering.findWordInText(repeatedWord,alreadySeen, tweet[0])
            numberOfTweets+=count
        #checking again if the count is greater than 1, as it is possible that there might have been
        #a tweet which contained a word twice, so it made it to the repeatedWords, however, the word
        #appeared only in that tweet    
        if numberOfTweets > 1:
            repeatedWordsTuple = (str(numberOfTweets), repeatedWord)
            repeatedWordsList.append(repeatedWordsTuple)
    print("Generated frequencies for current group") 
    topTen=ignoreUniqueWords(repeatedWordsList, group)

    return topTen 

def filterTexts(textList, nlp):
    allWords = []
    for tweet in textList:
        text = tweet[0].lower()
        sentence = nlp(text)
        resultsFiltering.textCleanup(allWords, sentence)
    allWordsStr = ' '.join(allWords)

    return allWordsStr

def ignoreUniqueWords(repeatedWords, group):
    n=0
    topTen=[]
    #removing the group keywords from that list because we clearly know they are frequent and select the top 15 remaining
    for tup in repeatedWords:
        i=0
        for word in group:
            if tup[1]not in word:
                i+=1 
        if n<15 and i==len(group) and tup not in topTen:
                topTen.append(tup)
                i=0
                n+=1                                      
    return topTen         