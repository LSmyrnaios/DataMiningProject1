# from sklearn.cross_validation import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.preprocessing import Normalizer

stop_words = set(ENGLISH_STOP_WORDS)


def addPreDefinedStopWords():
    stop_words.add('said')
    stop_words.add('he')
    stop_words.add('He')
    stop_words.add('it')
    stop_words.add('It')
    stop_words.add('got')
    stop_words.add("don't")
    stop_words.add('like')
    stop_words.add("didn't")
    stop_words.add('ago')
    stop_words.add('went')
    stop_words.add('did')
    stop_words.add('day')
    stop_words.add('just')
    stop_words.add('thing')
    stop_words.add('think')
    stop_words.add('say')
    stop_words.add('know')
    # TODO - Add more stopWords..


def split_dataset(dataset, train_percentage, feature_headers, target_header):
    """
    Split the dataset with train_percentage
    :param dataset:
    :param train_percentage:
    :param feature_headers:
    :param target_header:
    :return: train_x, test_x, train_y, test_y
    """

    # Split dataset into train and test dataset
    train_x, test_x, train_y, test_y = train_test_split(dataset[feature_headers], dataset[target_header],
                                                        train_size=train_percentage, test_size=0.3)
    return train_x, test_x, train_y, test_y


if __name__ == '__main__':
    headers = ['RowNum', 'Id', 'Title', 'Content', 'Category']

    train_data = pd.read_csv('train_set.csv', sep="\t")
    test_data = pd.read_csv('test_set.csv', sep="\t")

    print(headers[2:4])

    train_x, test_x, train_y, test_y = split_dataset(train_data, 0.7, headers[2:4], headers[-1])

    le = preprocessing.LabelEncoder()
    le.fit(train_data["Category"])
    y = le.transform(train_data["Category"])

    print 'y : ', set(y)

    # Train and Test dataset size details
    print "Train_x Shape :: ", train_x.shape
    print "Train_y Shape :: ", train_y.shape
    print "Test_x Shape :: ", test_x.shape
    print "Test_y Shape :: ", test_y.shape
    print "Train_x colums ::", train_x.columns

    for row in train_data:
        train_x['Content'] += 5 * train_x['Title']

    for row in test_data:
        test_x['Content'] += 5 * test_x['Title']

    addPreDefinedStopWords()

    # print train_x['Content'][1]

    count_vectorizer = CountVectorizer(stop_words)
    vectorTrain = count_vectorizer.fit_transform(train_x['Content'])
    vectorTest = count_vectorizer.fit_transform(test_x['Content'])
    clf = RandomForestClassifier(n_estimators=100)
    print "VectorTrain shape::", vectorTrain.shape
    print "VectorTest shape::", vectorTest.shape

    lsa = TruncatedSVD(n_components=100)

    vectorTrain = lsa.fit_transform(vectorTrain)
    vectorTest = lsa.fit_transform(vectorTest)

    print "VectorTrain shape::", vectorTrain.shape
    print "VectorTest shape::", vectorTest.shape

    clf.fit(vectorTrain, train_y)

    y_pred = clf.predict(vectorTest)

    print "Train Accuracy :: ", accuracy_score(train_y, clf.predict(vectorTrain))
    print "Test Accuracy  :: ", accuracy_score(test_y, y_pred)