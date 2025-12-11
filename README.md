# 🎵 Music Playlist Recommendation System

**ITM Skills University - Case Study 148**

A complete Python-based music recommendation system featuring mood-based and genre-based song recommendations, CSV data management, OOP design, lambda functions, decorators, and beautiful visualizations.

---

## 📁 Project Structure

```
python/
├── music_recommender_main.py     # Main application with interactive menu
├── playlist_class.py              # Playlist class with OOP design
├── music_utils.py                 # Utility functions, decorators, lambda operations
├── songs.csv                      # Song database (50 songs)
├── playlist_history.csv           # User listening history
└── README.md                      # This file
```

---

## 🎯 Features Implemented

### ✅ Core Requirements

1. **Full Python Code with Modular Structure**
   - Separated into 3 modules: main, class, and utils
   - Clean, well-documented code with comments

2. **Clean OOP Design**
   - `Playlist` class with attributes: username, mood, songs_list
   - Methods: user_profile(), recommend_songs(), track_history(), save_playlist()

3. **CSV Loading/Saving**
   - Load songs from songs.csv
   - Load/save playlist history
   - Save user playlists with custom names

4. **Mood-Based and Genre-Based Recommendations**
   - Filter by mood (Happy, Sad, Energetic, Calm, Romantic)
   - Filter by genre (Pop, Rock, Hip-Hop, etc.)
   - Combined filtering (Genre + Mood)
   - Smart recommendations based on listening history

5. **Popularity Tracking Using Lambda Functions**
   - Sort songs by popularity: `sorted(songs, key=lambda x: x['popularity'])`
   - Get top N songs using lambda

6. **Decorator for Measuring Recommendation Time**
   - `@measure_time` decorator tracks performance
   - Displays execution time for recommendations

7. **List Comprehensions for Filtering**
   - `[song for song in songs if song['genre'].lower() == genre.lower()]`
   - Multiple filtering operations using list comprehensions

8. **Visualization Using Matplotlib**
   - Bar chart for genre distribution
   - Pie chart for mood distribution
   - Combined visualization with both charts

9. **Two CSV Files**
   - `songs.csv`: 50 songs with metadata
   - `playlist_history.csv`: User listening history

10. **Input Handling + Validation**
    - Validates missing fields
    - Checks for duplicate songs
    - Validates data types and formats
    - Error handling throughout

---

## 🚀 How to Run the Project

### Prerequisites

1. **Python 3.7 or higher** installed on your system
2. **Required libraries**: matplotlib

### Installation Steps

1. **Navigate to the project directory**:
   ```bash
   cd /Users/ragini/Desktop/python
   ```

2. **Install required dependencies**:
   ```bash
   pip3 install matplotlib
   ```

3. **Run the application**:
   ```bash
   python3 music_recommender_main.py
   ```

### First Time Setup

When you run the application for the first time:

1. **Enter your username** when prompted
2. **Select your current mood** from the available options
3. The system will create your user profile and load the song database

---

## 📖 How to Use

### Main Menu Options

The application provides 18 different features:

1. **View User Profile** - See your listening statistics and preferences
2. **Mood-Based Recommendations** - Get songs matching a specific mood
3. **Genre-Based Recommendations** - Get songs from a specific genre
4. **Genre + Mood Recommendations** - Combined filtering
5. **Smart Recommendations** - AI-based recommendations from your history
6. **Search Songs** - Search by song name or artist
7. **View Current Playlist** - Display your current playlist
8. **Add Song to Playlist** - Add songs to your playlist
9. **Remove Song** - Remove songs from playlist
10. **Track Song in History** - Add a song to your listening history
11. **Save Playlist to CSV** - Export your playlist
12. **View Statistics** - See detailed playlist analytics
13. **Visualize Genres** - Bar chart of genre distribution
14. **Visualize Moods** - Pie chart of mood distribution
15. **Complete Analysis** - Both charts side by side
16. **Browse All Songs** - View entire song database
17. **Top Popular Songs** - See most popular songs
18. **Clear Playlist** - Clear your current playlist
0. **Exit** - Close the application

### Example Workflow

```
1. Run the application
2. Enter username: "John"
3. Select mood: "Happy"
4. Choose option 3 (Genre-Based Recommendations)
5. Select genre: "Pop"
6. Enter count: 10
7. View the recommendations with popularity scores
8. Choose option 11 to save your playlist
9. Choose option 13 to see genre visualization
10. Choose option 14 to see mood visualization
```

---

## 📊 Sample Data

### Songs Database (songs.csv)

Contains **50 songs** with:
- Song Name
- Artist
- Genre (Pop, Rock, Hip-Hop)
- Mood (Happy, Sad, Energetic, Calm, Romantic)
- Popularity (0-100)

Example entries:
```csv
Blinding Lights,The Weeknd,Pop,Happy,95
Bohemian Rhapsody,Queen,Rock,Energetic,90
Lose Yourself,Eminem,Hip-Hop,Energetic,91
```

### Playlist History (playlist_history.csv)

