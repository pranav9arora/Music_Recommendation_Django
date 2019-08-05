# You need to install scikit-learn:
# sudo pip install scikit-learn
#
# Dataset: Polarity dataset v2.0
# http://www.cs.cornell.edu/people/pabo/movie-review-data/
#
# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn


import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

import csv
from operator import itemgetter

train_data = []
train_labels = []
train_labels_name = []


def getRecommendation():


    with open('source/content/media/train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(row[0])
                line_count += 1
                try:
                    train_data.append([float(row[3]),
                                       float(row[4]),
                                       float(row[5]),
                                       float(row[6]),
                                       float(row[7]),
                                       float(row[8]),
                                       float(row[9]),
                                       float(row[10]),
                                       float(row[11])]
                                      )

                    train_labels.append(row[1])
                    train_labels_name.append(row[0])
                except Exception as e:
                    print(e)
        test_data = []
        test_label = []
        test_label_name = []

        with open('source/content/media/test.csv') as csv_file:
            csv_reader_test_data = csv.reader(csv_file, delimiter=',')
            line_count1 = 0
            for row in csv_reader_test_data:
                if line_count1 == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count1 += 1
                else:
                    # print(row[0])
                    line_count1 += 1
                    try:
                        test_data.append([float(row[3]),
                                          float(row[4]),
                                          float(row[5]),
                                          float(row[6]),
                                          float(row[7]),
                                          float(row[8]),
                                          float(row[9]),
                                          float(row[10]),
                                          float(row[11])]
                                         )

                        test_label.append(row[1])
                        test_label_name.append(row[0])
                    except Exception as e:
                        print(e)
        # print(train_data)
        clf = svm.SVC()
        # print(train_labels)

        clf.fit(train_data, train_labels)
        svc_predection = clf.predict(train_data)

        # print(svc_predection)
        classifier_linear = svm.SVC(kernel='rbf', probability=True, random_state=True)
        classifier_linear.fit(train_data, train_labels)

        probability = classifier_linear.predict_proba(test_data)
        predict = classifier_linear.predict(test_data)
        print(probability)
        print(classifier_linear.predict(test_data))
        # gets a dictionary of {'class_name': probability}
        # prob_per_class_dictionary = dict(zip(classifier_linear.classes_, classifier_linear.predict(test_data)))
        # print(prob_per_class_dictionary)
        decesion = classifier_linear.decision_function(test_data)
        # print(decesion.tolist())
        print(classifier_linear.classes_)
        key_list = 'name', 'value'
        recommended_artists_name = []
        recommended_artists_id = []
        recommended_artists_url = []

        for dec in decesion:
            # print(dec.tolist())
            data = dict(zip(classifier_linear.classes_, dec))
            print('------------------')
            print(data)
            count_artist_no = 0
            for key, value in sorted(data.items(), key=itemgetter(1), reverse=True):
                print(key, value)
                print(count_artist_no)
                name = train_labels_name[train_labels.index(key)]
                # try:
                #     b = recommended_artists_id.index(str(key))
                #
                #     print(b)
                # except Exception as e:
                #     print('artist not found so adding it')
                #     recommended_artists_id.append(key)
                #     recommended_artists_name.append(name)
                if count_artist_no == 1:
                    try:
                        b = recommended_artists_id.index(str(key))

                        print(b)
                    except Exception as e:
                        print('artist not found so adding it')
                        recommended_artists_id.append(key)
                        recommended_artists_name.append(name)
                count_artist_no += 1
            print('*************')
            # print(sorted(data.iterkeys()))
        print('-------------------recommended artists--------------------')
        count_artist = 0
        finallist = []
        for artists in recommended_artists_name:
            print(artists)
            print(recommended_artists_id[count_artist])
            recommend_dict = {}
            recommend_dict['id']=recommended_artists_id[count_artist]
            recommend_dict['name']=artists
            finallist.append(recommend_dict)
            count_artist += 1

        # data = [dict(zip(key_list, (a, b))) for a, b in zip(name_list, id_list)]
        # data = [dict(zip(key_list, (a, b))) for a, b in zip(classifier_linear.classes_, decesion)]
        # print(data)

        # gets a list of ['most_probable_class', 'second_most_probable_class', ..., 'least_class']
        # results_ordered_by_probability = map(lambda x: x[0],sorted(zip(classifier_linear.classes_, classifier_linear.predict(test_data)), key=lambda x: x[1], reverse=True))
        # results_ordered_by_probability = map(lambda x: x[0],sorted(zip(classifier_linear.classes_, classifier_linear.predict(test_data)), key=lambda x: x[1], reverse=True))
        # for res in results_ordered_by_probability:
        #     print(res)

        # prob_per_class_dictionary = zip(classifier_linear.classes_, classifier_linear.predict(test_data)[0])
        # print(prob_per_class_dictionary)
        # print('------')
        # # decesion=classifier_linear.decision_function(train_data)
        # # print(decesion)
        # linear=classifier_linear.predict(train_data)
        # print(linear)
        count = 0
        correct = 0
        incorrect = 0
        for values in predict:
            if values == test_label[count]:
                correct += 1
            else:
                incorrect += 1
            count += 1

        print(str(correct) + ":" + str(incorrect))
        print('correctness:' + str(float(correct / (correct + incorrect) * 100.0)))
        return {'finallist':finallist}
try:
    getRecommendation()
except Exception as e:
    print(e)
