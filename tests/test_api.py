import sys
import unittest
from pathlib import Path


SERVER_DIR = Path(__file__).resolve().parents[1] / "server"
sys.path.insert(0, str(SERVER_DIR))

import server as app_module


class HomePriceApiTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def test_homepage_and_assets_are_served(self):
        homepage = self.client.get("/")
        self.assertEqual(homepage.status_code, 200)
        homepage.close()

        stylesheet = self.client.get("/app.css")
        self.assertEqual(stylesheet.status_code, 200)
        stylesheet.close()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_locations_endpoint_returns_locations(self):
        response = self.client.get("/api/get_location_names")
        self.assertEqual(response.status_code, 200)
        self.assertIn("indira nagar", response.get_json()["locations"])

    def test_prediction_endpoint_returns_estimate(self):
        response = self.client.post(
            "/api/predict_home_price",
            json={
                "total_sqft": 1000,
                "bhk": 2,
                "bath": 2,
                "location": "indira nagar",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json()["estimated_price"], (int, float))

    def test_prediction_rejects_invalid_area(self):
        response = self.client.post(
            "/api/predict_home_price",
            json={
                "total_sqft": -10,
                "bhk": 2,
                "bath": 2,
                "location": "indira nagar",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
