
import authtoken
import getmusicfromSpotify
import classifier

print("Welcome to the Spotify Music Recommender.")
print("If this is your first time logging in, you will be asked to agree to data permissions")

username = input("Enter your username: ")

try:
    user = authtoken.get_credentials(username)
except Exception as e:
    print(e)
    print("Error in Authentication, please try again")
    exit(1)

playlists = getmusicfromSpotify.get_user_playlists(user)
print("Accessible Playlists:")
for playlist in playlists:
    print(playlist)

while True:
    like_playlist = input("Enter name of playlist containing songs of likes for recommendations to be derived from: ")
    if like_playlist not in playlists:
        print("Playlist does not exist")
    else:
        break

print("Playlist found, getting tracks")
like_track_list = getmusicfromSpotify.get_track_names_ids(playlists[like_playlist][0], playlists[like_playlist][1], user, username)
print("Have all tracks, getting track features")
getmusicfromSpotify.create_track_features(like_track_list, user)
unfeatured_likes = getmusicfromSpotify.remove_unfeatured_tracks(like_track_list)
if unfeatured_likes != []:
    print("Could not find all tracks. Missing tracks: ", end='')
    for missing_track in unfeatured_likes:
        print(missing_track, end=' ')
        print()
else:
    print("Received track features")


print("Do you have a playlist of dislikes to use for recommendations? This will improve recommendation accuracy")
dislikes_exist = input("Enter y for yes or anything else for no: ")

if dislikes_exist == 'y':
    while True:
        dislike_playlist = input("Enter name of playlist containing songs of likes for recommendations to be derived from: ")
        if dislike_playlist not in playlists:
            print("Playlist does not exist")
        else:
            havedislikes = True
            dislike_track_list = getmusicfromSpotify.get_track_names_ids(playlists[dislike_playlist][0], playlists[dislike_playlist][1], user, username)
            print("Have all tracks, getting track features")
            getmusicfromSpotify.create_track_features(dislike_track_list, user)
            unfeatured_dislikes = getmusicfromSpotify.remove_unfeatured_tracks(dislike_track_list)
            if unfeatured_dislikes != []:
                print("Could not find all tracks. Missing tracks: ", end='')
                for missing_track in unfeatured_dislikes:
                    print(missing_track, end=' ')
                    print()
            else:
                print("Received track features")
            break
else:
    havedislikes = False

print("Running Machine Learning Algorithm")
if havedislikes:
    print("Training Adaboost Classifier")
    clf = classifier.adaboost_train(like_track_list, dislike_track_list)
else:
    print("Training One Class SVM Classifier")
    clf = classifier.one_class_SVM_train(like_track_list)
print("Finished Training Classifier")

while True:
    print("Choose playlist for Recommendations")
    print("User Playlists:")
    for playlist in playlists:
        print(playlist)
    print("Spotify curated playlists")
    sp_curated = getmusicfromSpotify.list_of_curated_playlist()
    for playlist in sp_curated:
        print(playlist)

    while True:
        chosen_playlist = input("Choose a playlist: ")
        if chosen_playlist in playlists:
            test_playlist = playlists[chosen_playlist]
            break
        elif chosen_playlist in sp_curated:
            test_playlist = getmusicfromSpotify.get_curated_playlist_id(chosen_playlist)
            break
        else:
            print("Playlist not found")
    print("Playlist found, getting tracks")
    test_track_list = getmusicfromSpotify.get_track_names_ids(test_playlist[0], test_playlist[1], user, username)
    print("Have all tracks, getting track features")
    getmusicfromSpotify.create_track_features(test_track_list, user)
    unfeatured_tests = getmusicfromSpotify.remove_unfeatured_tracks(test_track_list)
    if unfeatured_tests != []:
        print("Could not find all tracks. Missing tracks: ", end='')
        for missing_track in unfeatured_tests:
            print(missing_track.name, end=' ')
            print()
    else:
        print("Received track features")

    liked_tracks, disliked_tracks = classifier.classify_tracks(clf, test_track_list)
    print("---------------------------------------------------------")
    print("Predicted liked tracks:")
    for track in liked_tracks:
        print(track)
    print("---------------------------------------------------------")
    print("Predicted disliked tracks:")
    for track in disliked_tracks:
        print(track)
    print("---------------------------------------------------------")
    test_again = input("Would you like to test another playlist?. Enter y for yes or anything else for no: ")
    if test_again != "y":
        break
print("Thank you for using Music Recommender")
