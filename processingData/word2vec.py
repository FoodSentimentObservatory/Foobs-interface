import urllib.parse
import urllib.request

def getSimilarForASingleWord(word,numOfEnrichments): 
 url = 'http://bionlp-www.utu.fi/wv_demo/nearest'
 values = {'form[0][name]' : 'word',
          'form[0][value]' : word,
          'form[1][name]' : 'topn',
          'form[1][value]' : numOfEnrichments,
          'model_name' : 'English GoogleNews Negative300' }

 data = urllib.parse.urlencode(values)
 data = data.encode('ascii') # data should be bytes
 req = urllib.request.Request(url, data)
 with urllib.request.urlopen(req) as response:
   the_page = response.read()
   the_page = the_page.decode('ascii')
   the_page = the_page.replace('{\"tbl\": "<div class=\\"w2vresultblock bg-info\\">','')
   the_page = the_page.replace('</br>\\n\\n',',')
   the_page = the_page.replace(',</div>\\n\\n\\n\\n"}','')
   the_page = the_page.replace('\\n\\n','')
   the_page = the_page.replace('_',' ')
   the_page = the_page.lower();
   list = the_page.split(',')
  
   return set(list)  

def getSimilarForListOfWords(words,numOfEnrichments):
  resultSet = set() 
  listOfWords=[]
  for word in words:
    listOfWords.append(word)
    wordSet = set(word) 
    resultSet = resultSet | getSimilarForASingleWord(word,numOfEnrichments) | wordSet

   
  for word in resultSet:
     if len(word)>2 and word not in listOfWords:
      listOfWords.append(word)
  
  return  (listOfWords)

