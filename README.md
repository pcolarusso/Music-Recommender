This project is for EE-551

This project is a music recommender to determine new music for you to enjoy based on songs you have liked.

# Summary
The project uses the Spotify API to get songs that have been liked as well as acoustic features about the songs. These features will be given to a classifier which will be able to determine if a song is similar to the music you have previously liked. After the classifier is trained, a playlist can be given to classifier and the it will pick out the songs that it predicts you would enjoy.

# Required Libraries
Spotipy  
`pip install spotipy`

Scikit-learn  
`pip install -U scikit-learn`

# Organization
* authtoken.py – used to provide credentials for accessing user information  
* classifier.py – contains functions for classifiers  
* getmusicfromSpotify.py – contains functions for communicating with Spotify  
* main.py – main program for using Music Recommender  
* testaccount.txt – information for signing into test account used  
* tests.py – test code  
* Track.py – class for creating tracks and holding track features  
* classifiertest folder  
   * classifiertest.py – program used to determine effectiveness of different classifiers  
   * results.txt – results of classifiertest.py

# Program Overview:
Program initially asks for credentials. First time users must grant access by copying redirect link into program after agreeing to permissions. The program will get user playlists and ask for a playlist of likes. Next, track features will be obtained for all tracks in like list. User will then be prompted if they have a playlist of dislikes. If yes, tracks and track features will be obtained and the Adaboost classifier will be used. If no, the one class SVM classifier will be used. The classifier will then run on a user chosen playlist to pick out songs that the user should like based on the training data.

# Machine Learning Classifiers.
### One Class SVM
Many users will not have a playlist of dislikes to add to the classifier, but most classifiers require a list of positive and negative data for training. One type of classifier that does not require both positive and negative data is the one class SVM classifier. This classifier will only need a user’s likes. The one class SVM will try to draw a frontier line around all positive samples and will classify new data as positive if it falls inside the frontier line. The drawback to this method is that this classifier does not deal with outliers very well which will decrease the accuracy overall. Based on test data, this algorithm had an accuracy of 71%

![One Class SVM](https://i.imgur.com/bAiWpND.png "One Class SVM")

### Adaboost
For users that have both likes and dislikes, many classifiers were tested (test can be seen in classifiertest). From the tests, it was found the Adaboost algorithm. Adaboost, also known as adaptive boosting, is an algorithm based on decision trees and random forest classification. The way Adaboost works is that it will take a small, random subset of the train and build a small decision tree from it. This decision tree is a stump and is considered a weak learner because is not a good classifier on its own. This stump is run on all data and the importance of samples that was incorrectly classified is increased so that it is mistakes are corrected in the next stump. Then another subset of the data is used to create another stump but this stump uses the sample weights determined by the previous stump. This will be done until many stumps are created. Finally, the stumps are run through the data again and stumps that perform better are given a higher weight for classifying. When the classifier is used on new data, each stump will predict a class and then the prediction and the weight of each stump is considered to create a prediction for the entire algorithm. Based on test data, this algorithm had an accuracy of 83%.

![Adaboost](https://i.imgur.com/Kw304aY.png "Adaboost")

