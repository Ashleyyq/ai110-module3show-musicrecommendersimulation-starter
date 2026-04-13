"""
Command line runner for the Music Recommender Simulation.

Run all profiles at once:
    python -m src.main

Switch to a single profile by setting RUN_ALL = False and picking one profile.
"""

from src.recommender import load_songs, recommend_songs

# Set to False to run only ACTIVE_PROFILE instead of all profiles
RUN_ALL = True


def print_profile_results(label: str, note: str, user_prefs: dict, songs: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"  {note}")
    print(f"{'=' * 60}")
    print(f"  genre={user_prefs['favorite_genre']} | mood={user_prefs['favorite_mood']} | "
          f"energy={user_prefs['target_energy']} | "
          f"acoustic={'yes' if user_prefs['likes_acoustic'] else 'no'}")
    print(f"{'-' * 60}")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.2f} / 9.0")
        print(f"       Why:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # ----------------------------------------------------------------
    # Standard profiles — predictable, well-matched preferences
    # ----------------------------------------------------------------

    rock_fan = {
        "favorite_genre":  "rock",
        "favorite_mood":   "intense",
        "target_energy":   0.88,
        "likes_acoustic":  False,
    }

    lofi_listener = {
        "favorite_genre":  "lofi",
        "favorite_mood":   "chill",
        "target_energy":   0.38,
        "likes_acoustic":  True,
    }

    pop_dancer = {
        "favorite_genre":  "pop",
        "favorite_mood":   "happy",
        "target_energy":   0.85,
        "likes_acoustic":  False,
    }

    # ----------------------------------------------------------------
    # Adversarial profiles — designed to expose edge cases
    # ----------------------------------------------------------------

    # D: Conflicting energy + mood. High energy (0.90) says "intense",
    #    but mood "sad" infers valence target 0.28 (dark/low positivity).
    #    High-energy songs have high valence — does the genre bonus
    #    override the mood mismatch and recommend a euphoric song to a sad user?
    sad_but_energetic = {
        "favorite_genre":  "edm",
        "favorite_mood":   "sad",
        "target_energy":   0.90,
        "likes_acoustic":  False,
    }

    # E: Genre not in catalog. No "country" songs exist, so the +3.0
    #    genre bonus never fires. The entire ranking falls back to
    #    mood match + numeric proximity only.
    genre_ghost = {
        "favorite_genre":  "country",
        "favorite_mood":   "relaxed",
        "target_energy":   0.38,
        "likes_acoustic":  True,
    }

    # F: Contradictory acoustic preference. Rock/intense carries
    #    genre (+3.0) + mood (+2.0), but rock songs score near 0 on
    #    acousticness. Does the categorical ceiling still win?
    acoustic_rocker = {
        "favorite_genre":  "rock",
        "favorite_mood":   "intense",
        "target_energy":   0.90,
        "likes_acoustic":  True,
    }

    # ----------------------------------------------------------------
    # Run profiles
    # ----------------------------------------------------------------

    all_profiles = [
        ("Profile A — High-Energy Rock Fan",   "Standard: well-matched preferences",             rock_fan),
        ("Profile B — Chill Lofi Listener",    "Standard: well-matched preferences",             lofi_listener),
        ("Profile C — Upbeat Pop Dancer",      "Standard: well-matched preferences",             pop_dancer),
        ("Profile D — Sad but Energetic",      "Adversarial: conflicting mood vs energy",        sad_but_energetic),
        ("Profile E — Genre Ghost (Country)",  "Adversarial: genre not present in catalog",      genre_ghost),
        ("Profile F — Acoustic Rocker",        "Adversarial: acoustic preference vs rock genre", acoustic_rocker),
    ]

    # Active profile used when RUN_ALL = False
    ACTIVE_PROFILE = all_profiles[2]  # default: pop_dancer

    if RUN_ALL:
        for label, note, prefs in all_profiles:
            print_profile_results(label, note, prefs, songs)
    else:
        label, note, prefs = ACTIVE_PROFILE
        print_profile_results(label, note, prefs, songs)


if __name__ == "__main__":
    main()
