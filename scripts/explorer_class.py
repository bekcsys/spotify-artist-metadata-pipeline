import json
from typing import Any, Optional

from spotify_client import setup_spotify_client


class SpotifyAPIExplorer:
    def __init__(self) -> None:
        self.sp = setup_spotify_client()
        self.sample_ids = {
            "artist": "3TVXtAsR1Inumwj472S9r4",
            "album": "2HpJwmx54r03VwyL7YMq9u",
            "track": "6rqhFgbbKwnb9MLmUQDhG6",
            "playlist": "37i9dQZEVXbMDoHDwVN2tF",
        }

    def print_fields(self, data: dict[str, Any], title: str = "Available fields") -> None:
        print(f"{title}:")
        for key, value in data.items():
            print(f"   {key}: {type(value).__name__}")

    def print_sample_data(self, data: dict[str, Any], max_length: int = 1000) -> None:
        print("\nSample data:")
        print(json.dumps(data, indent=2)[:max_length] + "...")

    def safe_api_call(self, func, *args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(f"Error: {exc}")
            return None

    def explore_artists(self) -> None:
        artist = self.safe_api_call(self.sp.artist, self.sample_ids["artist"])
        if artist:
            self.print_fields(artist)
            self.print_sample_data(artist)
