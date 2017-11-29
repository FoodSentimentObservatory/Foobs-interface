from itertools import groupby
import fileFunctions
#function to count how many tweets have been posted each day
def dateGrouping(dateList, word):
    dic = {}
    countByDateList = [("date","count")]
    f = lambda x: x[1]
    for key, group in groupby(sorted(dateList, key=f), f):
        dic[key] = list(group)

    for key, value in dic.items():
        tweetCount = len(value)
        countByDateTup = (key, tweetCount)
        countByDateList.append(countByDateTup)

    fileNameString = word+"count_by_date"

    fileFunctions.writeCsvFile(countByDateList, fileNameString)
