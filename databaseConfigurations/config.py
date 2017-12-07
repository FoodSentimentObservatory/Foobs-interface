from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.txt')

#collecting database specifications 
def databasePort():
    dbPort = parser.get('db-data', 'port')
    return dbPort

def dbServer():
    server = parser.get('db-data', 'server')
    return server

def getAllDatabases():
    databaseList = parser.items('db-names')
    return databaseList

def getJstDataFile():
	dataFilePath = parser.get('jst-data', 'dataFile')
	return dataFilePath

def getJstExecutable():
	jstExecutablePath = parser.get('jst-data', 'jstExe')
	return jstExecutablePath

def getJstTrainingProperties():
	jstTrainingPropertiesPath = parser.get('jst-data', 'trainingPropertiesFile')	
	return jstTrainingPropertiesPath	

def getJstFinalTwords():
	finalTwordsPath = parser.get('jst-data','jstFinalTwords')	    
	return finalTwordsPath