Contains user listening history:
- Username
- Song Name
- Timestamp
- Genre
- Mood

Example entries:
```csv
john_doe,Blinding Lights,2024-01-15 10:30:00,Pop,Happy
jane_smith,Someone Like You,2024-01-16 14:20:00,Pop,Sad
```

---

## 🔧 Technical Details

### OOP Implementation

**Playlist Class** (`playlist_class.py`):
```python
class Playlist:
    def __init__(self, username, mood, all_songs)
    def user_profile()         # Display user information
    def recommend_songs()      # Generate recommendations (with @measure_time)
    def track_history()        # Track listening history
    def save_playlist()        # Save to CSV
    # ... and more methods
```

### Lambda Functions

```python
# Sort by popularity
sorted_songs = sorted(songs, key=lambda x: x['popularity'], reverse=True)

# Get top N songs
top_songs = sorted(songs, key=lambda x: x['popularity'], reverse=True)[:n]
```

### List Comprehensions

```python
# Filter by genre
[song for song in songs if song['genre'].lower() == genre.lower()]

# Filter by mood
[song for song in songs if song['mood'].lower() == mood.lower()]

# Combined filter
[song for song in songs 
 if song['genre'].lower() == genre.lower() 
 and song['mood'].lower() == mood.lower()]
```

### Decorator

```python
@measure_time
def recommend_songs(self, genre=None, mood=None, count=10):
    # Recommendation logic
    # Decorator automatically measures execution time
```

### Visualization

```python
# Bar Chart - Genre Distribution
plt.bar(genres, counts, color=['#FF6B6B', '#4ECDC4', ...])

# Pie Chart - Mood Distribution
plt.pie(mood_counts, labels=moods, autopct='%1.1f%%', ...)
```

---

## 📝 Code Comments

All code files include:
- **Module docstrings** explaining purpose
- **Function docstrings** with parameters and return values
- **Inline comments** for complex logic
- **Type hints** where applicable

---

## 🎨 Output Examples

### Recommendation Report
```
============================================================
🎵  MUSIC RECOMMENDATION REPORT
============================================================
User: John
Date: 2024-12-11 16:43:49
Criteria: Genre: Pop, Mood: Happy
Total Songs Recommended: 10
============================================================

📊 STATISTICS:
   Average Popularity: 87.50/100
   Genres: {'Pop': 10}
   Moods: {'Happy': 10}

💿 RECOMMENDED SONGS:
------------------------------------------------------------
1. Blinding Lights
   Artist: The Weeknd
   Genre: Pop | Mood: Happy | Popularity: 95/100
...
```

### Visualizations

The system generates:
1. **genre_preferences.png** - Bar chart showing genre distribution
2. **mood_distribution.png** - Pie chart showing mood breakdown
3. **playlist_analysis.png** - Combined visualization

---

## ✨ Key Highlights

✅ **Modular Design**: Separated concerns across 3 files  
✅ **Error Handling**: Comprehensive validation and error messages  
✅ **User-Friendly**: Interactive menu with emoji indicators  
✅ **Data Validation**: Checks for missing fields and duplicates  
✅ **Performance Tracking**: Decorator measures recommendation time  
✅ **Rich Visualizations**: Beautiful matplotlib charts  
✅ **Persistent Storage**: CSV-based data management  
✅ **Smart AI**: History-based recommendation algorithm  

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'matplotlib'
**Solution**: Install matplotlib
```bash
pip3 install matplotlib
```

### Issue: FileNotFoundError for CSV files
**Solution**: Ensure you're running from the correct directory
```bash
cd /Users/ragini/Desktop/python
python3 music_recommender_main.py
```

### Issue: Permission denied
**Solution**: Check file permissions
```bash
chmod +x music_recommender_main.py
```

---

## 📄 Files Description

| File | Description | Lines |
|------|-------------|-------|
| `music_recommender_main.py` | Main application with interactive menu | ~400 |
| `playlist_class.py` | Playlist class with OOP methods | ~350 |
| `music_utils.py` | Utilities, decorators, visualizations | ~400 |
| `songs.csv` | Song database (50 songs) | 51 |
| `playlist_history.csv` | Listening history | 19 |

**Total Code**: ~1150 lines of well-documented Python code

---

## 🎓 Learning Objectives Covered

✅ CSV file handling (reading/writing)  
✅ Object-Oriented Programming (classes, methods, attributes)  
✅ Lambda functions for sorting  
✅ Decorators for cross-cutting concerns  
✅ List comprehensions for filtering  
✅ Data validation and error handling  
✅ Matplotlib visualizations  
✅ Modular code organization  
✅ User input validation  
✅ Algorithm design (recommendation system)  

---

## 👨‍💻 Author

**Expert Python Developer**  
Case Study: ITM Skills University - Case Study 148  
Date: December 2024

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all files are in the correct directory
3. Ensure Python 3.7+ is installed
4. Check that matplotlib is properly installed

---

## 🎉 Enjoy Your Music Recommendations!

Start the application and let the AI recommend great music based on your mood and preferences! 🎵🎧
