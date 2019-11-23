
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier


def get_track_features(list_of_tracks):
    """Returns a list of only track features grouped by track"""
    features = []
    for track in list_of_tracks:
        features.append(track.get_all_features())
    return features

def one_class_SVM(train_data, test_data):
    """Runs a one class svm on train_data and predicts test_data.
    train_data is only positive class data and is a list of audio features.
    test_data is a list of audio features.
    returns an ordered list in same order as test_data with 1 meaning positive class and -1 meaning negative class."""
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    clf.fit(train_data)
    predicted_data_binary = clf.predict(test_data)
    return predicted_data_binary

def one_class_SVM_train(train_data):
    """Creates a one class SVM based on the train_data provided. Returns trained classifier.
    train_data is a list of Tracks with audio features."""
    track_features = get_track_features(train_data)
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    clf.fit(track_features)
    return clf

def adaboost_train(train_positive, train_negative):
    """Creates a Adaboost classifier based on the train_data provided. Returns trained classifier. Returns trained classifier
    train_data is a list of tracks with audio features."""
    train_data = train_positive + train_negative
    train_target = [1]*len(train_positive) + [-1]*len(train_negative)
    track_features = get_track_features(train_data)
    clf = AdaBoostClassifier()
    clf.fit(track_features, train_target)
    return clf

def classify_tracks(clf, test_data):
    """Uses trained classifier on test_data.
    test_data is a list of tracks with audio features.
    returns a list of likes and dislikes."""
    track_features = get_track_features(test_data)
    predicted_data_binary = clf.predict(track_features)
    likes = []
    dislikes = []
    for t_or_f, track in zip(predicted_data_binary, test_data):
        if t_or_f == 1:
            likes.append(track)
        else:
            dislikes.append(track)
    return likes, dislikes



