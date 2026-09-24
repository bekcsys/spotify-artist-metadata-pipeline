import os

from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()


def setup_spotify_client() -> Spotify:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env"
        )

    return Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )
