import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import spotipy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from spotify_client import setup_spotify_client


def get_top_artists_by_popularity(sp: spotipy.Spotify, limit: int = 50) -> List[Dict[str, Any]]:
    """Get top artists by popularity score"""
    artists = []

    # Get multiple pages of top artists
    for offset in range(0, limit, 20):
        batch_size = min(20, limit - offset)
        if batch_size <= 0:
            break

        try:
            # Get top tracks globally to find popular artists
            top_tracks = sp.playlist_tracks(
                '37i9dQZEVXbMDoHDwVN2tF')  # Global Top 50 playlist
            if top_tracks and 'items' in top_tracks:
                for item in top_tracks['items']:
                    if item and 'track' in item and item['track']:
                        track = item['track']
                        if 'artists' in track and track['artists']:
                            for artist in track['artists']:
                                if artist and 'id' in artist:
                                    # Get detailed artist info
                                    try:
                                        artist_details = sp.artist(
                                            artist['id'])
                                        if artist_details:
                                            artists.append({
                                                'id': artist_details['id'],
                                                'name': artist_details['name'],
                                                'popularity': artist_details['popularity'],
                                                'followers': artist_details['followers']['total'],
                                                'genres': ', '.join(artist_details['genres']),
                                                'spotify_url': artist_details['external_urls']['spotify']
                                            })
                                    except Exception as e:
                                        print(
                                            f"Error getting artist details: {e}")
                                        continue
        except Exception as e:
            print(f"Error getting top tracks: {e}")
            break

    # Remove duplicates and sort by popularity
    unique_artists = {}
    for artist in artists:
        if artist['id'] not in unique_artists:
            unique_artists[artist['id']] = artist

    return sorted(unique_artists.values(), key=lambda x: x['popularity'], reverse=True)


def get_artist_streaming_data(sp: spotipy.Spotify, artist_id: str) -> Dict[str, Any]:
    """Get additional streaming data for an artist"""
    try:
        # Get artist's top tracks
        top_tracks = sp.artist_top_tracks(artist_id)
        total_streams_estimate = 0

        if top_tracks and 'tracks' in top_tracks:
            for track in top_tracks['tracks']:
                # Estimate streams based on popularity (this is approximate)
                popularity = track.get('popularity', 0)
                estimated_streams = popularity * 1000000  # Rough estimate
                total_streams_estimate += estimated_streams

        return {
            'total_streams_estimate': total_streams_estimate,
            'top_tracks_count': len(top_tracks.get('tracks', [])) if top_tracks else 0
        }
    except Exception as e:
        print(f"Error getting streaming data for artist {artist_id}: {e}")
        return {'total_streams_estimate': 0, 'top_tracks_count': 0}


def main():
    """Main function to find top streamers"""
    try:
        print("Setting up Spotify client...")
        sp = setup_spotify_client()

        print("Finding artists on Global Top 50...")
        top_artists = get_top_artists_by_popularity(sp, limit=100)

        print(f"Analyzing {len(top_artists)} artists...")

        # Get additional streaming data for top 10
        top_10_artists = []
        for i, artist in enumerate(top_artists[:10]):
            print(f"Analyzing {i+1}/10: {artist['name']}")
            streaming_data = get_artist_streaming_data(sp, artist['id'])
            artist.update(streaming_data)
            top_10_artists.append(artist)

        # Create DataFrame for better display
        df = pd.DataFrame(top_10_artists)
        df = df[['name', 'popularity', 'followers',
                 'total_streams_estimate', 'genres', 'spotify_url']]

        print("\nTOP ARTISTS FROM SPOTIFY GLOBAL TOP 50:")
        print("=" * 80)

        for i, (_, row) in enumerate(df.iterrows(), 1):
            print(f"{i:2d}. {row['name']}")
            print(f"    Popularity: {row['popularity']}/100")
            print(f"    Followers: {row['followers']:,}")
            print(
                f"    Estimated Streams: {row['total_streams_estimate']:,.0f}")
            print(f"    Genres: {row['genres'][:50]}...")
            print(f"    Spotify: {row['spotify_url']}")
            print()

        # Save to CSV
        df.to_csv('top_10_streamers.csv', index=False)
        print("Results saved to 'top_10_streamers.csv'")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
