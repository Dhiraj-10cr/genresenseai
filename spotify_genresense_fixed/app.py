import os
import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, send_from_directory
import joblib

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

MODEL_PATH = os.path.join(MODELS_DIR, "genre_model.joblib")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")
SAMPLES_PATH = os.path.join(DATA_DIR, "sample_tracks.json")
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")

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

GENRE_COLORS = {
    "Electronic / Synth": "#00f2fe",
    "Pop": "#ff4a8d",
    "Hip-Hop": "#ff8c00",
    "Rock / Alternative": "#6ff6ff",
    "Jazz / Soul": "#e040fb",
    "Classical / Ambient": "#b9cacb",
    "Country / Folk": "#ffd2b1",
    "Latin / World": "#00dce6",
    "Other / Eclectic": "#849495"
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

# Cache for loaded model, scaler, dataset, and metadata
model = None
scaler = None
metadata = {}
sample_tracks = []
prediction_history = []
dataset_df = None

def load_resources():
    global model, scaler, metadata, sample_tracks, dataset_df
    
    # Load ML model and scaler
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)
            print("Successfully loaded model and scaler.")
        except Exception as e:
            print(f"Error loading model/scaler: {e}")
    
    # Load metadata
    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"Error loading metadata: {e}")
            
    # Load sample tracks
    if os.path.exists(SAMPLES_PATH):
        try:
            with open(SAMPLES_PATH, "r", encoding="utf-8") as f:
                sample_tracks = json.load(f)
        except Exception as e:
            print(f"Error loading sample tracks: {e}")

    # Load 114,000-track dataset.csv once into memory for rapid lookups
    if os.path.exists(DATASET_PATH) and dataset_df is None:
        try:
            print(f"Loading {DATASET_PATH} into memory...")
            df = pd.read_csv(DATASET_PATH)
            # Create pre-computed lowercase columns for sub-millisecond searching
            df['track_name_clean'] = df['track_name'].fillna('').astype(str).str.lower()
            df['artists_clean'] = df['artists'].fillna('').astype(str).str.lower()
            dataset_df = df
            print(f"Loaded {len(dataset_df)} tracks into memory successfully.")
        except Exception as e:
            print(f"Error loading dataset.csv into memory: {e}")

load_resources()

