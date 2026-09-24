#!/usr/bin/env python3
import csv
import time
from pathlib import Path

import requests

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
PAGE_SIZE = 100
MAX_ROWS = 1000
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "data" / "wikidata_artist_spotify_ids.csv"
USER_AGENT = "spotify-metadata-ingestion/1.0"


def build_query(limit: int, offset: int) -> str:
    return f"""
    SELECT ?artist ?artistLabel ?spotifyID WHERE {{
      ?artist wdt:P31 wd:Q5;
              wdt:P106 wd:Q639669;
              wdt:P1902 ?spotifyID.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    OFFSET {offset}
    """


def parse_bindings(bindings: list[dict]) -> list[dict]:
    rows = []
    for binding in bindings:
        spotify_id = binding["spotifyID"]["value"]
        rows.append(
            {
                "name": binding["artistLabel"]["value"],
                "wikidata_id": binding["artist"]["value"].split("/")[-1],
                "spotify_id": spotify_id,
                "spotify_url": f"https://open.spotify.com/artist/{spotify_id}",
            }
        )
    return rows


def ingest_artist_ids(
    output_file: Path = OUTPUT_FILE,
    page_size: int = PAGE_SIZE,
    max_rows: int = MAX_ROWS,
) -> list[dict]:
    all_results: list[dict] = []
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": USER_AGENT,
    }

    for offset in range(0, max_rows, page_size):
        print(f"Fetching results {offset} to {offset + page_size}...")
        response = requests.get(
            SPARQL_ENDPOINT,
            params={"query": build_query(page_size, offset)},
            headers=headers,
            timeout=60,
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code}, stopping early.")
            break

        bindings = response.json()["results"]["bindings"]
        if not bindings:
            print("No more data found.")
            break

        all_results.extend(parse_bindings(bindings))
        time.sleep(1)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["name", "wikidata_id", "spotify_id", "spotify_url"],
        )
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Total records fetched: {len(all_results)}")
    print(f"Saved to: {output_file}")
    return all_results


if __name__ == "__main__":
    ingest_artist_ids()
