"""
Music Utilities Module
Contains helper functions, decorators, and lambda operations for the Music Recommendation System
"""

import csv
import time
from functools import wraps
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter


# ============================================
# DECORATOR: Measure Recommendation Time
# ============================================
def measure_time(func):
    """
    Decorator to measure the execution time of recommendation functions
    Prints the time taken to generate recommendations
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️  Recommendation generated in {execution_time:.4f} seconds")
        return result
    return wrapper


# ============================================
# CSV LOADING FUNCTIONS
# ============================================
def load_songs_from_csv(filename='songs.csv'):
    """
    Load songs from CSV file and return as list of dictionaries
    Handles missing files and validates data
    """
    songs = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Validate that all required fields are present
                if validate_song_data(row):
                    # Convert popularity to integer
                    row['popularity'] = int(row['popularity'])
                    songs.append(row)
                else:
                    print(f"⚠️  Skipping invalid song entry: {row}")
        print(f"✅ Loaded {len(songs)} songs from {filename}")
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
    except Exception as e:
        print(f"❌ Error loading songs: {e}")
    
    return songs


def load_playlist_history(filename='playlist_history.csv'):
    """
    Load user playlist history from CSV file
    Returns list of dictionaries with user listening data
    """
    history = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                history.append(row)
        print(f"✅ Loaded {len(history)} history entries from {filename}")
    except FileNotFoundError:
        print(f"⚠️  {filename} not found. Starting with empty history.")
    except Exception as e:
        print(f"❌ Error loading history: {e}")
    
    return history


# ============================================
# DATA VALIDATION
# ============================================
def validate_song_data(song):
    """
    Validate that song data contains all required fields
    Returns True if valid, False otherwise
    """
    required_fields = ['song_name', 'artist', 'genre', 'mood', 'popularity']
    
    for field in required_fields:
        if field not in song or not song[field]:
            print(f"❌ Missing or empty field: {field}")
            return False
    
    # Validate popularity is a number
    try:
        int(song['popularity'])
    except ValueError:
        print(f"❌ Invalid popularity value: {song['popularity']}")
        return False
    
    return True


def check_duplicate_song(songs, new_song_name):
    """
    Check if a song already exists in the songs list
    Returns True if duplicate found, False otherwise
    """
    # Use list comprehension to find duplicates
    duplicates = [song for song in songs if song['song_name'].lower() == new_song_name.lower()]
    return len(duplicates) > 0


# ============================================
# LAMBDA FUNCTIONS FOR SORTING
# ============================================
def sort_by_popularity(songs):
    """
    Sort songs by popularity using lambda function
    Returns sorted list in descending order
    """
    return sorted(songs, key=lambda x: x['popularity'], reverse=True)


def get_top_songs(songs, n=10):
    """
    Get top N most popular songs using lambda
    """
    sorted_songs = sort_by_popularity(songs)
    return sorted_songs[:n]


# ============================================
# LIST COMPREHENSIONS FOR FILTERING
# ============================================
def filter_by_genre(songs, genre):
    """
    Filter songs by genre using list comprehension
    Case-insensitive matching
    """
    return [song for song in songs if song['genre'].lower() == genre.lower()]


def filter_by_mood(songs, mood):
    """
    Filter songs by mood using list comprehension
    Case-insensitive matching
    """
    return [song for song in songs if song['mood'].lower() == mood.lower()]


def filter_by_genre_and_mood(songs, genre, mood):
    """
    Filter songs by both genre and mood using list comprehension
    """
    return [song for song in songs 
            if song['genre'].lower() == genre.lower() 
            and song['mood'].lower() == mood.lower()]


def filter_by_popularity_threshold(songs, min_popularity=80):
    """
    Filter songs above a certain popularity threshold
    """
    return [song for song in songs if song['popularity'] >= min_popularity]


# ============================================
# CSV SAVING FUNCTIONS
# ============================================
def save_playlist_to_csv(username, playlist, filename='my_playlist.csv'):
    """
    Save user's playlist to a CSV file
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            if playlist:
                fieldnames = ['username', 'song_name', 'artist', 'genre', 'mood', 'popularity']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for song in playlist:
                    row = {
                        'username': username,
                        'song_name': song['song_name'],
                        'artist': song['artist'],
                        'genre': song['genre'],
                        'mood': song['mood'],
                        'popularity': song['popularity']
                    }
                    writer.writerow(row)
        print(f"✅ Playlist saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving playlist: {e}")
        return False


