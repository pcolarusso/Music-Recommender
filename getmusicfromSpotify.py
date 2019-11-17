
import spotipy
import spotipy.util as util
import authtoken
from Track import Track

curated_playlists = { #contains spotify curated playlist IDS, key is playlist name and maps to playlist ID and length
    "US Top 50" : ['37i9dQZEVXbLRQDuF5jeBp', 50]
}


def get_credentials(username):
    """Prompt user to enter credentials, redirects user to website to agree to data collection, returns user object"""
    scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'
    token = util.prompt_for_user_token(username, scope, authtoken.CLIENT_ID, authtoken.ClIENT_SECRET, authtoken.REDIRECT_URL)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    return sp


def get_user_playlists(user):
    """Returns a dictionary of user's playlists, dictionary key is name and maps to list of playlist ID and length"""
    all_playlists = {}
    offset = 0
    while(True):
        results = user.current_user_playlists(50, offset)
        if results['items'] == []:
            break
        for item in results['items']:
            all_playlists[item['name']] = [item['id'], item['tracks']['total']]
        offset += 50
    return all_playlists


def get_track_names_ids(playlist_id, playlist_length):
    """Returns a list of tracks with track names and IDs"""
    list_of_tracks =[]
    for offset in range(0, playlist_length, 100):
        playlist_info = sp.user_playlist_tracks(username, playlist_id, None, 100, offset)
        for item in playlist_info['items']:
            track_id = item['track']['id']
            list_of_tracks.append(Track(item['track']['name'], track_id))
    return list_of_tracks


def create_track_features(list_of_tracks, user):
    """Sets track features for given tracks"""
    number_of_tracks = len(list_of_tracks)
    for i in range(0, number_of_tracks, 50):
        track_id_list = []
        if i + 50 < number_of_tracks:
            for track in list_of_tracks[i:i+50]:
                track_id_list.append(track.id)
        else:
            for track in list_of_tracks[i:]:
                track_id_list.append(track.id)
        features = user.audio_features(track_id_list)
        for track, track_features in zip(list_of_tracks[i:], features):
            track.set_all_features(track_features)


def get_track_features(list_of_tracks):
    """Returns a list of only track features grouped by track"""
    features = []
    for track in list_of_tracks:
        features.append(track.get_all_features())
    return features

def list_of_curated_playlist():
    """Returns a list of the names of playlists provided in the curated_playlists dictionary
    These playlists are predetermined and can be added to by adding to curated_playlists"""
    return list(curated_playlists.keys())

def get_curated_playlist_id(playlist_name):
    """Returns the ID and length of specified curated playlist"""
    return curated_playlists[playlist_name]


if __name__ == "__main__":

    username = "pecolarusso"

    sp = get_credentials(username)

    playlists = get_user_playlists(sp)

    for playlist in playlists:
        print(playlist)

    while(True):
        chosen_playlist = input("Enter name of playlist containing songs for recommendations to be derived from: ")
        if chosen_playlist not in playlists:
            print("Playlist does not exist")
        else:
            break

    track_list = get_track_names_ids(playlists[chosen_playlist][0], playlists[chosen_playlist][1])

    create_track_features(track_list, sp)
    print(track_list)