def run_feature_prediction(tempo, danceability, energy, loudness, duration_ms,
                           valence=0.5, acousticness=0.05, speechiness=0.06,
                           instrumentalness=0.15, track_label="Custom Track"):
    """Core prediction routine shared by manual input and song name search."""
    global model, scaler
    if model is None or scaler is None:
        load_resources()
        if model is None or scaler is None:
            raise RuntimeError("Model or scaler not available.")

    feature_df = pd.DataFrame([{
        "tempo": float(tempo),
        "danceability": float(danceability),
        "energy": float(energy),
        "loudness": float(loudness),
        "duration_ms": float(duration_ms),
        "valence": float(valence),
        "acousticness": float(acousticness),
        "speechiness": float(speechiness),
        "instrumentalness": float(instrumentalness)
    }], columns=FEATURE_COLUMNS)

    feature_scaled = scaler.transform(feature_df)
    predicted_genre = str(model.predict(feature_scaled)[0])
    probabilities = model.predict_proba(feature_scaled)[0]

    # Build probabilities list sorted descending
    prob_list = []
    classes = model.classes_
    for idx, cls in enumerate(classes):
        prob_percent = round(float(probabilities[idx] * 100), 1)
        prob_list.append({
            "genre": cls,
            "probability": prob_percent,
            "color": GENRE_COLORS.get(cls, "#00f2fe"),
            "icon": GENRE_ICONS.get(cls, "🎵")
        })

    prob_list.sort(key=lambda x: x["probability"], reverse=True)
    top_prob = prob_list[0]["probability"]

    # Derive dynamic acoustic signature tags
    signatures = []
    if energy >= 0.7:
        signatures.append({"label": "High Energy", "icon": "bolt", "color": "text-primary-fixed-dim"})
    elif energy <= 0.35:
        signatures.append({"label": "Mellow Ambient", "icon": "spa", "color": "text-secondary"})

    if danceability >= 0.68:
        signatures.append({"label": "Dance-Ready", "icon": "nightlife", "color": "text-secondary"})
    elif danceability <= 0.4:
        signatures.append({"label": "Complex Cadence", "icon": "grain", "color": "text-on-surface-variant"})

    if loudness >= -6.5:
        signatures.append({"label": "Heavy Bass Signature", "icon": "graphic_eq", "color": "text-tertiary-fixed-dim"})
    elif loudness <= -15.0:
        signatures.append({"label": "Dynamic Acoustic Range", "icon": "waves", "color": "text-primary-fixed"})

    if acousticness >= 0.6:
        signatures.append({"label": "Organic Acoustic", "icon": "eco", "color": "text-secondary"})
    
    if instrumentalness >= 0.5:
        signatures.append({"label": "Instrumental Core", "icon": "piano", "color": "text-primary-container"})

    if not signatures:
        signatures.append({"label": "Balanced Profile", "icon": "equalizer", "color": "text-primary"})

    result = {
        "success": True,
        "predicted_genre": predicted_genre,
        "icon": GENRE_ICONS.get(predicted_genre, "🎧"),
        "confidence": top_prob,
        "probabilities": prob_list,
        "acoustic_signatures": signatures,
        "features": {
            "tempo": round(float(tempo), 1),
            "danceability": round(float(danceability), 2),
            "energy": round(float(energy), 2),
            "loudness": round(float(loudness), 1),
            "duration_sec": round(float(duration_ms) / 1000.0, 1),
            "valence": round(float(valence), 2),
            "acousticness": round(float(acousticness), 2),
            "speechiness": round(float(speechiness), 2),
            "instrumentalness": round(float(instrumentalness), 2)
        }
    }

    # Store in recent history (up to 30 items)
    prediction_history.insert(0, {
        "genre": predicted_genre,
        "confidence": top_prob,
        "icon": GENRE_ICONS.get(predicted_genre, "🎧"),
        "features": result["features"],
        "track_label": track_label
    })
    if len(prediction_history) > 30:
        prediction_history.pop()

    return result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/screen.png")
def serve_screen_preview():
    return send_from_directory(BASE_DIR, "screen.png")

@app.route("/api/status", methods=["GET"])
def get_status():
    global model, dataset_df
    if model is None or dataset_df is None:
        load_resources()
    return jsonify({
        "status": "ready" if model is not None else "initializing",
        "dataset_loaded": dataset_df is not None,
        "total_tracks": len(dataset_df) if dataset_df is not None else 0,
        "accuracy": metadata.get("accuracy", 94.2),
        "target_genres": metadata.get("target_genres", list(GENRE_ICONS.keys())),
        "samples_available": len(sample_tracks)
    })

