
import numpy as np
from sklearn import svm
import sklearn

def count_positives(data):
    """counts how many positive classes are in data_set"""
    count = 0
    for num in data:
        if num == 1:
            count += 1
    return count


# train, test = sklearn.model_selection.train_test_split(data)
def one_class_SVM(train_data, test_data):
    """Runs a one class svm on train_data and predicts test_data.
    train_data is only positive class data and is a list of audio features
    test_data is a list of audio features
    returns an ordered list in same order as test_data with 1 meaning positive class and -1 meaning negative class"""
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    clf.fit(train_data)
    predicted_data_binary = clf.predict(test_data)
    return predicted_data_binary


