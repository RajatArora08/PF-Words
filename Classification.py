import string

from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_selection import SelectKBest, chi2

import PF_To_Be_Tested
from CONSTANTS import SOLR_URL_CORE, CLASSIFIER_DIR_NB, CLASSIFIER_FILE_SVM, \
    SOLR_URL_TEST, CLASSIFIER_FILE_NB, CLASSIFIER_DIR_SVM
import pysolr
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import svm
import pickle
import os
from sklearn.pipeline import Pipeline
import csv

def predict(pf_word, cutoff=None):
    print(pf_word)
    if pf_word == 'ADH_SHORT':
        print('pause')

    CLASSIFIER_CUT_OFF = 9

    search_query = "id:*_{0}".format(pf_word)
    solr = pysolr.Solr(SOLR_URL_TEST, timeout=10)
    results = solr.search(search_query, rows=10000)

    test_data = list()
    test_data_ids = list()
    for doc in results:
        content = doc.get('title') + " " + doc.get('description') if doc.get('description') else doc.get('title')
        test_data.append(content)
        test_data_ids.append(doc.get('id'))


    classifier_dir = CLASSIFIER_DIR_SVM.format(pf_word)


    # Mnb: Multinomial Naive Bayes
    models_list = list()
    for filename in os.listdir(classifier_dir):

        with open(os.path.join(classifier_dir, filename), "rb") as file:
            models_list.append(pickle.load(file))

    dict_final = dict()
    for model in models_list:
        index_pf_word = list(model.classes_).index(pf_word)

        predicted = model.predict(test_data)
        probabilities = model.predict_proba(test_data)

        for probab, predict, doc_id in zip(probabilities, predicted, test_data_ids):
            dict_final.setdefault(doc_id, [0, 0, 0, 0])

            if predict == pf_word:

                dict_final[doc_id][0] += 1

                if probab.item(index_pf_word) >= 0.7 :
                    dict_final[doc_id][1] += 1

                if probab.item(index_pf_word) >= 0.8 :
                    dict_final[doc_id][2] += 1

                if probab.item(index_pf_word) >= 0.9 :
                    dict_final[doc_id][3] += 1


    file = open("resources/Intermediate_docs.csv", "a")
    writer = csv.writer(file)

    final_list = list()
    for doc_id, model_count in dict_final.items():

        temp = [False, False, False, False]

        if model_count[0] == 17:
            temp[0] = True

        if model_count[1] >= CLASSIFIER_CUT_OFF:
            temp[1] = True
        if model_count[2] >= CLASSIFIER_CUT_OFF:
            temp[2] = True
        if model_count[3] >= CLASSIFIER_CUT_OFF:
            temp[3] = True

        final_list.append(temp)

    doc_count_orig = 0
    doc_count_7 = 0
    doc_count_8 = 0
    doc_count_9 = 0

    for tmp in final_list:
        if tmp[0]:
            doc_count_orig += 1
        if tmp[1]:
            doc_count_7 += 1
        if tmp[2]:
            doc_count_8 += 1
        if tmp[3]:
            doc_count_9 += 1


    writer.writerow([pf_word, len(test_data_ids), doc_count_orig, doc_count_7, doc_count_8, doc_count_9])


class TokenizerStemmer:

    def tokenize(text):
        stemmer = PorterStemmer()
        return [stemmer.stem(w) for w in word_tokenize(text)]


def train_classifier(pf_word_list, input_pf_word=None):

    if input_pf_word:
        core_docs_query = "id:*_{0}".format(input_pf_word)
    else:
        core_docs_query = "*:*"

    solr = pysolr.Solr(SOLR_URL_CORE, timeout=10)
    results = solr.search(core_docs_query, rows=10000)

    core_docs_dict = dict()
    for doc in results:
        pf_word = doc.get('id').split('_', 1)[1]

        content = doc.get('title') + " " + doc.get('description') if doc.get('description') else doc.get('title')
        core_docs_dict.setdefault(pf_word, []).append(content)

    # Obtaining combinations of 2 for Classifier
    choosed_list = list(combinations(list(core_docs_dict.keys()), 2))

    # SVM
    pipeline_svm = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=TokenizerStemmer.tokenize,
                                       min_df=1,
                                       stop_words=stopwords.words('english') + list(string.punctuation)
                                       )),
        # ('selector', SelectKBest(score_func=chi2, k=200)),
        ('classifier', svm.SVC(kernel="linear", probability=True))])


    # NB
    pipeline_nb = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=TokenizerStemmer.tokenize,
                                       min_df=1,
                                       stop_words=stopwords.words('english') + list(string.punctuation)
                                       )),
        # ('selector', SelectKBest(score_func=chi2, k=200)),
        ('classifier', MultinomialNB())])

    # Without CHi2
    # pipeline = Pipeline([
    #     ('vectorizer', TfidfVectorizer(min_df=1, stop_words='english')),
    #     ('classifier', MultinomialNB())])

    for pf_word in choosed_list:


            print("************************")
            print("{0}: {2} and {1}: {3}".format(pf_word[0], pf_word[1],
                                                 len(core_docs_dict[pf_word[0]]),
                                                 len(core_docs_dict[pf_word[1]])))
            print("************************")

            # Do this while retrieval of data
            x_train_data = []
            y_train_data = []

            for tmp in core_docs_dict[pf_word[0]]:
                x_train_data.append(tmp)
                y_train_data.append(pf_word[0])

            for tmp in core_docs_dict[pf_word[1]]:
                x_train_data.append(tmp)
                y_train_data.append(pf_word[1])


            # x_train, x_test, y_train, y_test = train_test_split(x_train_data, y_train_data, test_size=0.0)

            model_svm = pipeline_svm.fit(x_train_data, y_train_data)
            model_nb = pipeline_nb.fit(x_train_data, y_train_data)


            # Saving Vectors and MNBs (SVM)
            filename_svm = CLASSIFIER_FILE_SVM.format(pf_word[0], pf_word[1])
            os.makedirs(os.path.dirname(filename_svm), exist_ok=True)

            # Save Classifiers for both pf-words.
            with open(filename_svm, "wb") as file:
                pickle.dump(model_svm, file)

            filename_svm = CLASSIFIER_FILE_SVM.format(pf_word[1], pf_word[0])
            os.makedirs(os.path.dirname(filename_svm), exist_ok=True)

            with open(filename_svm, "wb") as file:
                pickle.dump(model_svm, file)

            # Saving Vectors and MNBs (NB)
            filename_nb = CLASSIFIER_FILE_NB.format(pf_word[0], pf_word[1])
            os.makedirs(os.path.dirname(filename_nb), exist_ok=True)

            # Save Classifiers for both pf-words.
            with open(filename_nb, "wb") as file:
                pickle.dump(model_nb, file)

            filename_nb = CLASSIFIER_FILE_NB.format(pf_word[1], pf_word[0])
            os.makedirs(os.path.dirname(filename_nb), exist_ok=True)

            with open(filename_nb, "wb") as file:
                pickle.dump(model_nb, file)


if __name__ == '__main__':

    pf_words = PF_To_Be_Tested.PF_List
    train_classifier(pf_words)
    print("Training both classifiers for all PF words in PF_TEST.txt")

    predict(pf_words)
    print("Predicting all PF words with SVM, recording analysis in file and adding to intermediate docs")
