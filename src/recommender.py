import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts."""
    print(f"Loading songs from {csv_path}...")
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences, returning (score, reasons)."""
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        genre_score = 1.0
    else: genre_score=0.0
    if genre_score:
        reasons.append(f"genre match (+{genre_score:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        mood_score = 1.0
    else: mood_score = 0.0
    if mood_score:
        reasons.append(f"mood match (+{mood_score:.1f})")

    energy_score = 4.0 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    reasons.append(f"energy similarity ({energy_score:+.1f})")

    likes_acoustic = user_prefs["likes_acoustic"]
    acousticness = song["acousticness"]
    if likes_acoustic and acousticness >= 0.6:
        acoustic_score = 0.5
        reasons.append(f"acoustic match (+{acoustic_score:.1f})")
    elif not likes_acoustic and acousticness <= 0.3:
        acoustic_score = 0.5
        reasons.append(f"acoustic match (+{acoustic_score:.1f})")
    elif likes_acoustic and acousticness <= 0.3:
        acoustic_score = -0.5
        reasons.append(f"acoustic mismatch ({acoustic_score:.1f})")
    elif not likes_acoustic and acousticness >= 0.7:
        acoustic_score = -0.5
        reasons.append(f"acoustic mismatch ({acoustic_score:.1f})")
    else:
        acoustic_score = 0.0

    total_score = genre_score + mood_score + energy_score + acoustic_score
    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
