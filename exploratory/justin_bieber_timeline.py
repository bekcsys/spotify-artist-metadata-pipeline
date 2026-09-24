import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import matplotlib.pyplot as plt
import pandas as pd
import spotipy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from spotify_client import setup_spotify_client


def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"


def estimate_monthly_listeners(popularity: int, followers: int, year_factor: float = 1.0) -> int:
    """Estimate monthly listeners based on popularity, followers, and year factor"""
    # Base estimation: monthly listeners ≈ followers * (popularity/100) * 0.3
    base_estimate = int(followers * (popularity / 100) * 0.3)

    # Apply year factor to simulate growth over time
    return int(base_estimate * year_factor)


def get_justin_bieber_current_data(sp: spotipy.Spotify) -> Dict[str, Any]:
    """Get current Justin Bieber data from Spotify"""
    justin_bieber_id = "1uNFoZAHBGtllmzznpCI3s"

    try:
        artist = sp.artist(justin_bieber_id)
        if not artist:
            raise Exception("Could not fetch artist data")

        # Get top tracks for additional analysis
        top_tracks = sp.artist_top_tracks(justin_bieber_id)

        return {
            'name': artist['name'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total'],
            'genres': artist['genres'],
            'top_tracks': top_tracks.get('tracks', []) if top_tracks else [],
            'spotify_url': artist['external_urls']['spotify']
        }
    except Exception as e:
        print(f"Error fetching current data: {e}")
        return {}


def create_historical_timeline() -> List[Dict[str, Any]]:
    """Create historical timeline for Justin Bieber's career"""
    # Historical data based on known career milestones and estimated growth
    timeline_data = [
        # 2009 - My World EP
        {'year': 2009, 'month': 7, 'event': 'My World EP Release',
            'estimated_popularity': 20, 'estimated_followers': 100000},
        {'year': 2009, 'month': 12, 'event': 'My World 2.0 Release',
            'estimated_popularity': 35, 'estimated_followers': 500000},

        # 2010 - My World 2.0 and Baby
        {'year': 2010, 'month': 3, 'event': 'Baby Music Video Release',
            'estimated_popularity': 50, 'estimated_followers': 2000000},
        {'year': 2010, 'month': 6, 'event': 'Baby Peak Popularity',
            'estimated_popularity': 85, 'estimated_followers': 5000000},
        {'year': 2010, 'month': 12, 'event': 'End of 2010',
            'estimated_popularity': 75, 'estimated_followers': 8000000},

        # 2011 - Under the Mistletoe
        {'year': 2011, 'month': 11, 'event': 'Under the Mistletoe Release',
            'estimated_popularity': 80, 'estimated_followers': 12000000},
        {'year': 2011, 'month': 12, 'event': 'End of 2011',
            'estimated_popularity': 78, 'estimated_followers': 15000000},

        # 2012 - Believe
        {'year': 2012, 'month': 6, 'event': 'Believe Album Release',
            'estimated_popularity': 85, 'estimated_followers': 20000000},
        {'year': 2012, 'month': 12, 'event': 'End of 2012',
            'estimated_popularity': 82, 'estimated_followers': 25000000},

        # 2013-2014 - Journals
        {'year': 2013, 'month': 12, 'event': 'Journals Release',
            'estimated_popularity': 75, 'estimated_followers': 30000000},
        {'year': 2014, 'month': 12, 'event': 'End of 2014',
            'estimated_popularity': 70, 'estimated_followers': 35000000},

        # 2015 - Purpose Era
        {'year': 2015, 'month': 8, 'event': 'What Do You Mean? Release',
            'estimated_popularity': 90, 'estimated_followers': 40000000},
        {'year': 2015, 'month': 11, 'event': 'Purpose Album Release',
            'estimated_popularity': 95, 'estimated_followers': 45000000},
        {'year': 2015, 'month': 12, 'event': 'End of 2015',
            'estimated_popularity': 92, 'estimated_followers': 50000000},

        # 2016 - Purpose Peak
        {'year': 2016, 'month': 6, 'event': 'Purpose Peak Popularity',
            'estimated_popularity': 98, 'estimated_followers': 60000000},
        {'year': 2016, 'month': 12, 'event': 'End of 2016',
            'estimated_popularity': 95, 'estimated_followers': 65000000},

        # 2017-2019 - Changes Era
        {'year': 2017, 'month': 12, 'event': 'End of 2017',
            'estimated_popularity': 88, 'estimated_followers': 70000000},
        {'year': 2018, 'month': 12, 'event': 'End of 2018',
            'estimated_popularity': 85, 'estimated_followers': 75000000},
        {'year': 2019, 'month': 12, 'event': 'End of 2019',
            'estimated_popularity': 82, 'estimated_followers': 80000000},

        # 2020 - Changes Album
        {'year': 2020, 'month': 2, 'event': 'Changes Album Release',
            'estimated_popularity': 88, 'estimated_followers': 85000000},
        {'year': 2020, 'month': 12, 'event': 'End of 2020',
            'estimated_popularity': 85, 'estimated_followers': 90000000},

        # 2021 - Justice Album
        {'year': 2021, 'month': 3, 'event': 'Justice Album Release',
            'estimated_popularity': 90, 'estimated_followers': 95000000},
        {'year': 2021, 'month': 12, 'event': 'End of 2021',
            'estimated_popularity': 87, 'estimated_followers': 100000000},

        # 2022-2023 - Recent Years
        {'year': 2022, 'month': 12, 'event': 'End of 2022',
            'estimated_popularity': 84, 'estimated_followers': 105000000},
        {'year': 2023, 'month': 12, 'event': 'End of 2023',
            'estimated_popularity': 82, 'estimated_followers': 110000000},

        # 2024 - Current
        {'year': 2024, 'month': datetime.now().month, 'event': 'Current',
         'estimated_popularity': 81, 'estimated_followers': 115000000}
    ]

    return timeline_data


def analyze_justin_bieber_timeline(sp: spotipy.Spotify):
    """Analyze Justin Bieber's monthly listeners timeline"""
    print("JUSTIN BIEBER - ESTIMATED MONTHLY LISTENERS TIMELINE")
    print("=" * 60)

    # Get current data
    current_data = get_justin_bieber_current_data(sp)
    if current_data:
        print(f"Current Status ({datetime.now().strftime('%B %Y')}):")
        print(f"  Name: {current_data['name']}")
        print(f"  Current Popularity: {current_data['popularity']}/100")
        print(
            f"  Current Followers: {format_number(current_data['followers'])}")
        print(f"  Genres: {', '.join(current_data['genres'])}")
        print()

    # Create historical timeline
    timeline = create_historical_timeline()

    # Calculate monthly listeners for each point
    for entry in timeline:
        monthly_listeners = estimate_monthly_listeners(
            entry['estimated_popularity'],
            entry['estimated_followers']
        )
        entry['monthly_listeners'] = monthly_listeners

    # Create DataFrame for analysis
    df = pd.DataFrame(timeline)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

    # Display timeline
    print("CAREER TIMELINE & ESTIMATED MONTHLY LISTENERS")
    print("-" * 60)

    for _, row in df.iterrows():
        date_str = pd.to_datetime(row['date']).strftime('%B %Y')
        print(f"{date_str:12} | {row['event']:25} | "
              f"Popularity: {row['estimated_popularity']:2d}/100 | "
              f"Followers: {format_number(row['estimated_followers']):>12} | "
              f"Monthly Listeners: {format_number(row['monthly_listeners']):>12}")

    # Save to CSV
    output_df = df[['date', 'event', 'estimated_popularity',
                    'estimated_followers', 'monthly_listeners']].copy()
    output_df.columns = ['Date', 'Event',
                         'Popularity', 'Followers', 'Monthly_Listeners']
    output_df.to_csv('justin_bieber_timeline.csv', index=False)
    print(f"\nTimeline data saved to 'justin_bieber_timeline.csv'")

    # Create visualization
    try:
        plt.figure(figsize=(15, 10))

        # Plot 1: Monthly Listeners over time
        plt.subplot(2, 1, 1)
        plt.plot(df['date'], df['monthly_listeners'],
                 marker='o', linewidth=2, markersize=6)
        plt.title('Justin Bieber - Estimated Monthly Listeners Over Time',
                  fontsize=16, fontweight='bold')
        plt.ylabel('Monthly Listeners', fontsize=12)
        plt.grid(True, alpha=0.3)

        # Add annotations for major events
        major_events = ['My World EP Release', 'Baby Peak Popularity', 'Purpose Album Release',
                        'Purpose Peak Popularity', 'Changes Album Release', 'Justice Album Release']
        for _, row in df.iterrows():
            if any(event in row['event'] for event in major_events):
                plt.annotate(row['event'], (row['date'], row['monthly_listeners']),
                             xytext=(10, 10), textcoords='offset points',
                             fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

        # Plot 2: Popularity and Followers
        plt.subplot(2, 1, 2)
        ax1 = plt.gca()
        ax2 = ax1.twinx()

        line1 = ax1.plot(df['date'], df['estimated_popularity'],
                         'b-', marker='o', label='Popularity', linewidth=2)
        line2 = ax2.plot(df['date'], df['estimated_followers']/1000000,
                         'r-', marker='s', label='Followers (M)', linewidth=2)

        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('Popularity Score', color='b', fontsize=12)
        ax2.set_ylabel('Followers (Millions)', color='r', fontsize=12)
        ax1.grid(True, alpha=0.3)

        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')

        plt.title('Popularity Score and Follower Growth',
                  fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save plot
        plt.savefig('justin_bieber_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'justin_bieber_analysis.png'")

    except Exception as e:
        print(f"Could not create visualization: {e}")
        print("Install matplotlib: pipenv install matplotlib")

    # Summary statistics
    print(f"\nSUMMARY STATISTICS")
    print("-" * 40)
    print(
        f"Peak Monthly Listeners: {format_number(df['monthly_listeners'].max())} ({df.loc[df['monthly_listeners'].idxmax(), 'event']})")
    print(
        f"Current Monthly Listeners: {format_number(df['monthly_listeners'].iloc[-1])}")
    print(
        f"Average Monthly Listeners: {format_number(int(df['monthly_listeners'].mean()))}")
    print(
        f"Total Career Growth: {format_number(df['monthly_listeners'].iloc[-1] - df['monthly_listeners'].iloc[0])} listeners")


def main():
    """Main function"""
    try:
        print("Setting up Spotify client...")
        sp = setup_spotify_client()

        analyze_justin_bieber_timeline(sp)

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your .env file contains valid Spotify credentials")


if __name__ == "__main__":
    main()
