import PF_To_Be_Tested
from CONSTANTS import SOLR_URL_CORE, CLASSIFIER_DIR, CLASSIFIER_FILE, VECTOR_FILE
import pysolr
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle
import os
import glob
import numpy as np


def predict(pf_word):

    search_query = "id:*_{0}".format(pf_word)
    solr = pysolr.Solr(SOLR_URL_CORE, timeout=10)
    results = solr.search(search_query, rows=10000)

    test_data = list()
    for doc in results:
        content = doc.get('title') + " " + doc.get('description') if doc.get('description') else doc.get('title')
        test_data.append(content)

    # vec = TfidfVectorizer(min_df=1, stop_words='english')
    # test_np_array = np.array(test_data)
    # test_vec = vec.fit_transform(test_np_array)

    classifier_dir = CLASSIFIER_DIR.format(pf_word)


    # Mnb: Multinomial Naive Bayes
    mnb_list = list()
    for filename in os.listdir(classifier_dir):

        with open(os.path.join(classifier_dir, filename), "rb") as file:
            mnb_list.append(pickle.load(file))

    for mnb in mnb_list:
        predicted = mnb.predict(test_data)

        actual_data_size = len(test_data)
        predicted_data_size = predicted.size
        unique, counts = np.unique(predicted, return_counts=True)
        dict_predictions = dict(zip(unique, counts))
        correct_predictions = dict_predictions.get(pf_word)
        accuray = (correct_predictions / predicted_data_size) * 100
        print("Actual data size: {0}".format(actual_data_size))
        print("Total predicted data: {0}".format(predicted_data_size))
        print("Correct prediction: {0}".format(correct_predictions))
        print("Accuracy: {0}%".format(accuray))
        print("___________________________________________________________________________________")




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

    for pf_word in choosed_list:

        if any(x for x in pf_word
               if "EF_HAND_1" in x):

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


            x_train, x_test, y_train, y_test = train_test_split(x_train_data, y_train_data, test_size=0.0)

            vec = TfidfVectorizer(min_df=1, stop_words='english')
            x_train_vectorised = vec.fit_transform(x_train)
            mnb = MultinomialNB()
            mnb.fit(x_train_vectorised, y_train)

            # Saving Vectors and MNBs
            filename = CLASSIFIER_FILE.format(pf_word[0], pf_word[1])
            os.makedirs(os.path.dirname(filename), exist_ok=True)


            # Save Classifiers for both pf-words.
            with open(filename, "wb") as file:
                pickle.dump(mnb, file)

            filename = CLASSIFIER_FILE.format(pf_word[1], pf_word[0])
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, "wb") as file:
                pickle.dump(mnb, file)


if __name__ == '__main__':

    pf_words = PF_To_Be_Tested.PF_List
    # train_classifier(pf_words)

    predict('EF_HAND_1')

    # for pf_word in PF_To_Be_Tested.PF_List:
    #     classify_pf_word(pf_word, train=True)
