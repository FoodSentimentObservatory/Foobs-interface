import sys
import re
import json
import databaseConfigurations.config as config
import processingData.resultsFiltering as resultsFiltering
#function to generate a json format data of the tweets for scattertext
def generateJson(listOfDataForVis):
    
    dicList = []
    for row in listOfDataForVis:
            dic = {}
            dic['group']=row[0]
            dic['username']=row[1]
            dic['tweet']=row[2]
            dicList.append(dic)

    jsonFormat =  json.dumps(dicList,ensure_ascii=False).encode('utf8')

    return (jsonFormat)  

def writeJstFile(texts, origCount):
    print ("Begining to generate a jst format file")
    count = len(texts)
    wordCount = 0
    documentBodyList = []
    n=0
    i = 1
    #opening a file to store all texts together
    path = config.getJstDataFile()

    with open(path, "w", encoding = 'utf-8') as f:
        for text in texts:
            n +=1
            textId = text[0]
            addCount = 0
            for tup in origCount:
                if tup[0]==textId:
                    addCount = tup[2]
            textBody = text[2]
            documentBodyList.append(textBody)
            wordCount += addCount

            if wordCount >=500 or n == count:
                wordCount = 0
                
                f.write("<d_%s> %s\n" %(i,n))
                for line in documentBodyList:
                     if len(line) == 0:
                         lineS = " "
                     else:
                         lineS = ' '.join(line)
                     
                     f.write("%s\n" %lineS)
                documentBodyList.clear()
                i += 1
                n=0

    print("JST data file created.")   

def readJSTResultFiles():
	path = config.getJstFinalTwords()
	charList = ["b'","\\n'"]
	check = 9
	with open(path,"r") as f:
		lines = f.readlines()
		for line in lines:
			#cleanLine = resultsFiltering.extraCharRemoval(line, charList,check)
			print(line)
		#print (repr(f.read()))	           