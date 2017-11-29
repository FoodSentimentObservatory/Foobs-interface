import scattertext as st
import spacy
from pprint import pprint
from scattertext import SampleCorpora
from scattertext.CorpusFromPandas import CorpusFromPandas
from scattertext import produce_scattertext_explorer
import pandas as pd
import numpy as np
import json

def generateScatterText(data, listOfCollectionNames):
	collectionOne = listOfCollectionNames[0]
	collectionTwo = listOfCollectionNames[1]

	convention_df = pd.DataFrame(eval(data))
	nlp = spacy.en.English()

	pprint(convention_df.iloc[1])


	corpus = CorpusFromPandas(convention_df,
	                          category_col='group',
	                          text_col='tweet',
	                          nlp=nlp).build()

	html = produce_scattertext_explorer(corpus,
	                                    category=collectionOne,
	                                    category_name=collectionOne,
	                                    not_category_name=collectionTwo,
	                                    minimum_term_frequency=5,
	                                    width_in_pixels=1000,
	                                    metadata=convention_df['username'])


	open('./demo.html', 'wb').write(html.encode('utf-8'))
	print("html file generated")

	return html

	