"""
Music Playlist Recommendation System
ITM Skills University - Case Study 148

Main Application Module
Author: Expert Python Developer
Date: December 2024

This application provides mood-based and genre-based music recommendations
using CSV data, OOP design, lambda functions, decorators, and visualizations.
"""

import sys
from playlist_class import Playlist
from music_utils import (
    load_songs_from_csv,
    visualize_genre_preferences,
    visualize_mood_distribution,
    visualize_both,
    display_songs_table,
    get_top_songs,
    filter_by_genre,
    filter_by_mood
)


def print_banner():
    """Display application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🎵  MUSIC PLAYLIST RECOMMENDATION SYSTEM  🎵          ║
    ║                                                               ║
    ║              ITM Skills University - Case Study 148           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Display main menu options"""
    menu = """
    ┌───────────────────────────────────────────────────────────┐
    │                      MAIN MENU                            │
    ├───────────────────────────────────────────────────────────┤
    │  1.  View User Profile                                    │
    │  2.  Get Mood-Based Recommendations                       │
    │  3.  Get Genre-Based Recommendations                      │
    │  4.  Get Recommendations (Genre + Mood)                   │
    │  5.  Smart Recommendations (Based on History)             │
    │  6.  Search Songs                                         │
    │  7.  View Current Playlist                                │
    │  8.  Add Song to Playlist                                 │
    │  9.  Remove Song from Playlist                            │
    │  10. Track Song in History                                │
    │  11. Save Playlist to CSV                                 │
    │  12. View Playlist Statistics                             │
    │  13. Visualize Genre Distribution (Bar Chart)             │
    │  14. Visualize Mood Distribution (Pie Chart)              │
    │  15. Visualize Complete Analysis (Both Charts)            │
    │  16. Browse All Available Songs                           │
    │  17. View Top Popular Songs                               │
    │  18. Clear Current Playlist                               │
    │  0.  Exit Application                                     │
    └───────────────────────────────────────────────────────────┘
    """
    print(menu)


