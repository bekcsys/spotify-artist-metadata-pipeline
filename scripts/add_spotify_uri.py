#!/usr/bin/env python3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "artists_spotify_ids.csv"
OUTPUT_FILE = ROOT / "data" / "artists_spotify_ids_with_uri.csv"
SPOTIFY_ARTIST_BASE_URL = "https://open.spotify.com/artist/"


def add_spotify_uri(
    input_file: Path = INPUT_FILE,
    output_file: Path = OUTPUT_FILE,
) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)
    df["SpotifyURI"] = SPOTIFY_ARTIST_BASE_URL + df["spotifyID"]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Wrote {len(df)} rows to {output_file}")
    return df


if __name__ == "__main__":
    add_spotify_uri()
