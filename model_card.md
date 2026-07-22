# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**

---

## 2. Intended Use  

MoodMatch takes a simple taste profile and picks the top 5 songs from a small catalog that best match it.

You tell it your favorite genre, favorite mood, a target energy level (0 to 1), and whether you like acoustic songs. It scores every song in the catalog and returns the highest-scoring ones, with a short list of reasons for each pick.

It assumes the user knows their own taste well enough to fill in those four fields, and that they'll type genre/mood exactly as it appears in the catalog (it does not fix typos or capitalization).

This is a classroom project for learning how a scoring-based recommender works. It's not built for real users — the catalog is only 18 songs, and the code has known bugs (see Limitations and Bias) that would need fixing before any real use.

---

## 3. How the Model Works  

Every song gets a score, and the 5 highest-scoring songs win.

The score is built from four pieces:

- **Genre match**: if the song's genre is exactly your favorite genre, it earns 1 point. Otherwise, 0.
- **Mood match**: same idea — exact match on mood earns 1 point.
- **Energy similarity**: the closer the song's energy is to your target energy, the more points it earns, up to 4 points for a perfect match. This is worth the most of any single factor.
- **Acoustic fit**: if you say you like acoustic songs and the song is acoustic (or you say you don't and it isn't), it gets a small +0.5 bonus. Getting it backwards costs -0.5.

All four pieces are added together for a total score, and the app shows the reasons behind each recommendation so you can see why a song was picked.

The starter code only had placeholders (`# TODO`) for all of this — I wrote the actual scoring rules, then later doubled the energy weight (from up to 2 points to up to 4) and halved the genre weight (from 2 points to 1) to see how it changed the results.

---

## 4. Data  

The catalog has 18 songs, each with a title, artist, genre, mood, energy (0-1), tempo, valence, danceability, and acousticness (0-1).

There are 15 different genres across those 18 songs (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, folk, metal, r&b, country, house, reggae). Only "lofi" and "pop" have more than one song — every other genre has exactly one representative track. Moods are just as spread out (happy, chill, intense, moody, relaxed, focused, confident, melancholic, nostalgic, angry, romantic, playful, euphoric, carefree).

I used the starter catalog as-is and didn't add or remove any songs.

Because most genres only have one song, the dataset can't really show what "similar genre" recommendations would look like — it's too small and too spread out for that. It also skews toward mid-to-high energy tracks, so it's thin on very calm, low-energy music outside of a few lofi/classical/ambient tracks.

---

## 5. Strengths  

For a normal, well-formed profile, MoodMatch does what you'd expect. A pop/happy fan with a mid-high energy target got "Sunrise City" as the #1 pick — a song that's genuinely pop, happy, and close to that energy level. That matched my intuition.

The scoring also correctly rewards songs that hit multiple criteria at once. A song that matches genre, mood, and energy all together clearly outscores one that only matches on one or two, which is the right behavior for a taste-based recommender.

The explanation output (the +1.0 / +4.0 reason list) is a real strength — it makes it easy to see exactly why a song was recommended, which helped a lot when I was debugging weird results during testing.

---

## 6. Limitations and Bias 

The energy-weighting experiment revealed a filter-bubble effect: after doubling the energy weight (4.0) and halving the genre weight (1.0), four users with entirely different favorite genres — hip-hop, house, metal, and r&b — all set to `target_energy=0.8` ended up sharing 4 of their top 5 recommendations (`Sunrise City`, `Night Drive Loop`, `Neon Pulse Rave`, `Storm Runner`), with only the #1 slot reflecting their actual genre. This happens because energy similarity can swing a song's score by up to 4.0 points while a genre match is worth only 1.0, so once several songs cluster near the requested energy value, they crowd out genre diversity almost entirely. The bias is worsened by the catalog itself: 13 of the 15 genres have exactly one representative song, so there's no way for the system to fall back on a "similar genre" when the exact match is weak, and it defaults to energy/acoustic proximity instead. The practical effect is that users who set similar energy targets get pushed toward the same narrow set of "safe" mid-to-high-energy tracks regardless of their stated taste, which is the opposite of what a good recommender should do.

---

## 7. Evaluation  

I tested a normal fan, four fans with different genres but the same energy target, a fan whose genre/mood contradicts their energy request, mismatched capitalization, a genre/mood not in the collection, blank fields, and impossible energy values. The biggest surprise: energy overpowered everything else, and a capital letter was enough to erase a genre/mood match.

### Plain-Language Comparisons (Profile Pairs)

