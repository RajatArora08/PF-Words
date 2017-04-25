from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pysolr
import CONSTANTS
import numpy as np
import pandas as pd
from itertools import combinations

solr = pysolr.Solr(CONSTANTS.SOLR_URL_CORE, timeout=10)

results = solr.search("*:*", rows=100)

df_x = {}

for result in results:
    if result.__contains__('description'):
        df_x[result['id']]= result['description']

choosed_list = list(combinations(list(df_x.keys()), 2))

test_data_x = []
solr = pysolr.Solr(CONSTANTS.SOLR_URL_TEST, timeout=10)
results = solr.search("id:*_RNASE_PANCREATIC", rows=1000)

for result in results:
    if result.__contains__('description'):
        test_data_x.append(result['description'])


models = []

for pf_word in choosed_list:

    if any(x for x in pf_word
           if "RNASE_PANCREATIC" in x):

        print("************************")
        print("{0} and {1}".format(pf_word[0], pf_word[1]))
        print("************************")

        x_train, x_test, y_train, y_test = \
            train_test_split([df_x[pf_word[0]], df_x[pf_word[1]]],
                             [pf_word[0], pf_word[1]],
                             test_size=0.0)

        vec = TfidfVectorizer(min_df=1, stop_words='english')

        x_train_cv = vec.fit_transform(x_train)

        mnb = MultinomialNB()

        mnb.fit(x_train_cv, y_train)

        models.append(mnb)

        foo = np.array(test_data_x)
        test_data_x_cv = vec.transform(test_data_x)
        predicted = mnb.predict(test_data_x_cv)

        print(predicted)
        print("___________________________________________________________________________________")
