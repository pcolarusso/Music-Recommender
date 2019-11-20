
import spotipy
import spotipy.util as util


CLIENT_ID = "d0c3b442f93c414b9c5a73b9cc740fcd"
ClIENT_SECRET = "f21eb9b28d834d3eae94094356ae71c5"
REDIRECT_URL = "http://localhost/"

def get_credentials(username):
    """Prompt user to enter credentials, redirects user to website to agree to data collection, returns user object"""
    scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, ClIENT_SECRET, REDIRECT_URL)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    return sp
