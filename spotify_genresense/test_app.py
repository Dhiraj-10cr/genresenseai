import unittest
import json
from app import app

class GenreSenseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GenreSense AI", response.data)
        self.assertIn(b"Predict Genre by Song Name", response.data)

    def test_api_status(self):
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "ready")
        self.assertTrue(data.get("dataset_loaded"))
        self.assertGreater(data.get("total_tracks", 0), 100000)

    def test_predict_by_name_single_match(self):
        # Searching Midnight City by M83
        payload = {
            "song_name": "Midnight City",
            "artist_name": "M83"
        }
        response = self.client.post(
            '/predict_by_name',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("found"))
        # If there are remixes of Midnight City by M83, it may return multiple or single
        if data.get("multiple"):
            self.assertIn("matches", data)
            self.assertLessEqual(len(data["matches"]), 5)
            # Pick first candidate and test exact selection
            first = data["matches"][0]
            pick_res = self.client.post(
                '/predict_by_name',
                data=json.dumps({"song_name": first["song_name"], "artist_name": first["artist_name"], "exact": True}),
                content_type='application/json'
            )
            pick_data = pick_res.get_json()
            self.assertTrue(pick_data.get("found"))
            self.assertFalse(pick_data.get("multiple"))
            self.assertIn("predicted_genre", pick_data)
            self.assertIn("matched_song", pick_data)
        else:
            self.assertIn("predicted_genre", data)
            self.assertIn("matched_song", data)
            self.assertIn("probabilities", data)

    def test_predict_by_name_multiple_candidates(self):
        # "Hold On" has many versions across artists in 114k dataset
        payload = {
            "song_name": "Hold On"
        }
        response = self.client.post(
            '/predict_by_name',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("found"))
        self.assertTrue(data.get("multiple"))
        self.assertIn("matches", data)
        self.assertLessEqual(len(data["matches"]), 5)
        self.assertGreater(len(data["matches"]), 1)
        self.assertIn("song_name", data["matches"][0])
        self.assertIn("artist_name", data["matches"][0])

    def test_predict_by_name_not_found(self):
        payload = {
            "song_name": "SuperNonExistentSongXyz999111"
        }
        response = self.client.post(
            '/predict_by_name',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data.get("found"))
        self.assertIn("message", data)
        self.assertIn("not found", data["message"].lower())

    def test_manual_predict_endpoint_preserved(self):
        # Existing manual feature entry endpoint
        payload = {
            "bpm": 128,
            "energy": 0.88,
            "danceability": 0.79,
            "loudness": -5.4,
            "duration": 214
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("predicted_genre", data)
        self.assertIn("probabilities", data)

    def test_presets_endpoint(self):
        response = self.client.get('/api/presets')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("song_name", data[0])

    def test_sample_tracks_endpoint(self):
        response = self.client.get('/api/tracks/sample')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("track_name", data)
        self.assertIn("artist", data)

if __name__ == "__main__":
    unittest.main()
