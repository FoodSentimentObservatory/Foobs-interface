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