# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (Spotify, YouTube) blend content-based filtering (matching an item's own attributes) with collaborative filtering (patterns from other users). This simulation has no other users, so it prioritizes content-based: it matches a song's own features directly against one listener's stated preferences, weighting genre and mood highest since they're the clearest signals in a small catalog.

**`Song` features used:** `genre`, `mood` (exact match), `energy` (distance to target), `acousticness` (checked against `likes_acoustic`).

**`UserProfile` stores:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

### Algorithm Recipe

Each song is scored against the user's profile and the highest-scoring songs are returned.

| Signal | Rule | Points |
|---|---|---|
| Genre | Exact match: `song.genre == user.favorite_genre` | **+2.0** |
| Mood | Exact match: `song.mood == user.favorite_mood` | **+1.0** |
| Energy | Similarity to target, not exact match | **up to +2.0** |
| Acousticness | Checked against `likes_acoustic` | **±0.5** |

```
genre_score    = 2.0 if song.genre == user.favorite_genre else 0.0
mood_score     = 1.0 if song.mood  == user.favorite_mood  else 0.0
energy_score   = 2.0 * (1 - abs(song.energy - user.target_energy))

if user.likes_acoustic and song.acousticness >= 0.6:
    acoustic_score = +0.5
elif not user.likes_acoustic and song.acousticness <= 0.3:
    acoustic_score = +0.5
elif user.likes_acoustic and song.acousticness <= 0.3:
    acoustic_score = -0.5
elif not user.likes_acoustic and song.acousticness >= 0.7:
    acoustic_score = -0.5
else:
    acoustic_score = 0.0

total_score = genre_score + mood_score + energy_score + acoustic_score
```

Genre outweighs mood 2:1 because genre is a stable, category-level preference, while mood is more situational. Energy gets 2.0 max weight but decays with distance from the target. Acousticness is treated as a soft nudge (±0.5) rather than a deciding factor, since it's a secondary preference.

**Expected biases:** This system might over-prioritize genre and energy closeness, which means it can bury a song that's a near-perfect mood match but the "wrong" genre — even if that song is what the user actually wants to hear in the moment.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

User profile: `favorite_genre="indie pop"`, `favorite_mood="happy"`, `target_energy=0.75`, `likes_acoustic=False`

```
Loaded songs: 18

========================================
Top Recommendations
========================================

1. Rooftop Lights — Indigo Parade (4.98 pts)
   - genre match (+2.0)
   - mood match (+1.0)
   - energy similarity (+2.0)

2. Sunrise City — Neon Echo (3.36 pts)
   - mood match (+1.0)
   - energy similarity (+1.9)
   - acoustic match (+0.5)

3. Night Drive Loop — Neon Echo (2.50 pts)
   - energy similarity (+2.0)
   - acoustic match (+0.5)

4. Concrete Anthem — Trace Bars (2.36 pts)
   - energy similarity (+1.9)
   - acoustic match (+0.5)

5. Neon Pulse Rave — Kilowatt (2.22 pts)
   - energy similarity (+1.7)
   - acoustic match (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



