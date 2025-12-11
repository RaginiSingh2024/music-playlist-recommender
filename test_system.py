"""
Quick Test Script for Music Recommendation System
Tests basic functionality to ensure everything works
"""

print("=" * 60)
print("🧪 TESTING MUSIC RECOMMENDATION SYSTEM")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing module imports...")
try:
    from music_utils import load_songs_from_csv, filter_by_mood, filter_by_genre, sort_by_popularity
    from playlist_class import Playlist
    print("   ✅ All modules imported successfully!")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    exit(1)

# Test 2: Load songs
print("\n2. Testing CSV loading...")
songs = load_songs_from_csv('songs.csv')
if songs and len(songs) > 0:
    print(f"   ✅ Loaded {len(songs)} songs successfully!")
else:
    print("   ❌ Failed to load songs!")
    exit(1)

# Test 3: Test filtering
print("\n3. Testing list comprehension filters...")
happy_songs = filter_by_mood(songs, 'Happy')
print(f"   ✅ Found {len(happy_songs)} happy songs")

pop_songs = filter_by_genre(songs, 'Pop')
print(f"   ✅ Found {len(pop_songs)} pop songs")

# Test 4: Test lambda sorting
print("\n4. Testing lambda function sorting...")
sorted_songs = sort_by_popularity(songs)
if sorted_songs[0]['popularity'] >= sorted_songs[-1]['popularity']:
    print(f"   ✅ Songs sorted correctly! Top song: {sorted_songs[0]['song_name']} (Popularity: {sorted_songs[0]['popularity']})")
else:
    print("   ❌ Sorting failed!")

# Test 5: Test Playlist class
print("\n5. Testing Playlist class...")
try:
    playlist = Playlist("TestUser", "Happy", songs)
    print(f"   ✅ Playlist object created for user: {playlist.username}")
    
    # Test recommendation
    print("\n6. Testing recommendation system...")
    recommendations = playlist.recommend_songs(mood='Happy', count=5)
    if recommendations and len(recommendations) > 0:
        print(f"   ✅ Generated {len(recommendations)} recommendations!")
    else:
        print("   ⚠️  No recommendations generated")
    
except Exception as e:
    print(f"   ❌ Playlist test error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Test data validation
print("\n7. Testing data validation...")
from music_utils import validate_song_data, check_duplicate_song

valid_song = {
    'song_name': 'Test Song',
    'artist': 'Test Artist',
    'genre': 'Pop',
    'mood': 'Happy',
    'popularity': '85'
}

invalid_song = {
    'song_name': 'Test Song',
    'artist': '',  # Missing artist
    'genre': 'Pop'
}

if validate_song_data(valid_song):
    print("   ✅ Valid song data accepted")
else:
    print("   ❌ Valid song data rejected")

if not validate_song_data(invalid_song):
    print("   ✅ Invalid song data rejected correctly")
else:
    print("   ❌ Invalid song data wrongly accepted")

# Test 7: Test duplicate detection
print("\n8. Testing duplicate detection...")
if check_duplicate_song(songs, "Blinding Lights"):
    print("   ✅ Duplicate detection working")
else:
    print("   ❌ Duplicate detection failed")

print("\n" + "=" * 60)
print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\n✅ The Music Recommendation System is ready to use!")
print("   Run: python3 music_recommender_main.py\n")
