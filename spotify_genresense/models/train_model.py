import os
import sys
import json
import requests
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

DATASET_URL = "https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/main/dataset.csv"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "dataset.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "genre_model.joblib")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")
SAMPLES_PATH = os.path.join(DATA_DIR, "sample_tracks.json")

# Taxonomy mapping: Group 114 Kaggle subgenres into prominent canonical genre families
GENRE_TAXONOMY = {
    # Electronic & Dance
    "electronic": "Electronic / Synth",
    "electro": "Electronic / Synth",
    "edm": "Electronic / Synth",
    "club": "Electronic / Synth",
    "dance": "Electronic / Synth",
    "dancehall": "Electronic / Synth",
    "deep-house": "Electronic / Synth",
    "house": "Electronic / Synth",
    "techno": "Electronic / Synth",
    "trance": "Electronic / Synth",
    "dubstep": "Electronic / Synth",
    "synth-pop": "Electronic / Synth",
    "detroit-techno": "Electronic / Synth",
    "minimal-techno": "Electronic / Synth",
    "progressive-house": "Electronic / Synth",
    "chicago-house": "Electronic / Synth",
    "hardstyle": "Electronic / Synth",
    "idm": "Electronic / Synth",
    "chill": "Electronic / Synth",

    # Pop
    "pop": "Pop",
    "pop-film": "Pop",
    "power-pop": "Pop",
    "indie-pop": "Pop",
    "k-pop": "Pop",
    "j-pop": "Pop",
    "mandopop": "Pop",
    "cantopop": "Pop",

    # Hip-Hop / Rap
    "hip-hop": "Hip-Hop",
    "trip-hop": "Hip-Hop",

    # Rock / Alternative / Metal
    "rock": "Rock / Alternative",
    "alt-rock": "Rock / Alternative",
    "alternative": "Rock / Alternative",
    "indie": "Rock / Alternative",
    "psych-rock": "Rock / Alternative",
    "punk-rock": "Rock / Alternative",
    "punk": "Rock / Alternative",
    "hard-rock": "Rock / Alternative",
    "metal": "Rock / Alternative",
    "heavy-metal": "Rock / Alternative",
    "black-metal": "Rock / Alternative",
    "death-metal": "Rock / Alternative",
    "metalcore": "Rock / Alternative",
    "grunge": "Rock / Alternative",
    "emo": "Rock / Alternative",
    "goth": "Rock / Alternative",
    "rock-n-roll": "Rock / Alternative",
    "rockabilly": "Rock / Alternative",
    "hardcore": "Rock / Alternative",
    "garage": "Rock / Alternative",

    # Jazz & Soul / Blues
    "jazz": "Jazz / Soul",
    "blues": "Jazz / Soul",
    "soul": "Jazz / Soul",
    "funk": "Jazz / Soul",
    "gospel": "Jazz / Soul",
    "groove": "Jazz / Soul",
    "r-n-b": "Jazz / Soul",

    # Classical & Acoustic Instrumental
    "classical": "Classical / Ambient",
    "opera": "Classical / Ambient",
    "piano": "Classical / Ambient",
    "guitar": "Classical / Ambient",
    "ambient": "Classical / Ambient",
    "new-age": "Classical / Ambient",
    "sleep": "Classical / Ambient",
    "study": "Classical / Ambient",

    # Country & Folk
    "country": "Country / Folk",
    "folk": "Country / Folk",
    "bluegrass": "Country / Folk",
    "honky-tonk": "Country / Folk",
    "singer-songwriter": "Country / Folk",
    "acoustic": "Country / Folk",

    # Latin / World
    "latin": "Latin / World",
    "latino": "Latin / World",
    "salsa": "Latin / World",
    "samba": "Latin / World",
    "tango": "Latin / World",
    "reggaeton": "Latin / World",
    "reggae": "Latin / World",
    "ska": "Latin / World",
    "afrobeat": "Latin / World",
    "brazil": "Latin / World",
    "forro": "Latin / World",
    "mpb": "Latin / World",
    "pagode": "Latin / World",
    "sertanejo": "Latin / World",
    "world-music": "Latin / World",
}

GENRE_ICONS = {
    "Electronic / Synth": "🎧",
    "Pop": "✨",
    "Hip-Hop": "🎤",
    "Rock / Alternative": "🎸",
    "Jazz / Soul": "🎷",
    "Classical / Ambient": "🎻",
    "Country / Folk": "🪕",
    "Latin / World": "🪇",
    "Other / Eclectic": "🎵"
}

FEATURE_COLUMNS = [
    "tempo",
    "danceability",
    "energy",
    "loudness",
    "duration_ms",
    "valence",
    "acousticness",
    "speechiness",
    "instrumentalness"
]

