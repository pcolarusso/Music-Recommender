
import spotipy
import spotipy.util as util


CLIENT_ID = "Client ID goes here"
ClIENT_SECRET = "Client Secret ID goes here"
REDIRECT_URL = "http://localhost/"


def get_credentials(username):
    """Prompt user to enter credentials, redirects user to website to agree to data collection, returns user object"""
    scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private'
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, ClIENT_SECRET, REDIRECT_URL)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        raise Exception("Can't get token for " + username)
    return sp