def append_to_history(username, song, filename='playlist_history.csv'):
    """
    Append a song to the user's listening history
    """
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['username', 'song_name', 'timestamp', 'genre', 'mood']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Check if file is empty to write header
            file.seek(0, 2)  # Go to end of file
            if file.tell() == 0:
                writer.writeheader()
            
            row = {
                'username': username,
                'song_name': song['song_name'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'genre': song['genre'],
                'mood': song['mood']
            }
            writer.writerow(row)
        return True
    except Exception as e:
        print(f"❌ Error appending to history: {e}")
        return False


# ============================================
# VISUALIZATION FUNCTIONS
# ============================================
def visualize_genre_preferences(playlist):
    """
    Create a bar chart showing genre distribution in playlist
    """
    if not playlist:
        print("❌ No songs in playlist to visualize!")
        return
    
    # Count genres using Counter
    genres = [song['genre'] for song in playlist]
    genre_counts = Counter(genres)
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(genre_counts.keys(), genre_counts.values(), color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
    plt.xlabel('Genre', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Songs', fontsize=12, fontweight='bold')
    plt.title('Genre Distribution in Your Playlist', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('genre_preferences.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Genre preference chart saved as 'genre_preferences.png'")


def visualize_mood_distribution(playlist):
    """
    Create a pie chart showing mood distribution in playlist
    """
    if not playlist:
        print("❌ No songs in playlist to visualize!")
        return
    
    # Count moods using Counter
    moods = [song['mood'] for song in playlist]
    mood_counts = Counter(moods)
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    colors = ['#FFD93D', '#6BCB77', '#4D96FF', '#FF6B9D', '#C780FA']
    explode = [0.05] * len(mood_counts)  # Explode all slices slightly
    
    plt.pie(mood_counts.values(), 
            labels=mood_counts.keys(), 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(mood_counts)],
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    plt.title('Mood Distribution in Your Playlist', fontsize=14, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('mood_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Mood distribution chart saved as 'mood_distribution.png'")


def visualize_both(playlist):
    """
    Create both visualizations side by side
    """
    if not playlist:
        print("❌ No songs in playlist to visualize!")
        return
    
    # Count genres and moods
    genres = [song['genre'] for song in playlist]
    moods = [song['mood'] for song in playlist]
    genre_counts = Counter(genres)
    mood_counts = Counter(moods)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart for genres
    ax1.bar(genre_counts.keys(), genre_counts.values(), 
            color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
    ax1.set_xlabel('Genre', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Songs', fontsize=12, fontweight='bold')
    ax1.set_title('Genre Distribution', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # Pie chart for moods
    colors = ['#FFD93D', '#6BCB77', '#4D96FF', '#FF6B9D', '#C780FA']
    explode = [0.05] * len(mood_counts)
    ax2.pie(mood_counts.values(), 
            labels=mood_counts.keys(), 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(mood_counts)],
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Mood Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('playlist_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Complete playlist analysis saved as 'playlist_analysis.png'")


# ============================================
# REPORTING FUNCTIONS
# ============================================
def generate_recommendation_report(username, playlist, criteria):
    """
    Generate a text-based recommendation report
    """
    report = []
    report.append("=" * 60)
    report.append("🎵  MUSIC RECOMMENDATION REPORT")
    report.append("=" * 60)
    report.append(f"User: {username}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Criteria: {criteria}")
    report.append(f"Total Songs Recommended: {len(playlist)}")
    report.append("=" * 60)
    report.append("")
    
    if playlist:
        # Calculate statistics
        avg_popularity = sum([song['popularity'] for song in playlist]) / len(playlist)
        genres = Counter([song['genre'] for song in playlist])
        moods = Counter([song['mood'] for song in playlist])
        
        report.append("📊 STATISTICS:")
        report.append(f"   Average Popularity: {avg_popularity:.2f}/100")
        report.append(f"   Genres: {dict(genres)}")
        report.append(f"   Moods: {dict(moods)}")
        report.append("")
        
        report.append("💿 RECOMMENDED SONGS:")
        report.append("-" * 60)
        for idx, song in enumerate(playlist, 1):
            report.append(f"{idx}. {song['song_name']}")
            report.append(f"   Artist: {song['artist']}")
            report.append(f"   Genre: {song['genre']} | Mood: {song['mood']} | Popularity: {song['popularity']}/100")
            report.append("")
    else:
        report.append("❌ No songs found matching your criteria!")
    
    report.append("=" * 60)
    
    report_text = "\n".join(report)
    print(report_text)
    
    # Save report to file
    filename = f"recommendation_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\n✅ Report saved to {filename}")
    
    return report_text


def display_songs_table(songs, title="Songs"):
    """
    Display songs in a formatted table
    """
    if not songs:
        print(f"\n❌ No {title.lower()} to display!")
        return
    
    print(f"\n{'=' * 100}")
    print(f"🎵  {title.upper()}")
    print(f"{'=' * 100}")
    print(f"{'#':<4} {'Song Name':<30} {'Artist':<20} {'Genre':<12} {'Mood':<12} {'Pop':<5}")
    print(f"{'-' * 100}")
    
    for idx, song in enumerate(songs, 1):
        song_name = song['song_name'][:28] + '..' if len(song['song_name']) > 30 else song['song_name']
        artist = song['artist'][:18] + '..' if len(song['artist']) > 20 else song['artist']
        print(f"{idx:<4} {song_name:<30} {artist:<20} {song['genre']:<12} {song['mood']:<12} {song['popularity']:<5}")
    
    print(f"{'=' * 100}\n")
