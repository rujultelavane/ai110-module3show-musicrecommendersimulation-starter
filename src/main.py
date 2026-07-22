"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: target values the recommender compares each song against
    user_prefs = {
        "favorite_genre": "indie pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("Top Recommendations")
    print("=" * 40)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']} ({score:.2f} pts)")
        for reason in explanation.split(", "):
            print(f"   - {reason}")
    print()


if __name__ == "__main__":
    main()
