import sys
import re
import json
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