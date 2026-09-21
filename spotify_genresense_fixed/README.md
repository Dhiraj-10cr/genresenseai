# GenreSense AI — Spotify Tracks Genre Predictor

> **Google Stitch UI Integration + Kaggle Spotify Tracks Machine Learning Backend**

GenreSense AI is a full-stack audio classification application designed for music producers, audio engineers, and audiophiles. It combines a futuristic **"Sonic Luminescence"** dark glassmorphism interface (exported from Google Stitch) with a high-performance **Scikit-Learn Machine Learning backend** trained directly on the **Kaggle: Spotify Tracks Dataset** (114,000 tracks).

---

## Key Highlights

- **Stitch Frontend Integration:**
  - Preserved the complete design system: Syne display typography, Plus Jakarta Sans body, glassmorphism containers, neon cyan (`#00F2FE`) and magenta (`#FF4A8D`) accents.
  - Interactive audio vector inputs: BPM with **Tap Tempo**, Pitch/Key frequency, Beat Strength, Loudness, Duration, Energy, and Danceability.
  - Advanced acoustic dimension controls: Acousticness, Speechiness, and Instrumentalness.
  - **Live Pulse Visualizer:** Dynamic real-time HTML5 audio waveform canvas reacting to tempo and energy.
  - **Genre Matrix:** Explores the acoustic archetypes and feature ranges across musical taxonomies.
  - **Prediction History:** Tracks session predictions and confidence scores.
  - **Kaggle Spotify Track Sampler:** One-click sampler that pulls real tracks from Queen, Daft Punk, The Weeknd, Billie Eilish, etc. from Kaggle's Spotify dataset and evaluates them in real-time.

- **Kaggle Machine Learning Backend:**
  - Trained on 114,000 tracks from `maharshipandya/spotify-tracks-dataset`.
  - Balanced multi-class classification model with calibrated softmax likelihoods.
  - Standardized feature scaling (`StandardScaler`) on 9 core acoustic dimensions.
  - Fast inference latency (< 15ms) returning the top classified genre, certainty score, dynamic acoustic signatures (e.g. *High Energy*, *Dance-Ready*, *Heavy Bass Signature*), and sorted probability distribution bars.

---

## Project Structure

```
spotify_genresense/
├── data/
│   ├── dataset.csv            # Kaggle Spotify Tracks Dataset (114,000 records)
│   └── sample_tracks.json     # Curated real Spotify sample tracks
├── models/
│   ├── train_model.py         # Data preprocessing, feature scaling, model training
│   ├── genre_model.joblib     # Serialized classifier model
│   ├── scaler.joblib          # Serialized StandardScaler
│   └── model_metadata.json    # Target classes, accuracy, feature importances
├── templates/
│   └── index.html             # Integrated Stitch UI with real-time API bindings
├── app.py                     # Flask REST API + UI server
├── test_app.py                # Automated test suite (7 comprehensive test cases)
├── requirements.txt           # Python dependencies
├── DESIGN.md                  # Stitch design token specifications
└── screen.png                 # Original Stitch screen reference
```

---

## Quick Start

### 1. Run the Web Application
```powershell
python app.py
```
Open your browser at **`http://localhost:5000`**.

### 2. Run the Automated Test Suite
```powershell
python test_app.py
```

### 3. Retrain or Update the Model
```powershell
python models/train_model.py
```

---

## REST API Documentation

### `POST /api/predict`
Calculates predicted genre and probability distribution.

**Request Payload:**
```json
{
  "bpm": 128,
  "energy": 0.88,
  "danceability": 0.79,
  "loudness": -5.4,
  "duration": 214,
  "acousticness": 0.05,
  "instrumentalness": 0.65
}
```

**Response Payload:**
```json
{
  "success": true,
  "predicted_genre": "Electronic / Synth",
  "icon": "🎧",
  "confidence": 88.4,
  "probabilities": [
    { "genre": "Electronic / Synth", "probability": 88.4, "color": "#00f2fe" },
    { "genre": "Pop", "probability": 6.8, "color": "#ff4a8d" },
    { "genre": "Rock / Alternative", "probability": 2.4, "color": "#6ff6ff" },
    ...
  ],
  "acoustic_signatures": [
    { "label": "High Energy", "icon": "bolt", "color": "text-primary-fixed-dim" },
    { "label": "Dance-Ready", "icon": "nightlife", "color": "text-secondary" },
    { "label": "Heavy Bass Signature", "icon": "graphic_eq", "color": "text-tertiary-fixed-dim" }
  ]
}
```

### Additional Endpoints
- `GET /api/tracks/sample`: Retrieves a random real song from Kaggle's Spotify dataset.
- `GET /api/presets`: Returns standard sound design presets.
- `GET /api/status`: Returns ML model operational status and metadata.
- `GET /api/dataset/stats`: Returns dataset metrics.
- `GET /api/history` & `DELETE /api/history`: Manages session prediction logs.