- **"pop"/"happy" vs. "Pop"/"Happy":** Same top pick either way, but capitalizing it makes the system act like the person never stated a genre or mood.
- **Energy request of 1.5 vs. -0.5:** Asking above the max pulls in an unrelated high-energy metal song; asking below the min pulls in unrelated low-energy acoustic songs. The math always finds a "closest" song even when the number itself is nonsense.
- **Blank genre/mood vs. a made-up genre/mood ("opera"/"ecstatic"):** Identical results. Makes sense mechanically (both fail the same exact-match check), but a blank field probably means "no preference," while a real-but-absent genre means "I have one, you just don't have it" — the system treats them the same.
- **Same listener, original weights vs. doubled-energy/halved-genre weights:** Same winner, but the runner-up nearly caught up (lead shrank from ~1.6 points to under 1). Makes sense — energy now counts 4x more, so an energy-close song can compete better against a genre-perfect one.
- **Conflicting classical/high-energy listener, original weights vs. new weights:** Under the old weights the classical pick won by a wide margin; under the new weights a high-energy rock song nearly overtook it. Makes sense — a badly-missed energy target now costs a lot more, even with a perfect genre/mood match.

### Adversarial / Edge Case Profiles

*Note: the technical outputs below were captured under the original weights (genre +2.0, energy up to +2.0), before the weight-shift experiment. See the pairs above for how these same conflicts play out under the current weights (genre +1.0, energy up to +4.0).*

To stress-test `score_song` beyond the happy path, I ran a set of profiles designed to create internal conflicts or feed it invalid/unexpected input, then inspected the actual scored output for each.

**Conflicting energy vs. genre/mood** — `favorite_genre="classical"`, `favorite_mood="melancholic"`, `target_energy=0.9` (classical/melancholic songs in this catalog run low-energy, so this pits genre+mood against energy):

```
$ python -m src.main   # Conflicting energy vs. genre/mood
User profile: {'favorite_genre': 'classical', 'favorite_mood': 'melancholic', 'target_energy': 0.9, 'likes_acoustic': True}

========================================
Top Recommendations
========================================
1. Autumn Sonata — Wren Ellis (4.26 pts)
   - genre match (+2.0)
   - mood match (+1.0)
   - energy similarity (+0.8)
   - acoustic match (+0.5)
2. Rooftop Lights — Indigo Parade (1.72 pts)
   - energy similarity (+1.7)
3. Midnight Coding — LoRoom (1.54 pts)
   - energy similarity (+1.0)
   - acoustic match (+0.5)
```

*Surprise:* Autumn Sonata wins by a wide margin despite missing the requested energy by 0.62 — genre (+2.0) and mood (+1.0) together outweigh a badly missed energy target. This tells me genre/mood dominate the ranking whenever they hit, regardless of how far off energy is.

**Genre match fighting the acoustic preference** — `favorite_genre="metal"`, `likes_acoustic=True` (metal in this catalog is the least acoustic genre, so a genre match forces an acoustic mismatch):

```
$ python -m src.main   # Genre match fighting acoustic preference
User profile: {'favorite_genre': 'metal', 'favorite_mood': 'angry', 'target_energy': 0.9, 'likes_acoustic': True}

========================================
Top Recommendations
========================================
1. Iron Collapse — Grave Circuit (4.36 pts)
   - genre match (+2.0)
   - mood match (+1.0)
   - energy similarity (+1.9)
   - acoustic mismatch (-0.5)
2. Rooftop Lights — Indigo Parade (1.72 pts)
   - energy similarity (+1.7)
3. Midnight Coding — LoRoom (1.54 pts)
   - energy similarity (+1.0)
   - acoustic match (+0.5)
```

*Surprise:* the acoustic mismatch penalty (-0.5) is too small to matter once genre/mood/energy stack up — `likes_acoustic` is effectively decorative whenever the favorite genre happens to match.

**Genre/mood not in the catalog** — `favorite_genre="opera"`, `favorite_mood="ecstatic"` (neither value exists in any row):

```
$ python -m src.main   # Genre/mood not in catalog
User profile: {'favorite_genre': 'opera', 'favorite_mood': 'ecstatic', 'target_energy': 0.5, 'likes_acoustic': False}

========================================
Top Recommendations
========================================
1. Concrete Anthem — Trace Bars (2.14 pts)
   - energy similarity (+1.6)
   - acoustic match (+0.5)
2. Night Drive Loop — Neon Echo (2.00 pts)
   - energy similarity (+1.5)
   - acoustic match (+0.5)
3. Island Drift — Sunny Tide (1.98 pts)
   - energy similarity (+2.0)
```

*Surprise:* nothing crashes or warns — the recommender silently degrades into a pure energy/acoustic matcher with no signal that the user's stated genre/mood were never honored.

**Case sensitivity** — `favorite_genre="Pop"`, `favorite_mood="Happy"` (capitalized, even though "Sunrise City" is literally `pop`/`happy` in the CSV):

```
$ python -m src.main   # Case sensitivity ("Pop"/"Happy")
User profile: {'favorite_genre': 'Pop', 'favorite_mood': 'Happy', 'target_energy': 0.8, 'likes_acoustic': False}

========================================
Top Recommendations
========================================
1. Sunrise City — Neon Echo (2.46 pts)
   - energy similarity (+2.0)
   - acoustic match (+0.5)
2. Night Drive Loop — Neon Echo (2.40 pts)
   - energy similarity (+1.9)
   - acoustic match (+0.5)
3. Neon Pulse Rave — Kilowatt (2.32 pts)
   - energy similarity (+1.8)
   - acoustic match (+0.5)
```

