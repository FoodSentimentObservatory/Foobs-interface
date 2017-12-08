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
		#self.groupList =[]

	def splitIntoTweetList(self):	
		#the tweets list and the tuples of frequent keywords are returned as strs instead of lists..
		#..however, they do look like lists, so we need to strip them from the list chars and split them
		tweetsList=self.tweets.split("], [")
		tweetDataList=[]
		self.tweetDataListNoHtmlTags=[]
		for tweet in tweetsList:
			charList=['[[',']]','\n']
			check=1
			cleanTweet=resultsFiltering.extraCharRemoval(tweet, charList,check)
			tweetData = cleanTweet.split("', '")
			text=html.escape(tweetData[0],quote=True)
			displayName = html.escape(tweetData[4],quote=True)
			newText = resultsFiltering.clickableLinks(text)
			#making two lists, one that will be used for content and one for the hidden input field
			#difference is that the one for the hidden field doesn't contain html tags
			dataWithNoHtmlTags = [text,tweetData[1],tweetData[2],tweetData[3],displayName]
			filteredTweetData=[newText,tweetData[1],tweetData[2],tweetData[3],tweetData[4]]
			tweetDataList.append(filteredTweetData)
			self.tweetDataListNoHtmlTags.append(dataWithNoHtmlTags)

		return tweetDataList	

	def findTweetsContainingSelectedWord(self):
		self.tweetDataList = self.splitIntoTweetList()
		for tweet in self.tweetDataList:
			if self.word in tweet[0].lower():
				resultsFiltering.addTweetToNewGroupsList(self.word,tweet,self.originalStringGroupId,self.newGroups)				

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

	def findTweetsForTheOtherFrequentWords(self):
		cleanGroupList = self.splitIntoGroupList()		
		#searching if a frequent word is in a tweet			
		for freqWord in cleanGroupList:
			if freqWord!=self.word:
				for tweet in self.tweetDataList:
					if freqWord in tweet[0].lower():
						resultsFiltering.addTweetToNewGroupsList(freqWord,tweet,self.originalStringGroupId,self.newGroups)

	def returnDictionaryOfTweets(self):		
		self.findTweetsContainingSelectedWord()
		self.findTweetsForTheOtherFrequentWords()		
		#making a dictionary by frequent word				
		index=5
		freqWordTweetsDict = resultsFiltering.dictionaryGen(self.newGroups,index)
		self.orderedFreqKeywordTweetDict = collections.OrderedDict(sorted(freqWordTweetsDict.items()))

		return self.orderedFreqKeywordTweetDict	

	def returnFrequentWordsGroupList(self):
		groupList = []
		i=0
		for key, value in self.orderedFreqKeywordTweetDict.items():
			numberOfTweets=len(value)
			groupId=self.originalStringGroupId+key
			groupString=self.originalGroupName+","+key
			frequentWords = frequencyCount.frequencyCount(value,groupString)
			listForInputValues=[]
			for tweet in self.tweetDataListNoHtmlTags:
				if key in tweet[0].lower():
					listForInputValues.append(tweet)
			groupTup = (key, groupString,i,numberOfTweets,frequentWords, listForInputValues)
			groupList.append(groupTup)
			i+=1				

		return groupList