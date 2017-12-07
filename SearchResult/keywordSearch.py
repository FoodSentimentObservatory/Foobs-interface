import databaseConfigurations.sqlQueries as sqlQueries
import processingData.inputManagment as inputManagment
import processingData.textCleanUp as textCleanUp

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
		conn = sqlQueries.connectionToDatabaseTest(self.dbName)	

		return conn
#retrieves all collections from db and passes it to controller		
	def listOfCollections(self):	
		listOfCollections = sqlQueries.getExistingCollections(self.cursor)
		return listOfCollections
#splits the string input of keywords into a list of lists
	def listOfGroups(self):
		listOfGroups=[]	
		#checking if there's only one or multiple keyword groups
		if isinstance(self.group, str):
			listofwords = self.group.split(",")
			listOfGroups.append(listofwords)
		else:
			for g in self.group:
				singleGroup = g.split(",")
				listOfGroups.append(singleGroup)
		return listOfGroups		
#fetches tweets for all keyword groups, adds a clickable links version of the tweet text and returns
#a dictionary to the controller
	def retrieveTweets(self):			
		#getting all tweets with the specified keywords, the result is a list of lists, tweets are grouped in lists by keyword groups
		self.tweets=inputManagment.fetchingTweetsContainingGroups(self.cursor,self.location,self.searchQuery,self.listOfGroups, self.fromDate, self.toDate)
		self.conn.close()
		i=0
		tweetList=[]

		#for each group of tweets (all tweets fetched for one group of keywords)
		for groupOfTweets in self.tweets:
			for tweet in groupOfTweets:
				tweetL = list(tweet)
				#making links clickable
				text = textCleanUp.clickableLinks(tweetL[0])
				tweetL.append(text)
				#sending the tweets to a list
				tweetList.append(tweetL)

		index=5
		tweetDictionary = textCleanUp.dictionaryGen(tweetList,index)
		return tweetDictionary
#returns a list of keyword groups
	def getGroupList(self):
		i=0
		groupList = []
		for groupOfTweets in self.tweets:
			numberOfTweets = len(groupOfTweets)
			strGroupOfTweets = ','.join(self.listOfGroups[i])
			print(strGroupOfTweets)
			frequentWords = textCleanUp.frequencyCount(groupOfTweets,self.listOfGroups[i])
			
			noCommaGroupOfTweets = strGroupOfTweets.replace(',','')
			groupTup = (noCommaGroupOfTweets, strGroupOfTweets,i,numberOfTweets,frequentWords, groupOfTweets)
			groupList.append(groupTup)
			i+=1
		return groupList

