import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2bd3abf122f54dd0b16eedfa81d2160c",
                                               client_secret="be6572cfc34e48e6a16c49b1eaf87929",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-library-read user-top-read"))

