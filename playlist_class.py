"""
Playlist Class Module
Defines the Playlist class with OOP design for music recommendation system
"""

from music_utils import (
    measure_time,
    filter_by_mood,
    filter_by_genre,
    filter_by_genre_and_mood,
    sort_by_popularity,
    save_playlist_to_csv,
    append_to_history,
    load_playlist_history,
    display_songs_table,
    generate_recommendation_report
)
from collections import Counter


class Playlist:
    """
    Playlist class to manage user playlists and recommendations
    
    Attributes:
        username (str): Name of the user
        mood (str): Current mood preference
        songs_list (list): List of songs in the playlist
        all_songs (list): Complete database of available songs
        history (list): User's listening history
    """
    
    def __init__(self, username, mood, all_songs):
        """
        Initialize Playlist object
        
        Args:
            username (str): User's name
            mood (str): User's current mood
            all_songs (list): Complete song database
        """
        self.username = username
        self.mood = mood
        self.songs_list = []
        self.all_songs = all_songs
        self.history = load_playlist_history()
    
    
    def user_profile(self):
        """
        Display user profile information including preferences and statistics
        """
        print("\n" + "=" * 60)
        print("👤  USER PROFILE")
        print("=" * 60)
        print(f"Username: {self.username}")
        print(f"Current Mood: {self.mood}")
        print(f"Songs in Current Playlist: {len(self.songs_list)}")
        
        # Analyze user's listening history
        user_history = [entry for entry in self.history if entry['username'] == self.username]
        
        if user_history:
            print(f"Total Songs in History: {len(user_history)}")
            
            # Most played genres
            genres_played = [entry['genre'] for entry in user_history]
            genre_counts = Counter(genres_played)
            print(f"Favorite Genre: {genre_counts.most_common(1)[0][0] if genre_counts else 'N/A'}")
            
            # Most played moods
            moods_played = [entry['mood'] for entry in user_history]
            mood_counts = Counter(moods_played)
            print(f"Favorite Mood: {mood_counts.most_common(1)[0][0] if mood_counts else 'N/A'}")
            
            # Recent songs
            print(f"\n📜 Recent Listening History:")
            print("-" * 60)
            recent_songs = user_history[-5:]  # Last 5 songs
            for idx, entry in enumerate(reversed(recent_songs), 1):
                print(f"{idx}. {entry['song_name']} ({entry['genre']}) - {entry['timestamp']}")
        else:
            print("No listening history found for this user.")
        
        print("=" * 60 + "\n")
    
    
    @measure_time
    def recommend_songs(self, genre=None, mood=None, count=10):
        """
        Recommend songs based on genre and/or mood preferences
        Uses the @measure_time decorator to track performance
        
        Args:
            genre (str, optional): Preferred genre
            mood (str, optional): Preferred mood
            count (int): Number of songs to recommend
        
        Returns:
            list: Recommended songs
        """
        print(f"\n🔍 Generating recommendations...")
        
        recommended = []
        
        # Filter based on criteria
        if genre and mood:
            print(f"   Filtering by Genre: {genre} and Mood: {mood}")
            recommended = filter_by_genre_and_mood(self.all_songs, genre, mood)
        elif genre:
            print(f"   Filtering by Genre: {genre}")
            recommended = filter_by_genre(self.all_songs, genre)
        elif mood:
            print(f"   Filtering by Mood: {mood}")
            recommended = filter_by_mood(self.all_songs, mood)
        else:
            # If no criteria, recommend based on user's listening history
            print(f"   Analyzing your listening history...")
            recommended = self._recommend_based_on_history()
        
        # Sort by popularity using lambda
        recommended = sort_by_popularity(recommended)
        
        # Limit to requested count
        recommended = recommended[:count]
        
        if recommended:
            print(f"✅ Found {len(recommended)} songs matching your criteria!")
            self.songs_list = recommended
            
            # Display recommendations
            display_songs_table(recommended, "Recommended Songs")
            
            # Generate and save recommendation report
            criteria = f"Genre: {genre or 'Any'}, Mood: {mood or 'Any'}"
            generate_recommendation_report(self.username, recommended, criteria)
        else:
            print("❌ No songs found matching your criteria. Try different filters!")
        
        return recommended
    
    
    def _recommend_based_on_history(self):
        """
        Private method to recommend songs based on user's listening history
        Uses collaborative filtering approach
        
        Returns:
            list: Recommended songs
        """
        user_history = [entry for entry in self.history if entry['username'] == self.username]
        
        if not user_history:
            # If no history, return popular songs
            return sort_by_popularity(self.all_songs)[:20]
        
        # Find user's preferred genres and moods
        genres_played = [entry['genre'] for entry in user_history]
        moods_played = [entry['mood'] for entry in user_history]
        
        genre_counts = Counter(genres_played)
        mood_counts = Counter(moods_played)
        
        # Get top genre and mood
        top_genre = genre_counts.most_common(1)[0][0] if genre_counts else None
        top_mood = mood_counts.most_common(1)[0][0] if mood_counts else None
        
        # Find songs already listened to
        listened_songs = {entry['song_name'] for entry in user_history}
        
        # Recommend songs from favorite genre/mood that haven't been listened to
        recommendations = []
        
        if top_genre and top_mood:
            # Try genre + mood combination first
            candidates = filter_by_genre_and_mood(self.all_songs, top_genre, top_mood)
            recommendations.extend([s for s in candidates if s['song_name'] not in listened_songs])
        
        # If not enough, add from top genre
        if len(recommendations) < 20 and top_genre:
            candidates = filter_by_genre(self.all_songs, top_genre)
            recommendations.extend([s for s in candidates if s['song_name'] not in listened_songs 
                                   and s not in recommendations])
        
        # If still not enough, add from top mood
        if len(recommendations) < 20 and top_mood:
            candidates = filter_by_mood(self.all_songs, top_mood)
            recommendations.extend([s for s in candidates if s['song_name'] not in listened_songs 
                                   and s not in recommendations])
        
        return recommendations if recommendations else self.all_songs
    
    
    def track_history(self, song):
        """
        Track a song in user's listening history
        
        Args:
            song (dict): Song to add to history
        
        Returns:
            bool: Success status
        """
        if append_to_history(self.username, song):
            print(f"✅ '{song['song_name']}' added to your listening history!")
            # Reload history to reflect changes
            self.history = load_playlist_history()
            return True
        return False
    
    
    def save_playlist(self, filename=None):
        """
        Save current playlist to a CSV file
        
        Args:
            filename (str, optional): Output filename
        
        Returns:
            bool: Success status
        """
        if not self.songs_list:
            print("❌ No songs in playlist to save!")
            return False
        
        if not filename:
            filename = f"playlist_{self.username}_{self.mood.lower()}.csv"
        
        if save_playlist_to_csv(self.username, self.songs_list, filename):
            print(f"💾 Your playlist has been saved successfully!")
            return True
        return False
    
    
    def add_song_to_playlist(self, song):
        """
        Add a single song to the current playlist
        
        Args:
            song (dict): Song to add
        """
        if song not in self.songs_list:
            self.songs_list.append(song)
            print(f"✅ '{song['song_name']}' added to your playlist!")
        else:
            print(f"⚠️  '{song['song_name']}' is already in your playlist!")
    
    
    def remove_song_from_playlist(self, song_name):
        """
        Remove a song from the current playlist
        
        Args:
            song_name (str): Name of song to remove
        """
        original_length = len(self.songs_list)
        self.songs_list = [s for s in self.songs_list if s['song_name'].lower() != song_name.lower()]
        
        if len(self.songs_list) < original_length:
            print(f"✅ '{song_name}' removed from playlist!")
        else:
            print(f"❌ '{song_name}' not found in playlist!")
    
    
    def clear_playlist(self):
        """
        Clear all songs from the current playlist
        """
        self.songs_list = []
        print("🗑️  Playlist cleared!")
    
    
    def show_current_playlist(self):
        """
        Display all songs in the current playlist
        """
        if self.songs_list:
            display_songs_table(self.songs_list, f"{self.username}'s Playlist")
        else:
            print("\n📭 Your playlist is empty! Add some songs first.\n")
    
    
    def get_playlist_statistics(self):
        """
        Display statistics about the current playlist
        """
        if not self.songs_list:
            print("\n❌ No songs in playlist to analyze!\n")
            return
        
        print("\n" + "=" * 60)
        print("📊  PLAYLIST STATISTICS")
        print("=" * 60)
        
        # Total songs
        print(f"Total Songs: {len(self.songs_list)}")
        
        # Average popularity
        avg_pop = sum([s['popularity'] for s in self.songs_list]) / len(self.songs_list)
        print(f"Average Popularity: {avg_pop:.2f}/100")
        
        # Genre breakdown
        genres = Counter([s['genre'] for s in self.songs_list])
        print(f"\nGenre Breakdown:")
        for genre, count in genres.most_common():
            percentage = (count / len(self.songs_list)) * 100
            print(f"  {genre}: {count} songs ({percentage:.1f}%)")
        
        # Mood breakdown
        moods = Counter([s['mood'] for s in self.songs_list])
        print(f"\nMood Breakdown:")
        for mood, count in moods.most_common():
            percentage = (count / len(self.songs_list)) * 100
            print(f"  {mood}: {count} songs ({percentage:.1f}%)")
        
        # Top 5 most popular songs in playlist
        top_songs = sort_by_popularity(self.songs_list)[:5]
        print(f"\nTop 5 Most Popular Songs:")
        for idx, song in enumerate(top_songs, 1):
            print(f"  {idx}. {song['song_name']} - {song['artist']} ({song['popularity']}/100)")
        
        print("=" * 60 + "\n")
    
    
    def search_songs(self, keyword):
        """
        Search for songs by keyword in song name or artist
        
        Args:
            keyword (str): Search keyword
        
        Returns:
            list: Matching songs
        """
        keyword = keyword.lower()
        
        # Use list comprehension to search
        results = [song for song in self.all_songs 
                  if keyword in song['song_name'].lower() 
                  or keyword in song['artist'].lower()]
        
        if results:
            print(f"\n🔍 Found {len(results)} songs matching '{keyword}':")
            display_songs_table(results, f"Search Results for '{keyword}'")
        else:
            print(f"\n❌ No songs found matching '{keyword}'")
        
        return results
