import string

from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_selection import SelectKBest, chi2

import PF_To_Be_Tested
from CONSTANTS import SOLR_URL_CORE, CLASSIFIER_DIR, CLASSIFIER_FILE, SOLR_URL_TEST
import pysolr
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle
import os
from sklearn.pipeline import Pipeline
import csv

def predict(pf_word, cutoff=None):
    print(pf_word)
    if pf_word == 'ADH_SHORT':
        print('pause')

    CLASSIFIER_CUT_OFF = 7
    # search_query = "id:308_EF_HAND_1".format(pf_word)

    search_query = "id:*_{0}".format(pf_word)
    solr = pysolr.Solr(SOLR_URL_TEST, timeout=10)
    results = solr.search(search_query, rows=10000)

    test_data = list()
    test_data_ids = list()
    for doc in results:
        content = doc.get('title') + " " + doc.get('description') if doc.get('description') else doc.get('title')
        test_data.append(content)
        test_data_ids.append(doc.get('id'))


    # vec = TfidfVectorizer(min_df=1, stop_words='english')
    # test_np_array = np.array(test_data)
    # test_vec = vec.fit_transform(test_np_array)

    classifier_dir = CLASSIFIER_DIR.format(pf_word)


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

            # if doc_id == '308_EF_HAND_1':
            #     print("Pause")
            #     print(probab)
            #
            # if predict != pf_word:
            #     print("Pause")

            if predict == pf_word:

                dict_final[doc_id][0] += 1

                if probab.item(index_pf_word) >= 0.7 :
                    dict_final[doc_id][1] += 1

                if probab.item(index_pf_word) >= 0.8 :
                    dict_final[doc_id][2] += 1

                if probab.item(index_pf_word) >= 0.9 :
                    dict_final[doc_id][3] += 1


        # temp_orig = set()
        # temp_orig.update([doc_id for word, doc_id in zip(predicted, test_data_ids)
        #                   if word == pf_word])


        # intermediate_docs = (temp & intermediate_docs)
        # actual_data_size = len(test_data)
        # predicted_data_size = predicted.size
        # unique, counts = np.unique(predicted, return_counts=True)
        # dict_predictions = dict(zip(unique, counts))
        # correct_predictions = dict_predictions.get(pf_word)
        # accuray = (correct_predictions / predicted_data_size) * 100
        # print("Actual data size: {0}".format(actual_data_size))
        # print("Total predicted data: {0}".format(predicted_data_size))
        # print("Correct prediction: {0}".format(correct_predictions))
        # print("Accuracy: {0}%".format(accuray))
        # print("___________________________________________________________________________________")

    # print(dict_final)

    file = open("/home/rajatar08/PF-Project/Intermediate_docs.csv", "a")
    writer = csv.writer(file)
    # writer.writerow(['Doc Id', 'No cut off', 'Cutoff @ 0.7', 'Cutoff @ 0.8', 'Cutoff @ 0.9'])

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

    # intermediate_docs_7 = set()
    # intermediate_docs_8 = set()
    # intermediate_docs_9 = set()
    #
    # print("***Length of intermediate docs 7= " + str(len(intermediate_docs_7)) + "***")
    # print("***Length of intermediate docs 8= " + str(len(intermediate_docs_8)) + "***")
    # print("***Length of intermediate docs 9= " + str(len(intermediate_docs_9)) + "***")


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

    pipeline = Pipeline([
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

        # if any(x for x in pf_word
        #        if "EF_HAND_1" in x):

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

            # vec = TfidfVectorizer(min_df=1, stop_words='english')
            model = pipeline.fit(x_train_data, y_train_data)
            # mnb = MultinomialNB()
            # mnb.fit(x_train_vectorised, y_train)

            # Testing
            print(len(model.named_steps['vectorizer'].get_feature_names()))
            # print(len(model.named_steps['selector'].scores_))
            # scores = sorted(model.named_steps['selector'].scores_.tolist(), reverse=True)

            # Saving Vectors and MNBs
            filename = CLASSIFIER_FILE.format(pf_word[0], pf_word[1])
            os.makedirs(os.path.dirname(filename), exist_ok=True)


            # Save Classifiers for both pf-words.
            with open(filename, "wb") as file:
                pickle.dump(model, file)

            filename = CLASSIFIER_FILE.format(pf_word[1], pf_word[0])
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, "wb") as file:
                pickle.dump(model, file)


if __name__ == '__main__':

    pf_words = PF_To_Be_Tested.PF_List
    # train_classifier(pf_words)

    for word in pf_words:
        predict(word)

    # predict('EF_HAND_1')
    # predict('ASP_PROTEASE')

    # for pf_word in PF_To_Be_Tested.PF_List:
    #     classify_pf_word(pf_word, train=True)
