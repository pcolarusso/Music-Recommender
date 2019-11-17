
import spotipy
import spotipy.util as util
import authtoken

class Track(object):
    def __init__ (self, name, id):
        self.name = name
        self.id = id
        self.acousticness = None
        self.danceability = None
        self.energy = None
        self.instrumentalness = None
        self.key = None
        self.liveness = None
        self.loudness = None
        self.mode = None
        self.speechiness = None
        self.tempo = None
        self.time_signature = None
        self.valence = None
    def set_all_features(self, features):
        self.acousticness = features['acousticness']
        self.danceability = features['danceability']
        self.energy = features['energy']
        self.instrumentalness = features['instrumentalness']
        self.key = features['key']
        self.liveness = features['liveness']
        self.loudness = features['loudness']
        self.mode = features['mode']
        self.speechiness = features['speechiness']
        self.tempo = features['tempo']
        self.time_signature = features['time_signature']
        self.valence = features['valence']
    def get_all_features(self):
        return [self.acousticness, self.danceability, self.energy, self.instrumentalness, self.key, self.liveness,
        self.loudness, self.mode, self.speechiness, self.tempo, self.time_signature, self.valence]
    def has_features_check(self):
        features = self.get_all_features()
        for feature in features:
            if feature == None:
                return False
        return True

    def __str__(self):
        return [self.name] + self.get_all_features()

def get_user_playlists(user_playlists):
    playlists = {} #playlists format is {'playlist_name' : ['id', number_of_tracks]}
    for item in user_playlists['items']:
        playlists[item['name']] =  [item['id'], item['tracks']['total']]
    return playlists

# def create_tracks(track_id_list, number_of_tracks, track_list):
#     for i in range(0, number_of_tracks, 50):
#         if i + 50 < number_of_tracks:
#             features = sp.audio_features(track_id_list[i:i+50])
#         else:
#             features = sp.audio_features(track_id_list[i:])
#
#         for track, track_features in zip(track_list[i:], features):
#             track.set_all_features(track_features)
#     return track_list


def create_tracks(track_id_list, number_of_tracks, track_list, sp):
    for j in range(0, number_of_tracks, 50):
        if j + 50 < number_of_tracks:
            features = sp.audio_features(track_id_list[j:j+50])
        else:
            features = sp.audio_features(track_id_list[j:])

        for track, track_features in zip(track_list[j:], features):
            track.set_all_features(track_features)
    return track_list

def generate_train_data(track_list):
    train_data = []
    for track in track_list:
        train_data.append(track.get_all_features())
    return train_data

def get_list_of_curated_playlist:



if __name__ == "__main__":
    scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'

    username = "pecolarusso"

    token = util.prompt_for_user_token(username, scope, authtoken.CLIENT_ID, authtoken.ClIENT_SECRET, authtoken.REDIRECT_URL)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)

    results = sp.current_user_playlists()
    all_playlists = {}
    offset = 0
    i=0

    while(True):
        results = sp.current_user_playlists(50, offset)
        if results['items'] == []:
            break
        all_playlists.update(get_user_playlists(results))
        offset += 50
    for playlist in all_playlists:
        print(playlist)

    while(True):
        chosen_playlist = input("Enter name of playlist containing songs for recommendations to be derived from: ")
        #chosen_playlist = 'Music Recommender'
        if chosen_playlist not in all_playlists:
            print("Playlist does not exist")
        else:
            break
    print(all_playlists[chosen_playlist][0])
    #exit(0)
    track_ids= []
    track_list =[]

    for offset in range(0, all_playlists[chosen_playlist][1], 100):
        playlist_info = sp.user_playlist_tracks(username, all_playlists[chosen_playlist][0], None, 100, offset)
        for item in playlist_info['items']:
            trackid = item['track']['id']
            track_list.append(Track(item['track']['name'], trackid))
            track_ids.append(trackid)

    number_of_tracks = len(track_ids)
    print(all_playlists[chosen_playlist][1])
    print(number_of_tracks)
    assert number_of_tracks == all_playlists[chosen_playlist][1], "Number of tracks collected does not equal number of tracks in playlist"

    create_tracks(track_ids, number_of_tracks, track_list, sp)

    train_data = generate_train_data(track_list)
    print(train_data)