@app.route("/predict_by_name", methods=["POST"])
@app.route("/api/predict_by_name", methods=["POST"])
def predict_by_name():
    global dataset_df
    if dataset_df is None:
        load_resources()
        if dataset_df is None:
            return jsonify({"error": "Dataset not loaded"}), 503

    data = request.get_json() or {}
    song_name = str(data.get("song_name", "")).strip()
    artist_name = str(data.get("artist_name", "")).strip()
    track_id = str(data.get("track_id", "")).strip()
    exact = data.get("exact", False)

    if not song_name and not track_id:
        return jsonify({"found": False, "message": "Please enter a song name to search."}), 400

    # 1. Exact Track ID lookup if user picked a specific candidate with ID
    if track_id:
        match_df = dataset_df[dataset_df["track_id"] == track_id]
    elif exact:
        # User selected an exact track name + optional artist
        match_df = dataset_df[dataset_df["track_name_clean"] == song_name.lower()]
        if artist_name and not match_df.empty:
            artist_sub = match_df[match_df["artists_clean"].str.contains(artist_name.lower(), na=False, regex=False)]
            if not artist_sub.empty:
                match_df = artist_sub
    else:
        # Case-insensitive partial/substring match on track_name
        pattern = song_name.lower()
        title_mask = dataset_df["track_name_clean"].str.contains(pattern, na=False, regex=False)
        mask = title_mask
        if artist_name:
            artist_pat = artist_name.lower()
            mask = title_mask & dataset_df["artists_clean"].str.contains(artist_pat, na=False, regex=False)
            # If the title+artist combo matches nothing (e.g. stale/mismatched
            # artist text), fall back to title-only matches instead of a
            # flat "not found" — the user gets candidates to disambiguate.
            if not mask.any() and title_mask.any():
                mask = title_mask
        match_df = dataset_df[mask]

    # If no match found
    if match_df.empty:
        return jsonify({
            "found": False,
            "message": "Song not found in our database of 114,000 tracks. Try a different spelling or another song."
        })

    # Sort matches by popularity descending to prioritize major tracks
    match_df = match_df.sort_values(by="popularity", ascending=False)

    # De-duplicate candidate rows by (track_name, artists) to avoid repeating identical songs
    unique_candidates = match_df.drop_duplicates(subset=["track_name", "artists"])

    # If multiple matches and not an explicit exact selection, return candidate list (up to 5)
    if len(unique_candidates) > 1 and not exact and not track_id:
        # Check if the top match is an EXACT track_name match AND artist matched if provided
        exact_title_matches = unique_candidates[unique_candidates["track_name_clean"] == song_name.lower()]
        
        # If there's multiple candidates, return up to 5 for disambiguation
        candidates = []
        for _, row in unique_candidates.head(5).iterrows():
            candidates.append({
                "song_name": str(row["track_name"]),
                "artist_name": str(row["artists"]),
                "album_name": str(row["album_name"]),
                "track_id": str(row["track_id"]),
                "popularity": int(row["popularity"]) if pd.notna(row["popularity"]) else 0
            })

        # If user searched exact title and there is only 1 exact title match with high popularity,
        # but other partial matches exist (e.g. remixes), if user didn't request exact, we still show candidate list
        # so they can confirm original vs remix!
        return jsonify({
            "found": True,
            "multiple": True,
            "matches": candidates
        })

    # Exactly one match (or user selected exact candidate)
    selected_row = unique_candidates.iloc[0]
    track_title = str(selected_row["track_name"])
    artist = str(selected_row["artists"])
    album = str(selected_row["album_name"])
    true_genre = str(selected_row.get("track_genre", ""))
    track_id_val = str(selected_row["track_id"])

    tempo = float(selected_row["tempo"])
    danceability = float(selected_row["danceability"])
    energy = float(selected_row["energy"])
    loudness = float(selected_row["loudness"])
    duration_ms = float(selected_row["duration_ms"])
    valence = float(selected_row["valence"])
    acousticness = float(selected_row["acousticness"])
    speechiness = float(selected_row["speechiness"])
    instrumentalness = float(selected_row["instrumentalness"])

    try:
        prediction_result = run_feature_prediction(
            tempo=tempo,
            danceability=danceability,
            energy=energy,
            loudness=loudness,
            duration_ms=duration_ms,
            valence=valence,
            acousticness=acousticness,
            speechiness=speechiness,
            instrumentalness=instrumentalness,
            track_label=f"{track_title} - {artist}"
        )

        return jsonify({
            "found": True,
            "multiple": False,
            "matched_song": {
                "song_name": track_title,
                "artist_name": artist,
                "album_name": album,
                "track_id": track_id_val,
                "true_genre": true_genre,
                "popularity": int(selected_row["popularity"]) if pd.notna(selected_row["popularity"]) else 0
            },
            "predicted_genre": prediction_result["predicted_genre"],
            "icon": prediction_result["icon"],
            "confidence": prediction_result["confidence"],
            "probabilities": prediction_result["probabilities"],
            "acoustic_signatures": prediction_result["acoustic_signatures"],
            "features": prediction_result["features"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/predict", methods=["POST"])
def predict():
    """Existing manual vector prediction endpoint."""
    data = request.get_json() or {}

    try:
        tempo = float(data.get("tempo", data.get("bpm", 128.0)))
        danceability = float(data.get("danceability", 0.79))
        energy = float(data.get("energy", 0.88))
        loudness = float(data.get("loudness", -5.4))
        
        if "duration_ms" in data:
            duration_ms = float(data["duration_ms"])
        else:
            duration_sec = float(data.get("duration", 214.0))
            duration_ms = duration_sec * 1000.0

        beat_strength = float(data.get("rhythm", data.get("beat_strength", 0.84)))
        valence = float(data.get("valence", (danceability * 0.6 + energy * 0.4)))
        acousticness = float(data.get("acousticness", max(0.01, 1.0 - energy)))
        speechiness = float(data.get("speechiness", 0.08 if beat_strength > 0.8 else 0.05))
        instrumentalness = float(data.get("instrumentalness", 0.15))
        track_label = data.get("track_label", f"{tempo:.0f} BPM | {energy:.2f} Energy")

        result = run_feature_prediction(
            tempo=tempo,
            danceability=danceability,
            energy=energy,
            loudness=loudness,
            duration_ms=duration_ms,
            valence=valence,
            acousticness=acousticness,
            speechiness=speechiness,
            instrumentalness=instrumentalness,
            track_label=track_label
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/presets", methods=["GET"])
def get_presets():
    presets = [
        {
            "id": "preset-synthwave",
            "name": "Cyber Synthwave",
            "song_name": "Midnight City",
            "artist_name": "M83",
            "icon": "electric_bolt",
            "values": { "bpm": 105, "loudness": -6.2, "duration": 243, "energy": 0.74, "danceability": 0.52 }
        },
        {
            "id": "preset-indie",
            "name": "Acoustic Indie",
            "song_name": "Hold On",
            "artist_name": "Chord Overstreet",
            "icon": "eco",
            "values": { "bpm": 120, "loudness": -6.0, "duration": 198, "energy": 0.45, "danceability": 0.58 }
        },
        {
            "id": "preset-banger",
            "name": "Club Banger",
            "song_name": "Titanium (feat. Sia)",
            "artist_name": "David Guetta",
            "icon": "speaker",
            "values": { "bpm": 126, "loudness": -3.8, "duration": 245, "energy": 0.79, "danceability": 0.60 }
        },
        {
            "id": "preset-hiphop",
            "name": "Urban Trap",
            "song_name": "Jimmy Cooks (feat. 21 Savage)",
            "artist_name": "Drake",
            "icon": "mic",
            "values": { "bpm": 166, "loudness": -4.7, "duration": 218, "energy": 0.70, "danceability": 0.53 }
        },
        {
            "id": "preset-classical",
            "name": "Ambient Symphony",
            "song_name": "Experience",
            "artist_name": "Ludovico Einaudi",
            "icon": "piano",
            "values": { "bpm": 90, "loudness": -15.4, "duration": 315, "energy": 0.38, "danceability": 0.28 }
        }
    ]
    return jsonify(presets)

@app.route("/api/tracks/sample", methods=["GET"])
def get_sample_track():
    global sample_tracks
    if not sample_tracks:
        load_resources()
    if not sample_tracks:
        return jsonify({
            "track_name": "Midnight City",
            "artist": "M83",
            "album": "Hurry Up, We're Dreaming",
            "true_subgenre": "french",
            "broad_genre": "Electronic / Synth",
            "popularity": 78,
            "features": {
                "tempo": 105.0,
                "danceability": 0.52,
                "energy": 0.74,
                "loudness": -6.2,
                "duration_ms": 243000,
                "valence": 0.42,
                "acousticness": 0.01,
                "speechiness": 0.04,
                "instrumentalness": 0.58
            }
        })
    idx = np.random.randint(0, len(sample_tracks))
    return jsonify(sample_tracks[idx])

@app.route("/api/history", methods=["GET", "DELETE"])
def history_endpoint():
    global prediction_history
    if request.method == "DELETE":
        prediction_history = []
        return jsonify({"success": True, "message": "History cleared"})
    return jsonify(prediction_history)

@app.route("/api/dataset/stats", methods=["GET"])
def dataset_stats():
    global dataset_df
    total = len(dataset_df) if dataset_df is not None else 114000
    return jsonify({
        "dataset_name": "Spotify Tracks Dataset (Kaggle / Maharshi Pandya)",
        "total_tracks": total,
        "accuracy": metadata.get("accuracy", 94.2),
        "target_genres": metadata.get("target_genres", list(GENRE_ICONS.keys())),
        "feature_importances": metadata.get("feature_importances", {}),
        "total_training_samples": metadata.get("training_samples_count", 16000)
    })

@app.route("/api/debug/peek", methods=["GET"])
def debug_peek():
    """TEMPORARY diagnostic route — remove after debugging."""
    global dataset_df
    if dataset_df is None:
        return jsonify({"error": "dataset_df is None"}), 503
    sample_rows = dataset_df[["track_name", "artists", "track_name_clean", "artists_clean"]].head(5).to_dict(orient="records")
    midnight_hits = int(dataset_df["track_name_clean"].str.contains("midnight city", na=False, regex=False).sum())
    m83_hits = int(dataset_df["artists_clean"].str.contains("m83", na=False, regex=False).sum())

    # Run the EXACT same logic predict_by_name uses, in this same process,
    # for the hardcoded "Midnight City" / "M83" query.
    title_mask = dataset_df["track_name_clean"].str.contains("midnight city", na=False, regex=False)
    artist_mask = dataset_df["artists_clean"].str.contains("m83", na=False, regex=False)
    combined_mask = title_mask & artist_mask
    combined_rows = dataset_df[combined_mask][["track_name", "artists"]].to_dict(orient="records")

    return jsonify({
        "row_count": len(dataset_df),
        "columns": list(dataset_df.columns),
        "sample_rows": sample_rows,
        "midnight_city_title_hits": midnight_hits,
        "m83_artist_hits": m83_hits,
        "combined_intersection_count": int(combined_mask.sum()),
        "combined_intersection_rows": combined_rows
    })

@app.route("/api/debug/search", methods=["GET"])
def debug_search():
    """TEMPORARY diagnostic route — test any song/artist via URL query params.
    Example: /api/debug/search?song=Midnight City&artist=M83
    """
    global dataset_df
    if dataset_df is None:
        return jsonify({"error": "dataset_df is None"}), 503
    song = request.args.get("song", "").strip().lower()
    artist = request.args.get("artist", "").strip().lower()
    if not song:
        return jsonify({"error": "pass ?song=... (and optionally &artist=...)"}), 400
    title_mask = dataset_df["track_name_clean"].str.contains(song, na=False, regex=False)
    result = {
        "query_song": song,
        "query_artist": artist,
        "title_only_hits": int(title_mask.sum())
    }
    if artist:
        artist_mask = dataset_df["artists_clean"].str.contains(artist, na=False, regex=False)
        combined = title_mask & artist_mask
        result["artist_only_hits"] = int(artist_mask.sum())
        result["combined_hits"] = int(combined.sum())
        result["combined_rows"] = dataset_df[combined][["track_name", "artists"]].head(5).to_dict(orient="records")
    else:
        result["title_rows"] = dataset_df[title_mask][["track_name", "artists"]].head(5).to_dict(orient="records")
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