def get_user_input(prompt, input_type=str, required=True):
    """
    Get and validate user input
    
    Args:
        prompt (str): Input prompt message
        input_type (type): Expected type (str, int, etc.)
        required (bool): Whether input is required
    
    Returns:
        User input of specified type
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and not required:
                return None
            
            if not user_input and required:
                print("❌ This field is required. Please enter a value.")
                continue
            
            if input_type == int:
                return int(user_input)
            else:
                return user_input
                
        except ValueError:
            print(f"❌ Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\n\n👋 Exiting application...")
            sys.exit(0)


def get_mood_choice():
    """Get mood choice from user with validation"""
    print("\n📋 Available Moods:")
    moods = ["Happy", "Sad", "Energetic", "Calm", "Romantic"]
    for idx, mood in enumerate(moods, 1):
        print(f"   {idx}. {mood}")
    
    while True:
        choice = get_user_input("\nSelect mood (1-5) or type custom mood: ", str)
        
        if choice.isdigit() and 1 <= int(choice) <= 5:
            return moods[int(choice) - 1]
        elif choice.isalpha():
            return choice.capitalize()
        else:
            print("❌ Invalid choice. Please try again.")


def get_genre_choice():
    """Get genre choice from user with validation"""
    print("\n📋 Available Genres:")
    genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz", "Classical"]
    for idx, genre in enumerate(genres, 1):
        print(f"   {idx}. {genre}")
    
    while True:
        choice = get_user_input("\nSelect genre (1-6) or type custom genre: ", str)
        
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return genres[int(choice) - 1]
        elif choice.replace('-', '').isalpha():
            return choice.title()
        else:
            print("❌ Invalid choice. Please try again.")


def select_song_from_list(songs):
    """
    Helper function to select a song from a list
    
    Args:
        songs (list): List of songs
    
    Returns:
        dict: Selected song or None
    """
    if not songs:
        return None
    
    while True:
        try:
            choice = get_user_input("\nEnter song number (or 0 to cancel): ", int)
            if choice == 0:
                return None
            if 1 <= choice <= len(songs):
                return songs[choice - 1]
            else:
                print(f"❌ Please enter a number between 1 and {len(songs)}")
        except:
            print("❌ Invalid input!")


def main():
    """Main application function"""
    
    # Display banner
    print_banner()
    
    # Load songs database
    print("🔄 Loading songs database...")
    all_songs = load_songs_from_csv('songs.csv')
    
    if not all_songs:
        print("❌ Error: Could not load songs database. Please ensure songs.csv exists.")
        sys.exit(1)
    
    # Get user information
    print("\n" + "=" * 60)
    print("👤  USER SETUP")
    print("=" * 60)
    
    username = get_user_input("Enter your username: ", str)
    print(f"\nHello, {username}! 👋")
    
    mood = get_mood_choice()
    
    # Create Playlist object
    playlist = Playlist(username, mood, all_songs)
    
    print(f"\n✅ Welcome to your personalized music recommendation system!")
    print(f"   Your current mood: {mood}")
    
    # Main application loop
    while True:
        print_menu()
        
        choice = get_user_input("Enter your choice (0-18): ", str)
        
        try:
            if choice == '1':
                # View User Profile
                playlist.user_profile()
            
            elif choice == '2':
                # Mood-Based Recommendations
                print("\n🎭 Mood-Based Recommendations")
                mood_choice = get_mood_choice()
                count = get_user_input("How many songs to recommend? (default: 10): ", int, required=False) or 10
                playlist.recommend_songs(mood=mood_choice, count=count)
            
            elif choice == '3':
                # Genre-Based Recommendations
                print("\n🎸 Genre-Based Recommendations")
                genre_choice = get_genre_choice()
                count = get_user_input("How many songs to recommend? (default: 10): ", int, required=False) or 10
                playlist.recommend_songs(genre=genre_choice, count=count)
            
            elif choice == '4':
                # Genre + Mood Recommendations
                print("\n🎯 Genre + Mood Based Recommendations")
                genre_choice = get_genre_choice()
                mood_choice = get_mood_choice()
                count = get_user_input("How many songs to recommend? (default: 10): ", int, required=False) or 10
                playlist.recommend_songs(genre=genre_choice, mood=mood_choice, count=count)
            
            elif choice == '5':
                # Smart Recommendations based on history
                print("\n🤖 Smart Recommendations (Based on Your History)")
                count = get_user_input("How many songs to recommend? (default: 10): ", int, required=False) or 10
                playlist.recommend_songs(count=count)
            
            elif choice == '6':
                # Search Songs
                keyword = get_user_input("Enter search keyword (song name or artist): ", str)
                results = playlist.search_songs(keyword)
                
                if results:
                    add_choice = get_user_input("\nAdd a song to playlist? (y/n): ", str)
                    if add_choice.lower() == 'y':
                        song = select_song_from_list(results)
                        if song:
                            playlist.add_song_to_playlist(song)
            
            elif choice == '7':
                # View Current Playlist
                playlist.show_current_playlist()
            
            elif choice == '8':
                # Add Song to Playlist
                print("\n➕ Add Song to Playlist")
                keyword = get_user_input("Search for a song (name or artist): ", str)
                results = playlist.search_songs(keyword)
                
                if results:
                    song = select_song_from_list(results)
                    if song:
                        playlist.add_song_to_playlist(song)
            
            elif choice == '9':
                # Remove Song from Playlist
                playlist.show_current_playlist()
                if playlist.songs_list:
                    song_name = get_user_input("Enter song name to remove: ", str)
                    playlist.remove_song_from_playlist(song_name)
            
            elif choice == '10':
                # Track Song in History
                print("\n📝 Track Song in History")
                keyword = get_user_input("Search for a song to track: ", str)
                results = playlist.search_songs(keyword)
                
                if results:
                    song = select_song_from_list(results)
                    if song:
                        playlist.track_history(song)
            
            elif choice == '11':
                # Save Playlist
                if playlist.songs_list:
                    custom_name = get_user_input("Enter filename (or press Enter for auto-name): ", str, required=False)
                    if custom_name and not custom_name.endswith('.csv'):
                        custom_name += '.csv'
                    playlist.save_playlist(custom_name)
                else:
                    print("\n❌ Your playlist is empty! Add some songs first.\n")
            
            elif choice == '12':
                # View Statistics
                playlist.get_playlist_statistics()
            
            elif choice == '13':
                # Visualize Genre Distribution
                if playlist.songs_list:
                    visualize_genre_preferences(playlist.songs_list)
                else:
                    print("\n❌ Your playlist is empty! Add some songs first.\n")
            
            elif choice == '14':
                # Visualize Mood Distribution
                if playlist.songs_list:
                    visualize_mood_distribution(playlist.songs_list)
                else:
                    print("\n❌ Your playlist is empty! Add some songs first.\n")
            
            elif choice == '15':
                # Visualize Both
                if playlist.songs_list:
                    visualize_both(playlist.songs_list)
                else:
                    print("\n❌ Your playlist is empty! Add some songs first.\n")
            
            elif choice == '16':
                # Browse All Songs
                display_songs_table(all_songs, "All Available Songs")
                
                add_choice = get_user_input("Add a song to playlist? (y/n): ", str)
                if add_choice.lower() == 'y':
                    song = select_song_from_list(all_songs)
                    if song:
                        playlist.add_song_to_playlist(song)
            
            elif choice == '17':
                # View Top Popular Songs
                count = get_user_input("How many top songs to display? (default: 10): ", int, required=False) or 10
                top_songs = get_top_songs(all_songs, count)
                display_songs_table(top_songs, f"Top {count} Most Popular Songs")
                
                add_choice = get_user_input("Add a song to playlist? (y/n): ", str)
                if add_choice.lower() == 'y':
                    song = select_song_from_list(top_songs)
                    if song:
                        playlist.add_song_to_playlist(song)
            
            elif choice == '18':
                # Clear Playlist
                confirm = get_user_input("Are you sure you want to clear your playlist? (y/n): ", str)
                if confirm.lower() == 'y':
                    playlist.clear_playlist()
            
            elif choice == '0':
                # Exit
                print("\n" + "=" * 60)
                print("👋 Thank you for using Music Recommendation System!")
                print("   Have a great day! 🎵")
                print("=" * 60 + "\n")
                sys.exit(0)
            
            else:
                print("\n❌ Invalid choice. Please select a valid option (0-18).\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting application...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")
            print("Please try again or contact support if the issue persists.\n")


if __name__ == "__main__":
    main()