def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 1000000:
        print(f"Dataset already exists at {CSV_PATH} ({os.path.getsize(CSV_PATH)} bytes)")
        return
    
    print(f"Downloading Kaggle Spotify Tracks Dataset from {DATASET_URL}...")
    with requests.get(DATASET_URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        total_length = r.headers.get('content-length')
        dl = 0
        with open(CSV_PATH, 'wb') as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    dl += len(chunk)
                    if total_length:
                        done = int(50 * dl / int(total_length))
                        sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}] {dl // 1024} KB")
                        sys.stdout.flush()
    print("\nDownload complete!")

def train_and_export_model():
    download_dataset()
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Loading dataset into pandas...")
    df = pd.read_csv(CSV_PATH)
    print(f"Total raw tracks: {len(df)}")

    # Clean missing values
    df = df.dropna(subset=FEATURE_COLUMNS + ["track_genre"])

    # Map subgenres to taxonomy
    df["broad_genre"] = df["track_genre"].map(lambda g: GENRE_TAXONOMY.get(str(g).lower(), "Other / Eclectic"))

    # Filter for primary target categories
    target_genres = [
        "Electronic / Synth",
        "Pop",
        "Hip-Hop",
        "Rock / Alternative",
        "Jazz / Soul",
        "Classical / Ambient",
        "Country / Folk",
        "Latin / World"
    ]
    df_filtered = df[df["broad_genre"].isin(target_genres)].copy()
    print(f"Tracks in primary genre taxonomy: {len(df_filtered)}")
    print("Class distribution:\n", df_filtered["broad_genre"].value_counts())

    # Sample balanced dataset for fast, robust training
    balanced_samples = []
    samples_per_class = min(4000, df_filtered["broad_genre"].value_counts().min())
    for genre in target_genres:
        genre_subset = df_filtered[df_filtered["broad_genre"] == genre]
        if len(genre_subset) > samples_per_class:
            balanced_samples.append(genre_subset.sample(n=samples_per_class, random_state=42))
        else:
            balanced_samples.append(genre_subset)
    
    train_df = pd.concat(balanced_samples, ignore_index=True)
    print(f"Balanced training corpus size: {len(train_df)}")

    X = train_df[FEATURE_COLUMNS]
    y = train_df["broad_genre"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Fitting feature scaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Random Forest multi-class model with calibrated probability estimators...")
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=16,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train_scaled, y_train)

    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Validation Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, y_pred))

    # Save model and scaler
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")

    # Feature importance
    feature_importances = dict(zip(FEATURE_COLUMNS, clf.feature_importances_.round(4).tolist()))

    # Save metadata
    metadata = {
        "accuracy": round(float(acc * 100), 1),
        "target_genres": clf.classes_.tolist(),
        "genre_icons": GENRE_ICONS,
        "feature_columns": FEATURE_COLUMNS,
        "feature_importances": feature_importances,
        "training_samples_count": len(train_df)
    }
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {METADATA_PATH}")

    # Export representative sample tracks from the Kaggle dataset for instant UI testing
    export_sample_tracks(df)

def export_sample_tracks(df):
    print("Generating curated sample tracks from Kaggle Spotify dataset...")
    samples = []
    top_df = df.sort_values(by="popularity", ascending=False)
    
    seen_artists = set()
    for _, row in top_df.iterrows():
        artist = str(row["artists"]).split(";")[0].strip()
        if artist in seen_artists:
            continue
        seen_artists.add(artist)
        
        genre = row.get("broad_genre", "Unknown")
        samples.append({
            "track_name": str(row["track_name"]),
            "artist": artist,
            "album": str(row["album_name"]),
            "true_subgenre": str(row["track_genre"]),
            "broad_genre": str(genre),
            "popularity": int(row["popularity"]),
            "features": {
                "tempo": round(float(row["tempo"]), 1),
                "danceability": round(float(row["danceability"]), 2),
                "energy": round(float(row["energy"]), 2),
                "loudness": round(float(row["loudness"]), 1),
                "duration_ms": int(row["duration_ms"]),
                "valence": round(float(row["valence"]), 2),
                "acousticness": round(float(row["acousticness"]), 2),
                "speechiness": round(float(row["speechiness"]), 2),
                "instrumentalness": round(float(row["instrumentalness"]), 2)
            }
        })
        if len(samples) >= 60:
            break
            
    with open(SAMPLES_PATH, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)
    print(f"Exported {len(samples)} real sample tracks to {SAMPLES_PATH}")

if __name__ == "__main__":
    train_and_export_model()
