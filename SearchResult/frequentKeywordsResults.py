import collections
import processingData.resultsFiltering as resultsFiltering
import Analysis.frequencyCount as frequencyCount
import html

class FrequentKeywordsResult:
	def __init__(self, group, tweets, word,groupIdStr,groupOriginalName):
		self.groupOfFrequentWords = group
		self.tweets = tweets
		self.word = word
		self.originalStringGroupId = groupIdStr
		self.originalGroupName = groupOriginalName
		self.newGroups = []			

	def splitIntoGroupList(self):		
		#splitting the freqword str into a list
		groupOfFrequentWordsList=self.groupOfFrequentWords.split("), (")
		cleanGroupList=[]
		for groups in groupOfFrequentWordsList:
			charList=['\'','[',']','(',')']
			check=0
			groups=resultsFiltering.extraCharRemoval(groups, charList,check)
			groupTup = groups.split(", ")		
			cleanGroupList.append(groupTup[1])

		return cleanGroupList	

	def findTweetsForFrequentWords(self):
		cleanGroupList = self.splitIntoGroupList()		
		#searching if a frequent word is in a tweet			
		for freqWord in cleanGroupList:
				for key, value in self.tweets.items():
					for tweet in value:
						alreadySeenWords=[]
						count = resultsFiltering.findWordInText(freqWord, alreadySeenWords, tweet[0])
						if count>0:
							resultsFiltering.addTweetToNewGroupsList(freqWord,tweet,self.originalStringGroupId,self.newGroups)
#main function to split the tweets in groups by frequent keyword
	def returnDictionaryOfTweets(self):		
		self.findTweetsForFrequentWords()		
		#making a dictionary by frequent word				
		index=5
		freqWordTweetsDict = resultsFiltering.dictionaryGen(self.newGroups,index)
		self.orderedFreqKeywordTweetDict = collections.OrderedDict(sorted(freqWordTweetsDict.items()))	
		return self.orderedFreqKeywordTweetDict	
#returns a list of data to be used by the upper part of the frequent results page
	def returnFrequentWordsGroupList(self):
		groupList = []
		i=0
		for key, value in self.orderedFreqKeywordTweetDict.items():
			numberOfTweets=len(value)
			groupId=self.originalStringGroupId+key
			groupString=self.originalGroupName+","+key
			keywordGroupList = groupString.split(',')
			frequentWords = frequencyCount.frequencyCount(value,keywordGroupList)
			numberOfTweets=len(value)

			groupTup = (key, groupString,i,numberOfTweets,frequentWords, numberOfTweets)
			groupList.append(groupTup)
			i+=1				
			
		return groupList