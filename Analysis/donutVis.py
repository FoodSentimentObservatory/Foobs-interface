import processingData.resultsFiltering as resultsFiltering
from operator import itemgetter

class Cluster:

	def __init__(self, tweetDictionary):
		
		self.tweetDictionary = tweetDictionary
		#self.newKeywordGroup = newKeywordGroup
		self.filteredTweets = []
		self.filteredTweetsList = []
		self.tweetsString = ""
#function that creates the string lists that will be used to display the donut
	def clusterKeywords(self,newKeywordGroup, keyword):
		listOfDicts = []
		for key, value in self.tweetDictionary.items():
			#only matches to the key that is the same as the selected word
			if key == keyword:
				filteredGroupOfTweets = []
				for word in newKeywordGroup:
					count = 0
					tweetsWithWordList = []
					#checks if the keywords for segments are in a list or string format
					# currently, the keyword groups would be in list format so they need to be treated differently
					if isinstance(word, str):
						wordStr = word
					else:
						wordStr = ' AND '.join(word)	
					for tweet in value:
						alreadySeenWords=[]
						#if the word is a string, search just for one word, else search for a list of words
						if isinstance(word, str):
							checkIfExists = resultsFiltering.findWordInText(word, alreadySeenWords, tweet[0])
						else:
							wordCount = resultsFiltering.findKeywordsInText(tweet[0], word)	
							if wordCount==len(word):
								checkIfExists = 1
							else:
								checkIfExists=0	
						#if the word (or the full list of words) exists in the tweet text, do the following							
						if checkIfExists==1:
							count += checkIfExists
							tweetTup = tweet[0]+"|"+tweet[2]+"|"+ wordStr+"|"+key+"|"+tweet[1]+"|"+tweet[3]+"|"+tweet[4]+"|"+tweet[7]
							tweetsTupList=(tweet[0],tweet[2],wordStr,key,tweet[1],tweet[3],tweet[4],tweet[7], tweet[8])
							#this list will be used to display all tweets once the donut has been loaded
							self.filteredTweetsList.append(tweetsTupList)
							#this is a stringified version of the list, which will be passed to the javaScript
							#in order to filter the tweets onclick of a segment
							self.filteredTweets.append(tweetTup)
					if count>0:
						if "," in key:
							keyStr = key.replace(",", " AND ")	
						else:
							keyStr = key		
						wordTup = wordStr+"|"+keyStr+"|"+str(count)	
						filteredGroupOfTweets.append(wordTup)
				index = 1	
				strFilteredGroupOftweets = ','.join(filteredGroupOfTweets)
			
				listOfDicts.append(strFilteredGroupOftweets)	
		self.tweetsString = self.joinTweets()
		#this string will also be passed to the javaScript in order to
		#create the actual donut
		strListOfDicts = ';'.join(listOfDicts)	
		return strListOfDicts	

	def joinTweets(self):	
		tweetsString = ';'.join(self.filteredTweets)
		return tweetsString	
	#function to get a list with all cluster keywords that have returned some 
	# tweets containing segment keywords
	def getCounts(self,keywordsForSegmentsList):	
		listOfCounts=[]
		for key, value in self.tweetDictionary.items():
			countOftweets=0
			for word in keywordsForSegmentsList:
				for v in value:
					alreadySeenWords=[]
					if isinstance(word, str):
						count = resultsFiltering.findWordInText(word, alreadySeenWords, v[0])
						countOftweets += count
					else:
						count = resultsFiltering.findKeywordsInText(v[0], word)	
						if count==len(word):
							countOftweets += 1	
			#if there are any tweets with any of the segment keywords, add to the count list			
			if countOftweets>0:		
				countTup = (key, countOftweets, v[6])
				listOfCounts.append(countTup)
	
		#ordering the final count list by count of tweets
		orderedListOfCounts = sorted(listOfCounts, key=itemgetter(1), reverse=True)

		return	orderedListOfCounts
	#this function check which cluster keywords do not appear in listOfCounts
	#and adds them into a list of keywords with no result to be displayed separately from
	#the main table of results
	def getKeywordsWithNoResults(self, keywordsToClusterEnriched, listOfCounts):
		keywordsWithNoResults = []
		for word in keywordsToClusterEnriched:
			count = 0
			if isinstance(word,list):
				wordStr = ','.join(word)
			else:
				wordStr = word

			for tup in listOfCounts:				
				if wordStr == tup[2]:
					count += 1

			if count == 0:
				keywordsWithNoResults.append(wordStr)

		if len(keywordsWithNoResults)>0:		
			keywordsWithNoResults.sort()				

		return keywordsWithNoResults					