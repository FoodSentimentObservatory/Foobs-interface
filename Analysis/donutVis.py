import processingData.resultsFiltering as resultsFiltering
from operator import itemgetter

class Cluster:

	def __init__(self, tweetDictionary):
		
		self.tweetDictionary = tweetDictionary
		#self.newKeywordGroup = newKeywordGroup
		self.filteredTweets = []
		self.filteredTweetsList = []
		self.tweetsString = ""

	def clusterKeywords(self,newKeywordGroup, keyword):
		listOfDicts = []
		for key, value in self.tweetDictionary.items():
			if key == keyword:
				filteredGroupOfTweets = []

				for word in newKeywordGroup:
					#print(word)
					count = 0
					tweetsWithWordList = []
					for tweet in value:
						alreadySeenWords=[]
						checkIfExists = resultsFiltering.findWordInText(word, alreadySeenWords, tweet[0])		
						if checkIfExists==1:
							count += checkIfExists
							tweetTup = tweet[0]+"|"+tweet[2]+"|"+ word+"|"+key+"|"+tweet[1]+"|"+tweet[3]+"|"+tweet[4]+"|"+tweet[7]
							tweetsTupList=(tweet[0],tweet[2],word,key,tweet[1],tweet[3],tweet[4],tweet[7])
							self.filteredTweetsList.append(tweetsTupList)
							self.filteredTweets.append(tweetTup)
					if count>0:		
						wordTup = word+"|"+key+"|"+str(count)		
						filteredGroupOfTweets.append(wordTup)
				index = 1	
				strFilteredGroupOftweets = ','.join(filteredGroupOfTweets)
			
				listOfDicts.append(strFilteredGroupOftweets)	
		self.tweetsString = self.joinTweets()
		strListOfDicts = ';'.join(listOfDicts)	
		return strListOfDicts	

	def joinTweets(self):
		
		tweetsString = ';'.join(self.filteredTweets)

		return tweetsString	

	def getCounts(self,keywordsForSegmentsList):	
		listOfCounts=[]	
		for key, value in self.tweetDictionary.items():
			countOftweets=0
			for word in keywordsForSegmentsList:
				for v in value:
					alreadySeenWords=[]
					count = resultsFiltering.findWordInText(word, alreadySeenWords, v[0])
					countOftweets += count
			if countOftweets>0:		
				countTup = (key, countOftweets)
			
			listOfCounts.append(countTup)

		orderedListOfCounts = sorted(listOfCounts, key=itemgetter(1), reverse=True)
		
		return	orderedListOfCounts

	def getKeywordsWithNoResults(self, keywordsToClusterEnriched, listOfCounts):
		keywordsWithNoResults = []
		for word in keywordsToClusterEnriched:
			count = 0
			for tup in listOfCounts:
				if word == tup[0]:
					count += 1
			if count == 0:
				keywordsWithNoResults.append(word)
		if len(keywordsWithNoResults)>0:		
			keywordsWithNoResults.sort()				

		return keywordsWithNoResults					