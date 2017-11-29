from spacy import en
import spacy

def stopWordsList(nlp):
    newStopWords = ['co', 'couldnt', 'describe', 'eg', 'find', 'found', 'hasnt', 'im', 'ie', 'ltd', 'mill', 'un', 'de', 'rt', 'pm', \
                    'hi', 'hello', 'hey', 'pre', 'retweet', 'http', 'htt', 'ht', 'mr', 'ms', 'mrs', 'maybe', 'app', 'ha', 'haha', 'till'\
                    'til', 'cv', 'ya', 'vs', 'st', 'dm', 'https','amp']
    for stopw in newStopWords:
        en.English.Defaults.stop_words.add(stopw)
    notStopWords = ['part', 'again', 'last', 'using', 'almost', 'together', 'cannot', 'well', 'rather', 'without', 'various',\
                    'same', 'empty', 'however', 'back', 'against', 'top', 'throughout', 'several', 'nevertheless', 'out', 'quite'\
                    'nobody', 'say', 'anything', 'alone', 'whole', 'full', 'first', 'always', 'across', 'least', 'third', 'please'\
                    'front', 'nothing', 'less', 'make', 'perhaps', 'behind', 'not', 'enough', 'really','used', 'side', 'move', \
                    'none', 'must', 'should', 'many', 'very', 'most', 'regarding', 'few', 'below', 'never', 'over', 'beyond', \
                    'show', 'bottom', 'before', 'indeed', 'already', 'down', 'beforehand', 'above','now', 'unless', 'further', 'nowhere',\
                    'serious']
    for word in en.English.Defaults.stop_words:
        lexeme = nlp.vocab[word]
        if word not in notStopWords:
            lexeme.is_stop = True
        else:
            lexeme.is_stop = False