*Surprise:* Sunrise City still lands on top on energy/acoustic alone, but it gets **zero** genre/mood credit it should clearly receive — exact string matching with no normalization is a real bug, not just a modeling choice.

**Out-of-range `target_energy` (no input validation)** — songs' `energy` is always in `[0, 1]`, but nothing stops a caller from passing a value outside that range:

```
$ python -m src.main   # Out-of-range target_energy = 1.5
User profile: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 1.5, 'likes_acoustic': False}

========================================
Top Recommendations
========================================
1. Sunrise City — Neon Echo (4.14 pts)
   - genre match (+2.0)
   - mood match (+1.0)
   - energy similarity (+0.6)
   - acoustic match (+0.5)
2. Gym Hero — Max Pulse (3.36 pts)
   - genre match (+2.0)
   - energy similarity (+0.9)
   - acoustic match (+0.5)
3. Rooftop Lights — Indigo Parade (1.52 pts)
   - mood match (+1.0)
   - energy similarity (+0.5)

$ python -m src.main   # Out-of-range target_energy = -0.5
User profile: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': -0.5, 'likes_acoustic': False}

========================================
Top Recommendations
========================================
1. Sunrise City — Neon Echo (2.86 pts)
   - genre match (+2.0)
   - mood match (+1.0)
   - energy similarity (-0.6)
   - acoustic match (+0.5)
2. Gym Hero — Max Pulse (1.64 pts)
   - genre match (+2.0)
   - energy similarity (-0.9)
   - acoustic match (+0.5)
3. Rooftop Lights — Indigo Parade (0.48 pts)
   - mood match (+1.0)
   - energy similarity (-0.5)
```

*Surprise:* `energy_score` happily goes negative and the ranking quietly reshuffles (Sunrise City vs. Gym Hero swap relative order between the two runs) — there's no bounds check, so a bad upstream value (e.g. a slider bug sending `1.5`) degrades results without any error.

**Empty-string preferences** — `favorite_genre=""`, `favorite_mood=""` (e.g. a form field the user left blank):

```
$ python -m src.main   # Empty-string "no preference"
User profile: {'favorite_genre': '', 'favorite_mood': '', 'target_energy': 0.5, 'likes_acoustic': False}

========================================
Top Recommendations
========================================
1. Concrete Anthem — Trace Bars (2.14 pts)
   - energy similarity (+1.6)
   - acoustic match (+0.5)
2. Night Drive Loop — Neon Echo (2.00 pts)
   - energy similarity (+1.5)
   - acoustic match (+0.5)
3. Island Drift — Sunny Tide (1.98 pts)
   - energy similarity (+2.0)
```

*Surprise:* identical behavior to the "not in catalog" case above — an empty string is treated as just another genre/mood that never matches, rather than as "no preference, don't penalize." Whether that's the right behavior depends on product intent, but it's currently an accident of the implementation, not a decision.

**Crash cases (not just bad scores — the code raises)** — a non-numeric `target_energy`, or a profile missing the field entirely, both blow up instead of failing gracefully:

```
>>> recommend_songs({'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 'high', 'likes_acoustic': False}, songs)
TypeError: unsupported operand type(s) for -: 'float' and 'str'

>>> recommend_songs({'favorite_genre': 'pop', 'favorite_mood': 'happy', 'likes_acoustic': False}, songs)
KeyError: 'target_energy'
```

*Takeaway:* `score_song` does no input validation at all, so any malformed profile (e.g. from a form that allows a blank field) takes down the entire recommendation call rather than returning a degraded-but-usable result.

---

## 8. Future Work  

1. **Normalize genre/mood input.** Lowercase and trim both the catalog and the user's input before comparing, so "Pop" and "pop" count as the same thing. This fixes a real bug, not just a nice-to-have.

2. **Add input validation.** Reject or clamp a `target_energy` outside `[0, 1]`, and give a clear error (instead of a crash) when a required field like `target_energy` is missing.

3. **Improve diversity in the top 5.** Right now, once energy dominates the score, the top results can all cluster around the same energy level and feel repetitive. I'd add a rule that caps how many songs from the same artist or how similar the energy values can be among the top 5, so recommendations feel less like the same song five times.

---

## 9. Personal Reflection  

Building this showed me how much a recommender's "personality" comes down to a few weight numbers. Doubling the energy weight and halving the genre weight completely changed which users got treated as similar to each other, even though I didn't touch the underlying data at all.

The most surprising thing was how fragile exact-match logic is. A single capital letter ("Pop" vs "pop") was enough to make the system act like I had no genre preference at all, even when a perfect match existed in the catalog. That's a bug I never would have noticed without deliberately testing weird inputs.

This changed how I think about recommendation apps I use every day — a "for you" list isn't some deep understanding of my taste, it's just a formula with weights someone chose, and small choices in that formula (or small bugs) can quietly push very different users toward the same results.
