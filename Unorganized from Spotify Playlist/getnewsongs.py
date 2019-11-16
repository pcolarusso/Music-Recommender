import spotipy
import spotipy.util as util
import authtoken
from getlikedmusic import Track, create_tracks


def generate_sample_data(track_list):
    sample_data = []
    for track in track_list:
        sample_data.append(track.get_all_features())
    return sample_data

ustop50id = '37i9dQZEVXbLRQDuF5jeBp'

scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'

username = "pecolarusso"

token = util.prompt_for_user_token(username, scope, authtoken.CLIENT_ID, authtoken.ClIENT_SECRET, authtoken.REDIRECT_URL)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

track_ids = []
track_list = []

top50tracks= sp.user_playlist_tracks(username, ustop50id, None, 50, 0)
for item in top50tracks['items']:
    trackid = item['track']['id']
    track_list.append(Track(item['track']['name'], trackid))
    track_ids.append(trackid)


create_tracks(track_ids, len(track_ids), track_list, sp)
sample_data = generate_sample_data(track_list)
print(sample_data)



