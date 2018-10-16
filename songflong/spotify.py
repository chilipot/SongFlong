import spotipy
from spotipy import oauth2
import spotipy.util as util

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'fdc64931f71d4b1b86d172dc7f113ec2'
SPOTIPY_CLIENT_SECRET = 'fdc64931f71d4b1b86d172dc7f113ec2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'


# client_credentials_manager = SpotifyClientCredentials('https://accounts.spotify.com/api/fdc64931f71d4b1b86d172dc7f113ec2', 'fdc64931f71d4b1b86d172dc7f113ec2')

token = util.oauth2.SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

results1 = spotify.user_playlist_tracks(USER, PLAY_LIST, limit=100, offset=0)
