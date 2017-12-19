import databaseConfigurations.sqlQueries as sqlQueries
import DataManager.dataManager as dataManager
import processingData.resultsFiltering as resultsFiltering
import DataManager.tweetsDataManager as tweetsDataManager
import Analysis.frequencyCount as frequencyCount

class SearchResult:		
	def __init__(self, group,fromDate,toDate, dbName, location, searchQuery):
		self.dbName=dbName	
		self.fromDate = fromDate
		self.toDate = toDate
		self.group = group
		self.listOfGroups = self.listOfGroups()
		self.location = location
		self.searchQuery = searchQuery

		self.conn = self.startDbConnection()
		self.cursor = self.conn.cursor()

	def startDbConnection(self):		
		conn = dataManager.startDbConnection(self.dbName)	

		return conn
#retrieves all collections from db and passes it to controller		
	def listOfCollections(self):	
		listOfCollections = sqlQueries.getExistingCollections(self.cursor)
		return listOfCollections
#splits the string input of keywords into a list of lists
	def listOfGroups(self):
		listOfGroups=resultsFiltering.splitStrOfGroups(self.group)	
		return listOfGroups		
#fetches tweets for all keyword groups, adds a clickable links version of the tweet text and returns
#a dictionary to the controller
	def retrieveTweets(self):			
		#getting all tweets with the specified keywords, the result is a list of lists, tweets are grouped in lists by keyword groups
		self.tweets=tweetsDataManager.fetchingTweetsContainingGroups(self.cursor,self.location,self.searchQuery,self.listOfGroups, self.fromDate, self.toDate)
		self.conn.close()
		i=0
		tweetList=[]

		#for each group of tweets (all tweets fetched for one group of keywords)
		for groupOfTweets in self.tweets:
			for tweet in groupOfTweets:
				tweetL = list(tweet)
				#making links clickable
				text = resultsFiltering.clickableLinks(tweetL[0])
				tweetL.append(text)
				#sending the tweets to a list
				tweetList.append(tweetL)

		index=5
		tweetDictionary = resultsFiltering.dictionaryGen(tweetList,index)

		return tweetDictionary
#returns a list of keyword groups
	def getGroupList(self):
		i=0
		groupList = []
		if self.listOfGroups[0] != 'all tweets':
			for groupOfTweets in self.tweets:
				numberOfTweets = len(groupOfTweets)
				strGroupOfTweets = ','.join(self.listOfGroups[i])
				frequentWords = frequencyCount.frequencyCount(groupOfTweets,self.listOfGroups[i])
				
				noCommaGroupOfTweets = strGroupOfTweets.replace(',','')
				groupTup = (noCommaGroupOfTweets, strGroupOfTweets,i,numberOfTweets,frequentWords, groupOfTweets)
				groupList.append(groupTup)
				i+=1
		else:
			numberOfTweets=len(self.tweets[0])	
			frequentWords = frequencyCount.frequencyCount(self.tweets[0],self.listOfGroups)	
			noCommaGroupOfTweets="alltweets"
			groupTup = (noCommaGroupOfTweets, self.listOfGroups[0],i,numberOfTweets,frequentWords, self.tweets[0])
			groupList.append(groupTup)

		return groupList

	def getQueryData(self):
		queryDataList = []
		if self.listOfGroups[0] != 'all tweets':
			for group in self.listOfGroups:
				keywordString = ','.join(group)
				noCommaKeywordGroup = ''.join(group)
				groupTup = (noCommaKeywordGroup,keywordString,self.searchQuery, self.location, self.fromDate, self.toDate)
				queryDataList.append(groupTup)
		else:
			noCommaKeywordGroup	="alltweets"
			groupTup = (noCommaKeywordGroup,self.listOfGroups[0],self.searchQuery, self.location, self.fromDate, self.toDate)
			queryDataList.append(groupTup)	

		return queryDataList		

	def filterTweets(self, keywordsToClusterEnriched):
		tweetsDictionary = self.retrieveTweets()
		newListOfTweets = []
		
		for key, value in tweetsDictionary.items():
			for tweet in value:
				for word in keywordsToClusterEnriched:
					alreadySeenWords=[]
					count = resultsFiltering.findWordInText(word, alreadySeenWords, tweet[0])
					if count>0:
						newTweetList = [tweet[0],tweet[1],tweet[2],tweet[3],tweet[4],tweet[5],tweet[6], word]
						newListOfTweets.append(newTweetList)

		index = 7
		newTweetsDictionary = resultsFiltering.dictionaryGen(newListOfTweets,index)

		return 	newTweetsDictionary				

