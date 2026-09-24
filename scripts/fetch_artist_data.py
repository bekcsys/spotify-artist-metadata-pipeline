#!/usr/bin/env python3
import time
from pathlib import Path

import pandas as pd

from spotify_client import setup_spotify_client

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "artists_spotify_ids_with_uri.csv"
OUTPUT_FILE = ROOT / "data" / "artists_metadata.csv"
BATCH_SIZE = 10
SLEEP_SECONDS = 1


def extract_artist_id_from_uri(uri: str) -> str:
    return uri.split("/")[-1]


def fetch_artist_data(
    input_file: Path = INPUT_FILE,
    output_file: Path = OUTPUT_FILE,
    batch_size: int = BATCH_SIZE,
) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}. Run add_spotify_uri.py first."
        )

    sp = setup_spotify_client()
    df = pd.read_csv(input_file)
    artist_data = []
    total_artists = len(df)
    total_batches = (total_artists + batch_size - 1) // batch_size

    print(f"Fetching data for {total_artists} artists in {total_batches} batches")

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_artists)
        print(f"Batch {batch_num + 1}/{total_batches} (rows {start_idx + 1}-{end_idx})")

        for idx in range(start_idx, end_idx):
            row = df.iloc[idx]
            try:
                artist_id = extract_artist_id_from_uri(row["SpotifyURI"])
                artist_info = sp.artist(artist_id) or {}
                followers_data = artist_info.get("followers") or {}
                images_data = artist_info.get("images") or []
                artist_data.append(
                    {
                        "name": artist_info.get("name", ""),
                        "followers": followers_data.get("total", 0),
                        "popularity": artist_info.get("popularity", 0),
                        "image_url": images_data[0].get("url", "") if images_data else "",
                        "href": artist_info.get("href", ""),
                        "genres": ",".join(artist_info.get("genres", [])),
                    }
                )
            except Exception as exc:
                print(f"Error processing {row.get('artistLabel', 'Unknown')}: {exc}")
                artist_data.append(
                    {
                        "name": row.get("artistLabel", ""),
                        "followers": 0,
                        "popularity": 0,
                        "image_url": "",
                        "href": "",
                        "genres": "",
                    }
                )

        if batch_num < total_batches - 1:
            time.sleep(SLEEP_SECONDS)

    result_df = pd.DataFrame(artist_data)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_file, index=False)
    print(f"Wrote {len(result_df)} rows to {output_file}")
    return result_df


if __name__ == "__main__":
    fetch_artist_data()
